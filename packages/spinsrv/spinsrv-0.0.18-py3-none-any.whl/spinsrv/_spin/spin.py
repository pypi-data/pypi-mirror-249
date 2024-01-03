import uuid

"""
    Name represents a spin name.
"""
Name = str


"""
    UUID is a universal unique identifier.
"""
UUID = uuid.UUID

Error = str

ErrNotImplemented: Error = "not implemented"
ErrInternal: Error = "internal"
ErrNotFound: Error = "not found"
ErrExpired: Error = "expired"
ErrNotVerified: Error = "not verified"
ErrNotAuthorized: Error = "not authorized"


def error_from_string(s: str) -> Error:
    if s == ErrNotImplemented:
        return ErrNotImplemented
    elif s == ErrInternal:
        return ErrInternal
    elif s == ErrNotFound:
        return ErrNotFound
    elif s == ErrExpired:
        return ErrExpired
    elif s == ErrNotVerified:
        return ErrNotVerified
    elif s == ErrNotAuthorized:
        return ErrNotAuthorized
    else:
        return Error(s)
