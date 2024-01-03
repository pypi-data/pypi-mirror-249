import dataclasses

import spinsrv._spin as spin
from spinsrv._identity.aliases import Proxy
from spinsrv._data.license_types import LicenseType
from spinsrv._data.permission_grants import PermissionGrant
from spinsrv._data.permissions import Permissions


@dataclasses.dataclass
class License:
    type: LicenseType = LicenseType.MissingLicenseType
    grants: list[PermissionGrant] = dataclasses.field(default_factory=list)
    created_at: spin.Time = 0
    updated_at: spin.Time = 0
    created_by: Proxy = dataclasses.field(default_factory=Proxy)
    updated_by: Proxy = dataclasses.field(default_factory=Proxy)
    caller_permissions: Permissions = 0

    @staticmethod
    def from_json(j: dict):
        r = License()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Type" in j:
            self.type = LicenseType(j["Type"])
        if "Grants" in j and j["Grants"] is not None:
            self.grants = [PermissionGrant.from_json(grant) for grant in j["Grants"]]
        if "CreatedAt" in j:
            self.created_at = j["CreatedAt"]
        if "UpdatedAt" in j:
            self.updated_at = j["UpdatedAt"]
        if "CreatedBy" in j:
            self.created_by = Proxy.from_json(j["CreatedBy"])
        if "UpdatedBy" in j:
            self.updated_by = Proxy.from_json(j["UpdatedBy"])
        if "CallerPermissions" in j:
            self.caller_permissions = j["CallerPermissions"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Type"] = self.type.value
        j["Grants"] = [grant.to_json() for grant in self.grants]
        j["CreatedAt"] = self.created_at
        j["UpdatedAt"] = self.updated_at
        j["CreatedBy"] = self.created_by.to_json()
        j["UpdatedBy"] = self.updated_by.to_json()
        j["CallerPermissions"] = self.caller_permissions
