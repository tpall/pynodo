
![](https://github.com/tpall/pynodo/workflows/CI/badge.svg)[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=tpall_zenapi&metric=alert_status)](https://sonarcloud.io/dashboard?id=tpall_zenapi)

# Pynodo -- manage your Zenodo depositions

Python wrapper for Zenodo REST API for working with Zenodo depositions and files.

## Installation

```python
pip install pynodo
```

## Usage

[Zenodo](https://zenodo.org) access token with write scope is necessary to access depositions and files.
Separate token is neccessary for [zenodo sandbox](https://sandbox.zenodo.org) environment.
Sandbox can be switched by setting `sandbox=True` when initiating *pynodo* instance.

- Depositions can be accessed using *pynodo.Depositions* class. 

- Files in a deposition can be accessed using *pynodo.DepositionFiles* class.

- *Depositions.create* and *DepositionFiles.files* return namedtuple and list of namedtuples, respectively.
Other functions return either json response or status code (delete).

- Actions (e.g. publish, new version, edit) are not implemented.

### Working with Depositions

pynodo allows listing, creating, retrieving, updating and deleting of depostions.

- Create zenodo (sandbox) instance

```python
import pynodo
import os

zen = pynodo.Depositions(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)
```

- List user depositions

```python
depos = zen.list(params={"size": 50})
```

- Create a new deposition with some metadata

```python
data = {
    "metadata": {
        "title": "My first upload",
        "upload_type": "poster",
        "description": "This is my first upload",
        "creators": [{"name": "Päll, Taavi", "affiliation": "UT"}],
    }
}
new_depo = zen.create(data=data)
```

- Retrieve deposition info

```python
ret_depo = zen.retrieve(deposition=new_depo.id)
```

- Update deposition metadata

```python
updates = {
    "metadata": {
        "title": "Modified upload",
        "upload_type": "dataset",
        "description": "This is updated upload",
        "creators": [
            {"name": "Päll, Taavi", "affiliation": "UT"},
            {"name": "Sus, Scrofa", "affiliation": "Mets"},
        ],
    }
}
updated_depo = zen.update(deposition=new_depo.id, data=updates)
```

- Delete deposition (status code 204 shows success)

```python
zen.delete(new_depo.id)
```

### Working with DepositionFiles

pynodo allows listing, uploading, downloading and deleting of files in a deposition.

- Create zenodo (sandbox) instance

```python
import pynodo
import os
zen = pynodo.Depositions(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)
```

- Create new deposition

```python
new_depo = zen.create()
```

- Retrive deposition

```python
ret_depo = zen.retrieve(deposition=new_depo.id)
```

- Create new instance for listing files

```python
zen_files = pynodo.DepositionFiles(
    deposition=new_depo.id,
    access_token=os.environ["ZENODO_SANDBOX_PAT"],
    sandbox=True,
)
```

- Upload file (second argument with new file name is optional)

```python
zen_files.upload("tests/upload.txt", "uploaded_file.txt")
```

- List files in deposition

```python
files = zen_files.files
```

- Download file from deposition (second argument with download folder is optional)

```python
zen_files.download("uploaded_file.txt", "tmp")
```

- Delete file (status code 204 shows success)

```python
zen_files.delete("uploaded_file.txt")
```
