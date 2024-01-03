# Xray Uploader

## usage

looks like this:
```
from xray.uploader import Uploader

xml = "res.xml"
summary = "automation test"
project_id = "12345"

Uploader(xml, summary, project_id, safe_mode=True)
```
