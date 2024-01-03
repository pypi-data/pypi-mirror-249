import os

import spinsrv as spin
from spinsrv import identity
from spinsrv import data

if "SPINPY_TEST_PUBLIC" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_PUBLIC environment variable")
if "SPINPY_TEST_PRIVATE" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_PRIVATE environment variable")
if "SPINPY_TEST_CITIZEN" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_CITIZEN environment variable")
SPINPY_TEST_PUBLIC = os.environ["SPINPY_TEST_PUBLIC"]
SPINPY_TEST_PRIVATE = os.environ["SPINPY_TEST_PRIVATE"]
SPINPY_TEST_CITIZEN = os.environ["SPINPY_TEST_CITIZEN"]

print("THIS IS SMOKE TEST 1: IT TESTS THE CLIENTS IN src/spin/spinpy.py")

kc = identity.KeyServerHTTPClient()
resp = kc.auth(
    identity.KeyAuthRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        duration=600,
    )
)
print(resp)

dc = data.DirServerHTTPClient()
resp = dc.list(
    data.DirListRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        citizen=SPINPY_TEST_CITIZEN,
        path="/",
        level=0,
    )
)
print(resp)
resp = dc.list(
    data.DirListRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        citizen=SPINPY_TEST_CITIZEN,
        path="/",
        level=1,
    )
)
print(resp)

resp = dc.apply(
    data.DirApplyRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        ops=[
            data.DirOp(
                type=data.PutDirOp,
                entry=data.Entry(
                    type=data.DirectoryEntry,
                    citizen=SPINPY_TEST_CITIZEN,
                    path="/test",
                    version=data.IgnoreVersion,
                ),
            )
        ],
    )
)
print(resp)

bc = data.BitServerHTTPClient()
bs = "Asdf".encode()
resp = bc.ops(
    data.BitOpsRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        ops=[
            data.BitOp(
                type=data.PutBitOp,
                address=data.AnyAddress,
                reference=spin.SHA256(bs),
                bytes=bs,
            )
        ],
    )
)
print(resp)
