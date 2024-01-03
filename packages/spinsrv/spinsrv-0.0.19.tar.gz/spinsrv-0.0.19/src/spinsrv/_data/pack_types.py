import enum


class PackType(enum.Enum):
    MissingPackType = 0
    Dev1Pack = 1
    Dev2Pack = 2
    Dev3Pack = 3
    PlainPack = 4
    SHA256Pack = 5
    RSAWrapAESPack = 6
    OpaquePack = 7
