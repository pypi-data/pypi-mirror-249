import dataclasses
import spinsrv._spin as spin

BlockAddress = str
BlockReference = spin.Name

AnyAddress: BlockAddress = ""


@dataclasses.dataclass
class EntryBlock:
    address: BlockAddress = ""
    reference: BlockReference = ""
    offset: int = 0
    size: int = 0
    pack_data: str = ""

    @staticmethod
    def from_json(j: dict):
        e = EntryBlock()
        e.unmarshal_json(j)
        return e

    def unmarshal_json(self, j: dict):
        if "Address" in j:
            self.address = j["Address"]
        if "Reference" in j:
            self.reference = j["Reference"]
        if "Offset" in j:
            self.offset = j["Offset"]
        if "Size" in j:
            self.size = j["Size"]
        if "PackData" in j:
            self.pack_data = j["PackData"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Address"] = self.address
        j["Reference"] = self.reference
        j["Offset"] = self.offset
        j["Size"] = self.size
        j["PackData"] = self.pack_data
