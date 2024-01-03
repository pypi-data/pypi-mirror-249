import dataclasses
import functools
import os
import typing

from fsspec import spec  # type: ignore


import spinsrv._spin as spin
import spinsrv._data as data
from spinsrv._data._client.file import File
import spinsrv._data._client.client as client


@dataclasses.dataclass
class Options:
    public: str = ""

    private: str = ""

    citizen: str = ""

    # TODO: use store not bit client
    dir_server: typing.Union[data.DirServerHTTPClient, None] = None

    bit_server: typing.Union[data.BitServerHTTPClient, None] = None

    pack_type: data.PackType = data.PackType.MissingPackType


# TODO: should be the notion of a namespace, and the fs should live on that ?


class Client:
    def __init__(self, options: Options):
        self.options = options

    def namespace(self, ctzn: spin.Name):
        return Namespace(self, ctzn)

    def put(
        self, address: data.BlockAddress, bs: bytes
    ) -> typing.Union[data.StoreRef, spin.Error]:
        return spin.ErrNotImplemented

    # get the data from the store
    @functools.lru_cache(maxsize=2000)
    def get(
        self, addr: data.BlockAddress, ref: data.BlockReference
    ) -> typing.Union[bytes, spin.Error]:
        if self.options.bit_server is None:
            return spin.ErrNotImplemented

        resp = self.options.bit_server.ops(
            data.BitOpsRequest(
                public=self.options.public,
                private=self.options.private,
                ops=[
                    data.BitOp(
                        type=data.GetBitOp,
                        address=addr,
                        reference=ref,
                    )
                ],
            )
        )
        if resp.error != "":
            return spin.error_from_string(resp.error)
        if len(resp.outcomes) != 1:
            raise OSError(f"expected 1 outcome, got {len(resp.outcomes)}")

        return resp.outcomes[0].bytes

    def delete(self, address: data.BlockAddress) -> typing.Union[spin.Error, None]:
        return spin.ErrNotImplemented

    def _lookup(
        self, ctzn: spin.Name, path: spin.Path
    ) -> typing.Union[data.Entry, spin.Error]:
        if self.options.dir_server is None:
            return spin.ErrNotImplemented

        resp = self.options.dir_server.list(
            data.DirListRequest(
                public=self.options.public,
                private=self.options.private,
                citizen=ctzn,
                path=path,
                level=0,
            )
        )
        if resp.error != "":
            return spin.error_from_string(resp.error)
        if len(resp.entries) != 1:
            # TODO better
            raise OSError(f"expected 1 entry, got {len(resp.entries)}")
        return resp.entries[0]

    def _read_directory(
        self, ctzn: spin.Name, path: spin.Path
    ) -> typing.Union[list[data.Entry], spin.Error]:
        if self.options.dir_server is None:
            return spin.ErrNotImplemented

        resp = self.options.dir_server.list(
            data.DirListRequest(
                public=self.options.public,
                private=self.options.private,
                citizen=ctzn,
                path=path,
                level=1,
            )
        )
        if resp.error != "":
            return spin.error_from_string(resp.error)
        return resp.entries[1:]  # exclude the root

    def _ensureDirectory(
        self, ctzn: spin.Name, path: spin.Path, no_prior: bool = False
    ) -> typing.Union[data.Entry, spin.Error]:
        if self.options.dir_server is None:
            return spin.ErrNotImplemented
        resp = self.options.dir_server.apply(
            data.DirApplyRequest(
                public=self.options.public,
                private=self.options.private,
                ops=[
                    data.DirOp(
                        type=data.PutDirOp,
                        entry=data.Entry(
                            citizen=ctzn,
                            path=path,
                            type=data.DirectoryEntry,
                            time=spin.now(),
                            version=data.NoPriorVersion
                            if no_prior
                            else data.IgnoreVersion,
                        ),
                    )
                ],
            )
        )
        if resp.error != "":
            return spin.error_from_string(resp.error)
        if len(resp.outcomes) != 1:
            raise OSError(f"expected 1 outcome, got {len(resp.outcomes)}")
        return resp.outcomes[0].entry

    def _ensureDirectoryAllPath(
        self,
        ctzn: spin.Name,
        p: spin.Path,
        frm: spin.Path,
        no_prior: bool = False,
    ) -> typing.Union[list[data.Entry], spin.Error]:
        if frm != "" and not spin.path_is_ancestor(frm, p):
            return spin.Error(f"{frm} is not an ancestor of {p}")
        if self.options.dir_server is None:
            return spin.ErrNotImplemented
        ps = spin.path_sequence(p)
        ops = []
        for p in ps:
            if frm != "" and spin.path_is_ancestor(p, frm):
                continue  # skip the path if it is an ancestor of frm
            ops.append(
                data.DirOp(
                    type=data.PutDirOp,
                    entry=data.Entry(
                        citizen=ctzn,
                        path=p,
                        type=data.DirectoryEntry,
                        time=spin.now(),
                        version=data.NoPriorVersion if no_prior else data.IgnoreVersion,
                    ),
                )
            )
        resp = self.options.dir_server.apply(
            data.DirApplyRequest(
                public=self.options.public,
                private=self.options.private,
                ops=ops,
            )
        )
        if resp.error != "":
            return spin.error_from_string(resp.error)
        if len(resp.entries) != len(ops):
            raise OSError(f"expected {len(ops)} entries, got {len(resp.entries)}")
        return resp.entries

    def _open(
        self,
        ctzn: spin.Name,
        path: spin.Path,
        mode="rb",
        block_size="default",
        **kwargs,
    ):
        return File(
            self.namespace("/").fs(), path, mode=mode, block_size=block_size, **kwargs
        )


