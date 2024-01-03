import dataclasses

import spinsrv._spin as spin

Alias = str


@dataclasses.dataclass
class Proxy:
    citizen: spin.Name = ""
    alias: Alias = ""

    @staticmethod
    def from_json(j: dict):
        p = Proxy()
        p.unmarshal_json(j)
        return p

    def unmarshal_json(self, j: dict):
        if "Citizen" in j:
            self.citizen = j["Citizen"]
        if "Alias" in j:
            self.alias = j["Alias"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Citizen"] = self.citizen
        j["Alias"] = self.alias
