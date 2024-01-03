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

print("THIS IS SMOKE TEST 1: IT TESTS BASIC IDENTITY LAYER FUNCTIONALITY")

kc = spin.identity.KeyServerHTTPClient()
resp = kc.auth(
    spin.identity.KeyAuthRequest(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
    )
)
print(resp)
