import zenapi
import os
import json
import pytest

# Should fail
def test_zenapi_zenodo():
    with pytest.raises(Exception):
        zenapi.Zenodo(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)


# Test creating zenodo (sandbox) instance
@pytest.fixture
def depositions_object():
    return zenapi.Depositions(
        access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True
    )


# Create a new deposition with some metadata
def test_depositions_create(depositions_object):
    data = {
        "metadata": {
            "title": "Test",
            "upload_type": "poster",
            "description": "This is test upload",
            "creators": [{"name": "Sus, scofa", "affiliation": "Forest Inc."}],
        }
    }
    resp = depositions_object.create(data=data)
    assert "Test" in resp


# List user depositions
def test_depositions_list(depositions_object):
    resp = depositions_object.list(params={"size": 1})
    assert len(resp) == 1


# Create test deposition
@pytest.fixture
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


# Testing deposition delete
def test_depositions_delete(depositions_object, test_deposition):
    resp = depositions_object.delete(test_deposition.id)
    assert resp == 204


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
