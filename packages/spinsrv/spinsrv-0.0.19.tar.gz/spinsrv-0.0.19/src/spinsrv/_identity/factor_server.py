import dataclasses

import spinsrv._spin as spin


@dataclasses.dataclass
class FactorChallengeResponse:
    nonce: str = ""
    factor_name: spin.Name = ""
    expires_at: spin.Time = 0
    data: str = ""
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        f = FactorChallengeResponse()
        f.unmarshal_json(j)
        return f

    def unmarshal_json(self, j: dict):
        if "Nonce" in j:
            self.nonce = j["Nonce"]
        if "FactorName" in j:
            self.factor_name = j["FactorName"]
        if "ExpiresAt" in j:
            self.expires_at = j["ExpiresAt"]
        if "Data" in j:
            self.data = j["Data"]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Nonce"] = self.nonce
        j["FactorName"] = self.factor_name
        j["ExpiresAt"] = self.expires_at
        j["Data"] = self.data
        j["Error"] = self.error
        return j


@dataclasses.dataclass
class FactorVerifyResponse:
    none: str = ""
    factor_name: spin.Name = ""
    factor_verified: bool = False
    data: str = ""
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        f = FactorVerifyResponse()
        f.unmarshal_json(j)
        return f

    def unmarshal_json(self, j: dict):
        if "Nonce" in j:
            self.nonce = j["Nonce"]
        if "FactorName" in j:
            self.factor_name = j["FactorName"]
        if "FactorVerified" in j:
            self.factor_verified = j["FactorVerified"]
        if "Data" in j:
            self.data = j["Data"]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Nonce"] = self.nonce
        j["FactorName"] = self.factor_name
        j["FactorVerified"] = self.factor_verified
        j["Data"] = self.data
        j["Error"] = self.error
        return j
