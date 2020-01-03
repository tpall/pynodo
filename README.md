# Zenapi

Python wrapper for Zenodo API.

## Install

Clone this repo and cd to this directory. Package can be installed with:

```python
pip install .
```

## Usage

### Working with depositions

```python
import zenapi
import os
import json

# Create zenodo (sandbox) instance
zen = zenapi.Depositions(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)

# List user depositions
depos = zen.list(params={"size": 50})

# Create a new deposition with some metadata
data = {
    "metadata": {
        "title": "My first upload",
        "upload_type": "poster",
        "description": "This is my first upload",
        "creators": [{"name": "Päll, Taavi", "affiliation": "UT"}],
    }
}
new_depo = zen.create(data=data)

# Retrieve deposition info
ret_depo = zen.retrieve(deposition=new_depo["id"])

# Update deposition metadata
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
updated_depo = zen.update(deposition=new_depo["id"], data=updates)

# Delete deposition
zen.delete(new_depo["id"])
```

### Working with deposition files

```python
import zenapi
import os
import json

# Create zenodo (sandbox) instance
zen = zenapi.Depositions(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)

# Create new deposition
new_depo = zen.create()

# Retrive deposition
ret_depo = zen.retrieve(deposition=new_depo["id"])

# Create new instance for listing files
zen_files = zenapi.DepositionFiles(
    deposition=new_depo["id"],
    access_token=os.environ["ZENODO_SANDBOX_PAT"],
    sandbox=True,
)

# Upload file (second argument with new file name is optional)
zen_files.upload("tests/upload.txt", "uploaded_file.txt")

# List files in deposition
files = zen_files.files

# Download file from deposition (second argument with download folder is optional)
zen_files.download("uploaded_file.txt", "tmp")
```
