import zenhelper
import os
import json

# Create zenodo instance
zen = zenhelper.depositions(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)
print(zen.list())

# Create new instance
new_depo = zen.create()

# Retrive deposition 
ret_depo = zen.retrieve(deposition=new_depo["id"])

# Create new instance for listing files
zen_files = zenhelper.deposition_files(deposition=new_depo["id"], access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)

# List files 
files = zen_files.list()
print(files)

# Cleanup
zen.delete(deposition=new_depo["id"])
