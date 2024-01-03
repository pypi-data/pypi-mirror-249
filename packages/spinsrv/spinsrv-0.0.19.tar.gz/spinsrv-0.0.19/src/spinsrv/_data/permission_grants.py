import dataclasses
import typing
import uuid

import spinsrv._spin as spin
from spinsrv._data.permission_grant_types import PermissionGrantType
from spinsrv._data.permissions import Permissions
from spinsrv._identity.aliases import Proxy


@dataclasses.dataclass
class PermissionGrant:
    uuid: typing.Union[spin.UUID, None] = None
    path: spin.Path = ""
    type: PermissionGrantType = PermissionGrantType.MissingPermissionGrantType
    identity: Proxy = dataclasses.field(default_factory=Proxy)
    permissions: Permissions = 0
    expires_at: spin.Time = 0
    created_at: spin.Time = 0
    created_by: Proxy = dataclasses.field(default_factory=Proxy)

    @staticmethod
    def from_json(j: dict):
        g = PermissionGrant()
        g.unmarshal_json(j)
        return g

    def unmarshal_json(self, j: dict):
        if "UUID" in j:
            self.uuid = uuid.UUID(j["UUID"])
        if "Path" in j:
            self.path = j["Path"]
        if "Type" in j:
            self.type = PermissionGrantType(j["Type"])
        if "Identity" in j:
            self.identity = Proxy.from_json(j["Identity"])
        if "Permissions" in j:
            self.permissions = j["Permissions"]
        if "ExpiresAt" in j:
            self.expires_at = j["ExpiresAt"]
        if "CreatedAt" in j:
            self.created_at = j["CreatedAt"]
        if "CreatedBy" in j:
            self.created_by = Proxy.from_json(j["CreatedBy"])

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["UUID"] = str(self.uuid)
        j["Path"] = self.path
        j["Type"] = self.type.value
        j["Identity"] = self.identity.to_json()
        j["Permissions"] = self.permissions
        j["ExpiresAt"] = self.expires_at
        j["CreatedAt"] = self.created_at
        j["CreatedBy"] = self.created_by.to_json()
