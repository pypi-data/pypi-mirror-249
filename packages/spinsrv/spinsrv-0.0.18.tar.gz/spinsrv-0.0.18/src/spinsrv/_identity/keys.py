import dataclasses
import typing
import uuid

import spinsrv._spin as spin
from spinsrv._identity.key_types import KeyType
from spinsrv._identity.factorizations import Factorization


@dataclasses.dataclass
class Key:
    uuid: typing.Union[spin.UUID, None] = None
    created_at: spin.Time = 0
    expires_at: spin.Time = 0
    citizen: spin.Name = ""
    name: spin.Name = ""
    type: KeyType = KeyType.MissingKeyType
    data: str = ""
    parent: spin.Name = ""
    alias: spin.Name = ""
    factorization: Factorization = dataclasses.field(default_factory=Factorization)

    @staticmethod
    def from_json(j: dict) -> "Key":
        k = Key()
        k.unmarshal_json(j)
        return k

    def unmarshal_json(self, j: dict):
        if "UUID" in j:
            self.uuid = uuid.UUID(j["UUID"])
        if "CreatedAt" in j:
            self.created_at = j["CreatedAt"]
        if "ExpiresAt" in j:
            self.expires_at = j["ExpiresAt"]
        if "Citizen" in j:
            self.citizen = j["Citizen"]
        if "Name" in j:
            self.name = j["Name"]
        if "Type" in j:
            self.type = KeyType(j["Type"])
        if "Data" in j:
            self.data = j["Data"]
        if "Parent" in j:
            self.parent = j["Parent"]
        if "Alias" in j:
            self.alias = j["Alias"]
        if "Factorization" in j and j["Factorization"] is not None:
            self.factorization = Factorization.from_json(j["Factorization"])

    def to_json(self) -> dict:
        j: dict = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["UUID"] = str(self.uuid)
        j["CreatedAt"] = self.created_at
        j["ExpiresAt"] = self.expires_at
        j["Citizen"] = self.citizen
        j["Name"] = self.name
        j["Type"] = self.type
        j["Data"] = self.data
        j["Parent"] = self.parent
        j["Alias"] = self.alias
        j["Factorization"] = self.factorization.to_json()


@dataclasses.dataclass
class PrivateKey(Key):
    private: str = ""

    @staticmethod
    def from_json(j: dict) -> "PrivateKey":
        k = PrivateKey()
        k.unmarshal_json(j)
        return k

    def unmarshal_json(self, j: dict):
        super().unmarshal_json(j)
        if "Private" in j:
            self.private = j["Private"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        super().marshal_json(j)
        j["Private"] = self.private
