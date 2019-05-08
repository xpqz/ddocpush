# ddocpush

Very basic tools for managing CouchDB design documents to enable proper versioning.

## mkddoc.py

`usage: mkddoc.py sourcedir destdir`

Read through the `sourcedir`, and expecting a structure like

```text
sourcedir/
    ddoc1/
        view1/
            map.js
            reduce.js
        view2/
            map.js
            reduce.js
    ddoc2/
        ...
```

creating json documents under `destdir`:

```text
destdir/
    ddoc1-view1.json
    ddoc1-view2.json
    ...
```

## pushddoc.py

`usage: pushddoc.py https://account.cloudant.com/database sourcedir`

Iterate over the json ddocs produced by `mkddoc.py` and upload those
to the server under `database`.

Expects to find credentials in the following environment variables:

```text
COUCHDB_USER
COUCHDB_PW
```