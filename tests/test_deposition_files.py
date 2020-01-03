import zenapi
import os

# Create zenodo instance
zen = zenapi.Depositions(access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True)

# Create new instance
new_depo = zen.create()

# Retrive deposition
ret_depo = zen.retrieve(deposition=new_depo.id)

# Create new instance for listing files
zen_files = zenapi.DepositionFiles(
    deposition=new_depo.id, access_token=os.environ["ZENODO_SANDBOX_PAT"], sandbox=True
)

UPLOADED = "uploaded_file.txt"

# Upload file
zen_files.upload("tests/upload.txt", UPLOADED)

# List files
print(zen_files.files)


# Download file
zen_files.download(UPLOADED, "tests")

# Delete file
zen_files.delete(UPLOADED)
print(zen_files.files)

# Cleanup
zen.delete(deposition=new_depo.id)
