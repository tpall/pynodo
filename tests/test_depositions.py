import zenhelper
import os
import json

try:
    zen_base = zenhelper.Zenodo(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)
except Exception as e:
    print(e)

# Create zenodo (sandbox) instance 
zen = zenhelper.Depositions(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)

# List user depositions
depos = zen.list(params={"size": 50})
for d in depos:
    print("title:{}, id: {}".format(d["title"], d["id"]))
    zen.delete(d["id"])

# Create a new deposition with some metadata
data = {"metadata": {"title": "My first upload", "upload_type": "poster", "description": "This is my first upload", "creators": [{"name": "Päll, Taavi", "affiliation": "UT"}]}}
new_depo = zen.create(data=data)

# Should fail. Try to retrieve deposition info without deposition id
ret_depo = zen.retrieve()

# Retrieve deposition info
ret_depo = zen.retrieve(deposition=new_depo["id"])

# Update deposition metadata
updates = {"metadata": {"title": "Modified upload", "upload_type": "dataset", "description": "This is updated upload", "creators": [{"name": "Päll, Taavi", "affiliation": "UT"}, {"name": "Sus, Scrofa", "affiliation": "Mets"}]}}
updated_depo = zen.update(deposition=new_depo["id"], data=updates)
