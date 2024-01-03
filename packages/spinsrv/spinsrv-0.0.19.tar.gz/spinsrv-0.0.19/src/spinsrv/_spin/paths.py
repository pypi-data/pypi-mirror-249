"""
    Path represents a spin path.
"""
Path = str


def path_ancestors(p: Path) -> list[Path]:
    if p == "":
        raise Exception("path_ancestors given empty path")
    if p == "/":
        return []
    rest = p[1:]
    # count number of slashes
    c = p.count("/")
    ancestors = [""] * c
    for i in range(1, c):
        j = rest.find("/")
        ancestors[i] = ancestors[i - 1] + "/" + rest[:j]  # exclude ending slash
        rest = rest[j + 1 :]  # exclude leading slash
    ancestors[0] = "/"
    return ancestors


def path_is_ancestor(a: Path, p: Path) -> bool:
    return p != a and p.startswith(a)


_root_sequence = ["/"]


def path_sequence(p: Path) -> list[Path]:
    if p == "":
        raise Exception("path_sequence given empty path")
    if p == "/":
        return _root_sequence
    ancestors = path_ancestors(p)
    ancestors.append(p)
    return ancestors
