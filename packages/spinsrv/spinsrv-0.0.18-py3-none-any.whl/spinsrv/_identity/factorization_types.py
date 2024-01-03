import enum


class FactorizationType(enum.Enum):
    MissingFactorizationType = 0
    Dev1Factorization = 1
    Dev2Factorization = 2
    Dev3Factorization = 3
    NeedsAllFactors = 4
    NeedsAnyOneFactor = 5
