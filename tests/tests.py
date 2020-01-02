import zenhelper
import os
import json

zen = zenhelper.depositions(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)
depos = zen.list(params={"size": 20})
for d in depos:
    print("title:{}, id: {}".format(d["title"], d["id"]))
    zen.delete(d["id"])

data = {"metadata": {"title": "My first upload", "upload_type": "poster", "description": "This is my first upload", "creators": [{"name": "Päll, Taavi", "affiliation": "UT"}]}}
new_depo = zen.create(data=data)
print(new_depo)

ret_depo = zen.retrieve()
print(ret_depo)

ret_depo = zen.retrieve(deposition=new_depo["id"])
print(ret_depo)

updates = {"metadata": {"title": "Modified upload", "upload_type": "dataset", "description": "This is updated upload", "creators": [{"name": "Päll, Taavi", "affiliation": "UT"}, {"name": "Sus, Scrofa", "affiliation": "Mets"}]}}
updated_depo = zen.update(deposition=new_depo["id"], data=updates)
print(updated_depo)

