import os

import spinsrv as spin

if "SPINPY_TEST_PUBLIC" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_PUBLIC environment variable")
if "SPINPY_TEST_PRIVATE" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_PRIVATE environment variable")
if "SPINPY_TEST_CITIZEN" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_CITIZEN environment variable")
SPINPY_TEST_PUBLIC = os.environ["SPINPY_TEST_PUBLIC"]
SPINPY_TEST_PRIVATE = os.environ["SPINPY_TEST_PRIVATE"]
SPINPY_TEST_CITIZEN = os.environ["SPINPY_TEST_CITIZEN"]

print("THIS IS SMOKE TEST 002: IT TESTS BASIC DATA LAYER FUNCTIONALITY")

bc = spin.data.BitServerHTTPClient()
resp = bc.ops(
    spin.data.BitOpsRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
    )
)
print(resp)
