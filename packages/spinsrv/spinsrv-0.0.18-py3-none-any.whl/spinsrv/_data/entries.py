import dataclasses

import spinsrv._spin as spin
import spinsrv._identity as identity
from spinsrv._data.entry_blocks import EntryBlock
from spinsrv._data.entry_versions import EntryVersion
from spinsrv._data.entry_types import EntryType
from spinsrv._data.licenses import License
from spinsrv._data.pack_types import PackType


@dataclasses.dataclass
class Entry:
    citizen: spin.Name = ""
    path: spin.Path = ""
    version: EntryVersion = dataclasses.field(default_factory=EntryVersion)
    created_at: spin.Time = 0
    updated_at: spin.Time = 0
    created_by: identity.Proxy = dataclasses.field(default_factory=identity.Proxy)
    updated_by: identity.Proxy = dataclasses.field(default_factory=identity.Proxy)
    time: spin.Time = 0
    type: EntryType = EntryType.MissingEntryType
    pack_type: PackType = PackType.MissingPackType
    pack_data: str = ""
    blocks: list[EntryBlock] = dataclasses.field(default_factory=list)
    license: License = dataclasses.field(default_factory=License)

    @staticmethod
    def from_json(j: dict):
        e = Entry()
        e.unmarshal_json(j)
        return e

    def unmarshal_json(self, j: dict):
        if "Citizen" in j:
            self.citizen = j["Citizen"]
        if "Path" in j:
            self.path = j["Path"]
        if "Version" in j:
            self.version = j["Version"]
        if "CreatedAt" in j:
            self.created_at = j["CreatedAt"]
        if "UpdatedAt" in j:
            self.updated_at = j["UpdatedAt"]
        if "CreatedBy" in j:
            self.created_by = identity.Proxy.from_json(j["CreatedBy"])
        if "UpdatedBy" in j:
            self.updated_by = identity.Proxy.from_json(j["UpdatedBy"])
        if "Time" in j:
            self.time = j["Time"]
        if "Type" in j:
            self.type = EntryType(j["Type"])
        if "PackType" in j:
            self.pack_type = PackType(j["PackType"])
        if "PackData" in j:
            self.pack_data = j["PackData"]
        if "Blocks" in j and j["Blocks"] is not None:
            self.blocks = [EntryBlock.from_json(block) for block in j["Blocks"]]
        if "License" in j:
            self.license = License.from_json(j["License"])

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Citizen"] = self.citizen
        j["Path"] = self.path
        j["Version"] = self.version
        j["CreatedAt"] = self.created_at
        j["UpdatedAt"] = self.updated_at
        j["CreatedBy"] = self.created_by.to_json()
        j["UpdatedBy"] = self.updated_by.to_json()
        j["Time"] = self.time
        j["Type"] = self.type.value
        j["PackType"] = self.pack_type.value
        j["PackData"] = self.pack_data
        j["Blocks"] = [block.to_json() for block in self.blocks]
        j["License"] = self.license.to_json()