class Namespace:
    def __init__(self, client: Client, ctzn: spin.Name):
        self.client = client
        self.ctzn = ctzn
        self.root = spin.Path("/")

    def _fullPath(self, name: str) -> str:
        return os.path.join(self.root, name)

    def change_directory(self, name: str) -> typing.Union[spin.Error, None]:
        self.root = os.path.join(self.root, name)
        return None

    def lookup(self, name: str) -> typing.Union[data.Entry, spin.Error]:
        return self.client._lookup(self.ctzn, self._fullPath(name))

    def read_directory(self, name: str) -> typing.Union[list[data.Entry], spin.Error]:
        return self.client._read_directory(self.ctzn, self._fullPath(name))

    def make_directory(
        self, name: str, no_prior=False
    ) -> typing.Union[data.Entry, spin.Error]:
        return self.client._ensureDirectory(
            self.ctzn, self._fullPath(name), no_prior=no_prior
        )

    def make_directory_all(
        self, name: str, no_prior=False
    ) -> typing.Union[list[data.Entry], spin.Error]:
        return self.client._ensureDirectoryAllPath(
            self.ctzn, self._fullPath(name), self.root, no_prior=no_prior
        )

    def open(
        self, name: str, mode="rb", block_size="default", **kwargs
    ) -> typing.Union[File, spin.Error]:
        return self.client._open(self.ctzn, self._fullPath(name))

    def fs(self) -> "FileSystem":
        return FileSystem(self)


