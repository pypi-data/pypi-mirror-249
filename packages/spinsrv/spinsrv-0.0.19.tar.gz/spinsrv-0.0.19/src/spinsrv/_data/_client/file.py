import spinsrv._data as data

from fsspec import spec  # type: ignore

# I copied in a sample from the Databricks filesystem implementation
# https://github.com/fsspec/filesystem_spec/blob/master/fsspec/implementations/dbfs.py
class File(spec.AbstractBufferedFile):
    """
    Helper class for files referenced in the SpinFileSystem.
    """

    DEFAULT_BLOCK_SIZE = 10 * 2**20

    def __init__(
        self,
        fs,
        path,
        mode="rb",
        block_size="default",
        autocommit=True,
        cache_type="readahead",
        cache_options=None,
        **kwargs,
    ):
        """
        Create a new instance of the SpinFile.

        """
        if block_size is None or block_size == "default":
            block_size = self.DEFAULT_BLOCK_SIZE

        self.dir_entry = None

        super().__init__(
            fs,
            path,
            mode=mode,
            block_size=block_size,
            autocommit=autocommit,
            cache_type=cache_type,
            cache_options=cache_options or {},
            **kwargs,
        )

    def _initiate_upload(self):
        """Internal function to start a file upload"""
        pt = self.fs.ns.client.options.pack_type
        if pt != data.PackType.MissingPackType and pt != data.PackType.PlainPack:
            raise NotImplementedError(f"Pack type {pt} not implemented")
        if pt == data.PackType.MissingPackType:
            pt = data.PackType.PlainPack

        self.dir_entry = data.Entry(
            type=data.FileEntry,
            citizen=self.fs.ns.ctzn,
            path=self.path,
            version=data.IgnoreVersion,
            pack_type=pt,
        )

    def _upload_chunk(self, final=False):
        """Internal function to add a chunk of data to a started upload"""
        self.buffer.seek(0)
        bs = self.buffer.getvalue()

        data_chunks = [bs[start:end] for start, end in self._to_sized_blocks(len(bs))]

        for (i, data_chunk) in enumerate(data_chunks):
            resp = self.fs.ns.client.options.bit_server.ops(
                data.BitOpsRequest(
                    public=self.fs.ns.client.options.public,
                    private=self.fs.ns.client.options.private,
                    ops=[data.BitOp(type=data.PutBitOp, bytes=data_chunk)],
                )
            )

            if resp.error != "":
                print(resp)
                raise OSError(resp.error)  # TODO: better handling?

            if len(resp.outcomes) != 1:
                print(resp)
                raise OSError(f"expected 1 outcome, got {len(resp.outcomes)}")

            self.dir_entry.blocks.append(
                data.EntryBlock(
                    address=resp.outcomes[0].store_ref.address,
                    reference=resp.outcomes[0].store_ref.reference,
                    offset=self.offset + i * self.blocksize,
                    size=len(data_chunk),
                )
            )

        if final:
            resp = self.fs.ns.client.options.dir_server.apply(
                data.DirApplyRequest(
                    public=self.fs.ns.client.options.public,
                    private=self.fs.ns.client.options.private,
                    ops=[data.DirOp(type=data.PutDirOp, entry=self.dir_entry)],
                )
            )
            if resp.error != "":
                print(resp)
                raise OSError(resp.error)  # TODO: better handling
            self.dir_entry = resp.entries[0]
            self.fs.invalidate_cache(self.fs._parent(self.dir_entry.path))
            return True

    # warn: this code is not seriously tested
    def _intersection(self, a, b, c, d):
        # compute [a, b] ∩ [c,d]
        if b < c or a > d:
            return (0, 0)
        return (max(a, c), min(b, d))

    # warn: this code is not seriously tested
    def _blocks_in_range(self, start, end):
        # find the blocks for the file for the bit range start to end
        out = []
        for b in self.dir_entry.blocks:
            bstart, bend = b.offset, b.offset + b.size
            istart, iend = self._intersection(start, end, bstart, bend)
            if iend - istart == 0:  # skip if empty intersection
                continue
            out.append((b, (istart, iend)))
        return out

    def _fetch_range(self, start, end):
        """Internal function to download a block of data"""
        if self.dir_entry is None:
            self.dir_entry = self.fs._lookup(self.path)

        return_buffer = b""
        for (b, (s, e)) in self._blocks_in_range(start, end):
            data = self.fs._get(b.address, b.reference)
            return_buffer += data[start - b.offset : end]
        return return_buffer

    def _to_sized_blocks(self, total_length):
        """Helper function to split a range from 0 to total_length into blocksizes"""
        for data_chunk in range(0, total_length, self.blocksize):
            data_start = data_chunk
            data_end = min(total_length, data_chunk + self.blocksize)
            yield data_start, data_end
