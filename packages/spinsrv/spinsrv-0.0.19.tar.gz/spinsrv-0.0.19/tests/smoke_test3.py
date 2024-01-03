import os

from spinsrv import data, client

if "SPINPY_TEST_PUBLIC" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_PUBLIC environment variable")
if "SPINPY_TEST_PRIVATE" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_PRIVATE environment variable")
if "SPINPY_TEST_CITIZEN" not in os.environ:
    raise ValueError("must specify SPINPY_TEST_CITIZEN environment variable")
SPINPY_TEST_PUBLIC = os.environ["SPINPY_TEST_PUBLIC"]
SPINPY_TEST_PRIVATE = os.environ["SPINPY_TEST_PRIVATE"]
SPINPY_TEST_CITIZEN = os.environ["SPINPY_TEST_CITIZEN"]

print(
    "THIS IS SMOKE TEST 3: IT TESTS (primarily file related) \
    functionality of src/spin/spinfs.py"
)

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

f = fs.open("/notes.txt", "wb")
f.write(b"Hello world!")
f.close()
f = fs.open("/notes.txt", "rb")
b = f.read()
assert b == b"Hello world!", f"got {b}, wanted Hello world!"
