import enum


class FactorType(enum.Enum):
    MissingFactorType = 0
    Dev1Factor = 1
    Dev2Factor = 2
    Dev3Factor = 3
    BcryptPasswordFactor = 4
    RSAPublicKeyFactor = 5
    EmailCodeFactor = 6
    PhoneSMSCodeFactor = 7