# I copied in a sample from the Databricks filesystem implementation
# https://github.com/fsspec/filesystem_spec/blob/master/fsspec/implementations/dbfs.py
class FileSystem(spec.AbstractFileSystem):
    protocol = "spin"
    root_marker = "/"

    def __init__(self, ns: client.Namespace, *args, **kwargs):
        self.ns = ns

        super().__init__(*args, **kwargs)

    def ls(self, path, detail=True, refresh=False):
        """
        List the contents of the given path.

        Parameters
        ----------
        path: str
            Absolute path
        detail: bool
            Return not only the list of filenames,
            but also additional information on file sizes
            and types.
        """

        if refresh:
            self.invalidate_cache(path)

        out = self._ls_from_cache(path)
        if not out:
            entries = self.ns.read_directory(path)
            out = [
                {
                    # these three are required
                    "name": e.path,
                    "type": "directory" if e.type == data.DirectoryEntry else "file",
                    "size": sum([b.size for b in e.blocks]),
                }
                for e in entries
            ]
            self.dircache[path.rstrip("/")] = out

        if detail:
            return out
        else:
            return sorted([o["name"] for o in out])

    # helper to get parents of a path, used by makedirs below
    def _parents(self, path):
        x = path.split("/")
        ps = []
        for i in range(1, len(x)):
            ps.append("/".join(x[0 : i + 1]))
        return ps

    def makedirs(self, path, exist_ok=True):
        """
        Create a given absolute path and all of its parents.

        Parameters
        ----------
        path: str
            Absolute path to create
        exist_ok: bool
            If false, checks if the folder
            exists before creating it (and raises an
            Exception if this is the case)
        """
        out = self.ns.make_directory_all(path)
        if isinstance(out, spin.Error):
            raise Exception(out)

        for e in out:
            self.invalidate_cache(self._parent(e.path))

    def mkdir(self, path, create_parents=True, **kwargs):
        """
        Create a given absolute path and all of its parents.

        Parameters
        ----------
        path: str
            Absolute path to create
        create_parents: bool
            Whether to create all parents or not.
            "False" is not implemented so far.
        """
        if not create_parents:
            return self.ns.make_directory(path, **kwargs)

        out = self.mkdirs(path, **kwargs)
        if isinstance(out, spin.Error):
            raise Exception(out)

        self.invalidate_cache(self._parent(path))

    def cp_file(self, frompath, topath, **kwargs):
        e = self._lookup(frompath)
        if e is None:
            raise FileNotFoundError(f"path {frompath}")
        ne = data.Entry(
            citizen=e.citizen,
            path=topath,
            version=data.IgnoreVersion,
            time=spin.now(),
            type=e.type,
            pack_type=e.pack_type,
            pack_data=e.pack_data,
            blocks=e.blocks,
            license=e.license,
        )
        resp = self.ns.client.options.dir_server.apply(
            data.DirApplyRequest(
                public=self.ns.client.options.public,
                private=self.ns.client.options.private,
                ops=[
                    data.DirOp(
                        type=data.PutDirOp,
                        entry=ne,
                    )
                ],
            )
        )
        if resp.error != "":
            raise OSError(resp.error)
        self.invalidate_cache(self._parent(topath))

    def rm_file(self, path):
        resp = self.ns.client.options.dir_server.apply(
            data.DirApplyRequest(
                public=self.ns.client.options.public,
                private=self.ns.client.options.private,
                ops=[
                    data.DirOp(
                        type=data.DelDirOp,
                        entry=data.Entry(
                            citizen=self.ns.ctzn,
                            path=path,
                            version=data.IgnoreVersion,
                        ),
                    )
                ],
            )
        )
        if resp.error != "":
            raise OSError(resp.error)  # TODO: better error handling?
        # TODO check for error on resp
        self.invalidate_cache(self._parent(path))

    def _open(self, path, mode="rb", block_size="default", **kwargs):
        """
        Overwrite the base class method to make sure to create a File.
        All arguments are copied from the base method.
        """
        return File(self, path, mode=mode, block_size=block_size, **kwargs)

    # lookup a dir entry
    def _lookup(self, path: spin.Path) -> typing.Union[data.Entry, spin.Error]:
        return self.ns.client._lookup(self.ns.client.options.citizen, path)

    def _get(
        self, addr: data.BlockAddress, ref: data.BlockReference
    ) -> typing.Union[bytes, spin.Error]:
        return self.ns.client.get(addr, ref)

    def invalidate_cache(self, path=None):
        if path is None:
            self.dircache.clear()
        else:
            self.dircache.pop(path, None)
        super().invalidate_cache(path)
