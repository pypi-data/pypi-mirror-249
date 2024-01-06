and-otp-uri
===========

Parses backups from the [andOTP-Android app](https://github.com/andOTP/andOTP)
and turns the entries into otpauth-URIs understood by other authenticator apps.

With the `--generate-pass-entries` option you can directly create pass entries
from the backup.


Installation
------------

```
pip install and-otp-uri
```


Usage:
------

To print out URIs for the entries in the backup run

```bash
and-otp-uri /path/to/backup.json
```

See `and-otp-uri --help` for all available options.
