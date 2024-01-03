# spinpy

The spin python package. Only Python 3.

```
pip install spinsrv
```

```python3
from spinsrv import spinfs
fs = spinfs.SpinFileSystem(config=spinfs.Config(public=<PUBLIC HERE>, private=<PRIVATE HERE>, citizen=<CITIZEN HERE>))
fs.ls("/")
```
