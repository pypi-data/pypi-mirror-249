import enum


class PermissionGrantType(enum.Enum):
    MissingPermissionGrantType = 0
    Dev1PermissionGrant = 1
    Dev2PermissionGrant = 2
    Dev3PermissionGrant = 3
    InherentGrant = 4
    OpaqueGrant = 5
    IdentityGrant = 11
    AliasPathGrant = 12
