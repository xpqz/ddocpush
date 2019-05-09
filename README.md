# ddocpush

Very basic tools for managing CouchDB design documents to enable proper versioning.

## mkddoc

`usage: mkddoc sourcedir destdir`

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
    ddoc1.json
    ddoc2.json
    ...
```

## pushddoc

`usage: pushddoc https://account.cloudant.com/database sourcedir`

Iterate over the json ddocs produced by `mkddoc` and upload those
to the server under `database`.

Expects to find credentials in the following environment variables:

```text
COUCHDB_USER
COUCHDB_PW
```