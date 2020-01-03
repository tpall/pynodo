import zenapi
import os
import json

# Create zenodo instance
zen = zenapi.Depositions(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)

# Create new instance
new_depo = zen.create()

# Retrive deposition 
ret_depo = zen.retrieve(deposition=new_depo["id"])

# Create new instance for listing files
zen_files = zenapi.DepositionFiles(deposition=new_depo["id"], access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)

# Upload file
zen_files.upload("tests/upload.txt", "uploaded_file.txt")

# List files 
files = zen_files.files

# Download file
zen_files.download("uploaded_file.txt", "tmp")

# Cleanup
zen.delete(deposition=new_depo["id"])
