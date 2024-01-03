import base64
import dataclasses
import enum

from spinsrv._data.entry_blocks import BlockAddress, BlockReference
from spinsrv._data.store import StoreRef


class BitOpType(enum.Enum):
    MissingBitOpType = 0
    Dev1BitOp = 1
    Dev2BitOp = 2
    Dev3BitOp = 3
    GetBitOp = 4
    PutBitOp = 5
    DelBitOp = 6
    HashBitOp = 7


@dataclasses.dataclass
class BitOp:
    type: BitOpType = BitOpType.MissingBitOpType
    address: BlockAddress = ""
    reference: BlockReference = ""
    bytes: bytes = b""

    @staticmethod
    def from_json(j: dict):
        o = BitOp()
        o.unmarshal_json(j)
        return o

    def unmarshal_json(self, j: dict):
        if "Type" in j:
            self.type = BitOpType(j["Type"])
        if "Address" in j:
            self.address = j["Address"]
        if "Reference" in j:
            self.reference = j["Reference"]
        if "Bytes" in j and j["Bytes"] is not None:
            self.bytes = base64.b64decode(j["Bytes"])

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Type"] = self.type.value
        j["Address"] = self.address
        j["Reference"] = self.reference
        j["Bytes"] = base64.b64encode(self.bytes).decode()


@dataclasses.dataclass
class BitOpOutcome:
    store_ref: StoreRef = dataclasses.field(default_factory=StoreRef)
    bytes: bytes = b""
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        o = BitOpOutcome()
        o.unmarshal_json(j)
        return o

    def unmarshal_json(self, j: dict):
        if "StoreRef" in j:
            self.store_ref = StoreRef.from_json(j["StoreRef"])
        if "Bytes" in j and j["Bytes"] is not None:
            self.bytes = base64.b64decode(j["Bytes"])
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["StoreRef"] = self.store_ref.to_json()
        j["Bytes"] = base64.b64encode(self.bytes).decode()
        j["Error"] = self.error
