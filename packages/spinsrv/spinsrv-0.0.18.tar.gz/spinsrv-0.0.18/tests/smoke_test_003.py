import os

from spinsrv import client, data

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


c = client.Client(
    client.Options(
        public=SPINPY_TEST_PUBLIC,
        private=SPINPY_TEST_PRIVATE,
        citizen=SPINPY_TEST_CITIZEN,
        dir_server=data.DirServerHTTPClient(),
        bit_server=data.BitServerHTTPClient(),
    )
)

fs = c.namespace(SPINPY_TEST_CITIZEN).fs()

out = fs.ls("/", detail=False)
print(out)

out2 = fs.ls("/", detail=False)

if out != out2:
    raise ValueError(f"out != out2, {out} != {out2}")
