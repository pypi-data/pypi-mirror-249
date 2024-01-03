import dataclasses

import spinsrv._spin as spin
from spinsrv._data.entry_blocks import BlockAddress, BlockReference


@dataclasses.dataclass
class StoreRef:
    address: BlockAddress = ""
    reference: BlockReference = ""
    volatile: bool = False
    expires_at: spin.Time = 0

    @staticmethod
    def from_json(j: dict):
        r = StoreRef()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Address" in j:
            self.address = j["Address"]
        if "Reference" in j:
            self.reference = j["Reference"]
        if "Volatile" in j:
            self.volatile = j["Volatile"]
        if "ExpiresAt" in j:
            self.expires_at = j["ExpiresAt"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Address"] = self.address
        j["Reference"] = self.reference
        j["Volatile"] = self.volatile
        j["ExpiresAt"] = self.expires_at
