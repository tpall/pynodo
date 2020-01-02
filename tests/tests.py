import zenhelper
import os
import json

zen = zenhelper.depositions(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)
depos = zen.list()
for d in depos:
    print("title:{}, id: {}".format(d["title"], d["id"]))

data = '{"metadata": {"title": "My first upload", "upload_type": "poster", "description": "This is my first upload", "creators": [{"name": "Pall, Taavi", "affiliation": "UT"}]}}'
new_depo = zen.create(data=data)
print(new_depo)

ret_depo = zen.retrieve()
print(ret_depo)

ret_depo = zen.retrieve(deposition=new_depo["id"])
print(ret_depo)

data = {"metadata": {"upload_type": "dataset", "title": "Updated first upload"}}
