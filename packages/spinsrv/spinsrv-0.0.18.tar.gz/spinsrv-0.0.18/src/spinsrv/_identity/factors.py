import dataclasses

import spinsrv._spin as spin
from spinsrv._identity.factor_types import FactorType


@dataclasses.dataclass
class Factor:
    name: spin.Name = ""
    type: FactorType = FactorType.MissingFactorType
    data: str = ""

    @staticmethod
    def from_json(j: dict) -> "Factor":
        k = Factor()
        k.unmarshal_json(j)
        return k

    def unmarshal_json(self, j: dict):
        if "Name" in j:
            self.name = j["Name"]
        if "Type" in j:
            self.type = FactorType(j["Type"])
        if "Data" in j:
            self.data = j["Data"]

    def to_json(self) -> dict:
        j: dict = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Name"] = self.name
        j["Type"] = self.type
        j["Data"] = self.data
