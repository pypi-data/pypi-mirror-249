import dataclasses
import requests

import spinsrv._spin as spin
from spinsrv._data.dir_ops import DirOp
from spinsrv._data.entries import Entry
from spinsrv._data.entry_levels import EntryLevel
from spinsrv._data.path_patterns import PathPattern


@dataclasses.dataclass
class DirApplyRequest:
    public: str = ""
    private: str = ""
    ops: list[DirOp] = dataclasses.field(default_factory=list)

    @staticmethod
    def from_json(j: dict):
        r = DirApplyRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]
        if "Ops" in j and j["Ops"] is not None:
            self.ops = [DirOp.from_json(op) for op in j["Ops"]]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Ops"] = [op.to_json() for op in self.ops]


@dataclasses.dataclass
class DirApplyResponse:
    entries: list[Entry] = dataclasses.field(default_factory=list)
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = DirApplyResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Entries" in j and j["Entries"] is not None:
            self.entries = [Entry.from_json(op) for op in j["Entries"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Entries"] = [op.to_json() for op in self.entries]
        j["Error"] = self.error


@dataclasses.dataclass
class DirListRequest:
    public: str = ""
    private: str = ""
    citizen: spin.Name = ""
    path: spin.Path = ""
    level: EntryLevel = 0
    pattern: PathPattern = ""

    @staticmethod
    def from_json(j: dict):
        r = DirListRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]
        if "Citizen" in j:
            self.citizen = j["Citizen"]
        if "Path" in j:
            self.path = j["Path"]
        if "Level" in j:
            self.level = j["Level"]
        if "Pattern" in j:
            self.pattern = j["Pattern"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Citizen"] = self.citizen
        j["Path"] = self.path
        j["Level"] = self.level
        j["Pattern"] = self.pattern


@dataclasses.dataclass
class DirListResponse:
    entries: list[Entry] = dataclasses.field(default_factory=list)
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = DirListResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Entries" in j and j["Entries"] is not None:
            self.entries = [Entry.from_json(op) for op in j["Entries"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Entries"] = [op.to_json() for op in self.entries]
        j["Error"] = self.error


# TODO: watch

DefaultDirProtocolVersion = "v0.0.0"
DefaultDirServerAddress = "https://dirs-ddh4amviaq-uw.a.run.app"


class DirServerHTTPClient(object):
    def __init__(
        self,
        session=requests.Session(),
        debug: bool = False,
        address: str = DefaultDirServerAddress,
        protocol: str = DefaultDirProtocolVersion,
    ):
        self.address = address
        self.protocol = protocol
        self.session = session
        self.debug = debug

    def apply(self, req: DirApplyRequest):
        if self.debug:
            print(f"DirServerHTTPClient.apply {req}")

        url = self.address + "/" + self.protocol + "/apply"
        return DirApplyResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )

    def list(self, req: DirListRequest):
        if self.debug:
            print(f"DirServerHTTPClient.list {req}")

        url = self.address + "/" + self.protocol + "/list"
        return DirListResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )


# make abstract class DirServer etc...
