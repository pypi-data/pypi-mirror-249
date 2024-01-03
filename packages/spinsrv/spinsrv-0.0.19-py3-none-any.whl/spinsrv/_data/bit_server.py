import requests
import dataclasses

from spinsrv._data.bit_ops import BitOp, BitOpOutcome


@dataclasses.dataclass
class BitOpsRequest:
    public: str = ""
    private: str = ""
    ops: list[BitOp] = dataclasses.field(default_factory=list)

    @staticmethod
    def from_json(j: dict):
        r = BitOpsRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]
        if "Ops" in j and j["Ops"] is not None:
            self.ops = [BitOp.from_json(op) for op in j["Ops"]]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Ops"] = [op.to_json() for op in self.ops]


@dataclasses.dataclass
class BitOpsResponse:
    outcomes: list[BitOpOutcome] = dataclasses.field(default_factory=list)
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = BitOpsResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Outcomes" in j and j["Outcomes"] is not None:
            self.outcomes = [BitOpOutcome.from_json(op) for op in j["Outcomes"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Outcomes"] = [op.to_json() for op in self.outcomes]
        j["Error"] = self.error


DefaultBitProtocolVersion = "v0.0.0"
DefaultBitServerAddress = "https://store-ddh4amviaq-uw.a.run.app"


class BitServerHTTPClient(object):
    def __init__(
        self,
        session=requests.Session(),
        debug: bool = False,
        address: str = DefaultBitServerAddress,
        protocol: str = DefaultBitProtocolVersion,
    ):
        self.address = address
        self.protocol = protocol
        self.session = session
        self.debug = debug

    def ops(self, req: BitOpsRequest, address=None):
        if self.debug:
            print(f"BitServerHTTPClient.ops {req}")
        if address is None or address == "":
            address = self.address

        url = address + "/" + self.protocol + "/ops"
        resp = BitOpsResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )
        for out in resp.outcomes:  # TODO: hack
            if out.store_ref.address == "":
                out.store_ref.address = address
        return resp
