import dataclasses
import requests
import typing


import spinsrv._spin as spin
from spinsrv._identity.keys import Key, PrivateKey
from spinsrv._identity.factor_server import (
    FactorChallengeResponse,
    FactorVerifyResponse,
)


@dataclasses.dataclass
class KeyAuthRequestFactor:
    public: str = ""
    private: str = ""

    @staticmethod
    def from_json(j: dict):
        f = KeyAuthRequestFactor()
        f.unmarshal_json(j)
        return f

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        return j


@dataclasses.dataclass
class KeyAuthRequest:
    nonce: str = ""
    public: str = ""
    private: str = ""
    factors: list[KeyAuthRequestFactor] = dataclasses.field(default_factory=list)
    duration: int = 0  # microseconds
    derived_name: str = ""
    derived_alias: str = ""
    derived_type: int = 0
    derived_data: str = ""

    @staticmethod
    def from_json(j: dict):
        r = KeyAuthRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Nonce" in j:
            self.nonce = j["Nonce"]
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]
        if "Factors" in j and j["Factors"] is not None:
            self.blocks = [KeyAuthRequestFactor.from_json(f) for f in j["Factors"]]
        if "Duration" in j:
            self.duration = j["Duration"]
        if "DerivedName" in j:
            self.derived_name = j["DerivedName"]
        if "DerivedAlias" in j:
            self.derived_alias = j["DerivedAlias"]
        if "DerivedType" in j:
            self.derived_type = j["DerivedType"]
        if "DerivedData" in j:
            self.derived_data = j["DerivedData"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Nonce"] = self.nonce
        j["Public"] = self.public
        j["Private"] = self.private
        j["Factors"] = [f.to_json() for f in self.factors]
        j["Duration"] = self.duration
        j["DerivedName"] = self.derived_name
        j["DerivedAlias"] = self.derived_alias
        j["DerivedType"] = self.derived_type
        j["DerivedData"] = self.derived_data
        return j


@dataclasses.dataclass
class KeyAuthResponse:
    nonce: str = ""
    handled_at: spin.Time = 0
    key_verified: bool = False
    key: typing.Optional[Key] = None
    derived: typing.Optional[PrivateKey] = None
    factor_challenges: list[FactorChallengeResponse] = dataclasses.field(
        default_factory=list
    )
    factor_verifies: list[FactorVerifyResponse] = dataclasses.field(
        default_factory=list
    )
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        print(j)
        r = KeyAuthResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Nonce" in j:
            self.nonce = j["Nonce"]
        if "HandledAt" in j:
            self.handled_at = j["HandledAt"]
        if "KeyVerified" in j:
            self.key_verified = j["KeyVerified"]
        if "Key" in j and j["Key"] is not None:
            self.key = Key.from_json(j["Key"])
        if "Derived" in j and j["Derived"] is not None:
            print("here")
            self.derived = PrivateKey.from_json(j["Derived"])
        if "FactorChallenges" in j and j["FactorChallenges"] is not None:
            self.factor_challenges = [
                FactorChallengeResponse.from_json(f) for f in j["FactorChallenges"]
            ]
        if "FactorVerifies" in j and j["FactorVerifies"] is not None:
            self.factor_verifies = [
                FactorVerifyResponse.from_json(f) for f in j["FactorVerifies"]
            ]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Nonce"] = self.nonce
        j["HandledAt"] = self.handled_at
        j["KeyVerified"] = self.key_verified
        j["Key"] = self.key.to_json()
        j["Derived"] = self.derived.to_json()
        j["FactorChallenges"] = [f.to_json() for f in self.factor_challenges]
        j["FactorVerifies"] = [f.to_json() for f in self.factor_verifies]
        j["Error"] = self.error
        return j


DefaultKeyProtocolVersion = "v0.0.0"
DefaultKeyServerAddress = "https://keys-ddh4amviaq-uw.a.run.app"


class KeyServerHTTPClient(object):
    def __init__(
        self,
        session=requests.Session(),
        debug: bool = False,
        address: str = DefaultKeyServerAddress,
        protocol: str = DefaultKeyProtocolVersion,
    ):
        self.address = address
        self.protocol = protocol
        self.session = session
        self.debug = debug

    def auth(self, req: KeyAuthRequest) -> KeyAuthResponse:
        if self.debug:
            print(f"KeyServerHTTPClient.auth {req}")

        url = self.address + "/" + self.protocol + "/auth"
        return KeyAuthResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )
