import hashlib

__all__ = ["spin", "identity", "data", "SHA256", "client"]

# ruff: noqa: F401
import spinsrv._spin as spin


# ruff: noqa: F401
import spinsrv._identity as identity

# ruff: noqa: F401
import spinsrv._data as data

# ruff: noqa: F401
import spinsrv._data._client as client

# SHA256 creates a sum of the data
def SHA256(b: bytes):
    m = hashlib.sha256()
    m.update(b)
    return m.hexdigest()
