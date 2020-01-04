import zenapi
import os
import pytest
import hashlib

# Should fail: calling base class
def test_zenapi_zenodo():
    with pytest.raises(Exception):
        zenapi.Zenodo(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)


# Creating zenodo (sandbox) depositions instance for tests
@pytest.fixture(scope="module")
def depositions_object():
    return zenapi.Depositions(
        access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True
    )


# Create test deposition
@pytest.fixture(scope="module")
def test_deposition(depositions_object):
    data = {
        "metadata": {
            "title": "Test",
            "upload_type": "poster",
            "description": "This is test upload",
            "creators": [{"name": "Sus, scofa", "affiliation": "Forest Inc."}],
        }
    }
    return depositions_object.create(data=data)


# Create a new deposition with some metadata
def test_depositions_create(test_deposition):
    resp = test_deposition
    assert "Test" in resp


# List user depositions
def test_depositions_list(depositions_object):
    resp = depositions_object.list(params={"size": 1})
    assert len(resp) == 1


# Testing deposition retrieve
def test_depositions_retrieve(depositions_object, test_deposition):
    resp = depositions_object.retrieve(test_deposition.id)
    assert resp["id"] == test_deposition.id


# Update deposition metadata
def test_depositions_update(depositions_object, test_deposition):
    updates = {
        "metadata": {
            "title": "Modified upload",
            "upload_type": "dataset",
            "description": "This is updated upload",
            "creators": [{"name": "Felis, Catus", "affiliation": "Sofa"}],
        }
    }
    resp = depositions_object.update(deposition=test_deposition.id, data=updates)
    assert resp["title"] == "Modified upload"


# Create new instance for listing files
@pytest.fixture(scope="module")
def deposition_files_object(test_deposition):
    return zenapi.DepositionFiles(
        deposition=test_deposition.id,
        access_token=os.environ["ZENODO_SANDBOX_PAT"],
        sandbox=True,
    )


LOCAL = "tests/upload.txt"
UPLOADED = "uploaded_file.txt"
DOWNLOADED = "tests/uploaded_file.txt"


def md5(file):
    local_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            local_md5.update(chunk)
    return local_md5.hexdigest()


# Upload file
def test_file_upload(deposition_files_object):
    deposition_files_object.upload(LOCAL, UPLOADED)
    assert deposition_files_object.files[UPLOADED].checksum == md5(LOCAL)


# Download file
def test_file_download(deposition_files_object):
    deposition_files_object.download(UPLOADED, "tests")
    assert deposition_files_object.files[UPLOADED].checksum == md5(DOWNLOADED)


# Testing file delete
def test_file_delete(deposition_files_object):
    resp = deposition_files_object.delete(UPLOADED)
    assert resp == 204


# Testing deposition delete
def test_depositions_delete(depositions_object, test_deposition):
    resp = depositions_object.delete(test_deposition.id)
    assert resp == 204
