import enum


class LicenseType(enum.Enum):
    MissingLicenseType = 0
    Dev1License = 1
    Dev2License = 2
    Dev3License = 3
    InheritLicense = 4
    ReplaceLicense = 5
    OpaqueLicense = 6
