__author__ = "Taavi Päll"
__copyright__ = "Copyright 2020, Taavi Päll"
__email__ = "tapa741@gmail.com"
__license__ = "MIT"

import os
import hashlib
from collections import namedtuple
import requests
import json
from requests.exceptions import HTTPError


ZenFileInfo = namedtuple("ZenFileInfo", ["checksum", "filesize", "id", "download"])


class zenodo:
    """
    Zenodo personal access token must be passed in as 'access_token' argument.
    Separate registration and access token is needed for Zenodo sandbox
    environment at https://sandbox.zenodo.org.
    """

    def __init__(self, *args, access_token, **kwargs):
        self._access_token = access_token
        if "sandbox" in kwargs:
            self._sandbox = kwargs.pop("sandbox")
        else:
            self._sandbox = False

        if self._sandbox:
            self._baseurl = "https://sandbox.zenodo.org"
        else:
            self._baseurl = "https://zenodo.org"

        # Check if access token is valid
        try:
            self.try_access()
        except Exception as e:
            print(
                "The Zenodo server could not verify that you are authorized to access your resources. You supplied the wrong credentials (e.g. a bad access_token): {}".format(
                    e
                )
            )

        if "deposition" in kwargs:
            self.deposition = kwargs.pop("deposition")
            self.bucket = self.get_bucket()

    def _api_request(
        self,
        url,
        method="GET",
        headers={},
        params=None,
        data=None,
        files=None,
        json=False,
    ):

        # Create a session with a hook to raise error on bad request.
        session = requests.Session()
        session.hooks = {"response": lambda r, *args, **kwargs: r.raise_for_status()}
        session.headers["Authorization"] = "Bearer {}".format(self._access_token)
        session.headers.update(headers)

        # Run query.
        r = session.request(
            method=method, url=url, params=params, data=data, files=files
        )
        if json:
            msg = r.json()
            return msg
        else:
            return r

    def try_access(self):
        return self._api_request(self._baseurl + "/api/deposit/depositions", json=True,)

    def get_bucket(self):
        resp = self._api_request(
            self._baseurl + "/api/deposit/depositions/{}".format(self.deposition),
            headers={"Content-Type": "application/json"},
            json=True,
        )
        return resp["links"]["bucket"]

    def get_files(self):
        files = self._api_request(
            self._baseurl + "/api/deposit/depositions/{}/files".format(self.deposition),
            headers={"Content-Type": "application/json"},
            json=True,
        )
        return {
            os.path.basename(f["filename"]): ZenFileInfo(
                f["checksum"], int(f["filesize"]), f["id"], f["links"]["download"]
            )
            for f in files
        }

    def _stats(self):
        return self.get_files()[os.path.basename(self.local_file())]

    def exists(self):
        return os.path.basename(self.local_file()) in self.get_files()

    def size(self):
        if self.exists():
            return self._stats().filesize
        else:
            return self._iofile.size_local


class depositions(zenodo):
    def __init__(self, *args, access_token, **kwargs):

        zenodo.__init__(self, *args, access_token=access_token, **kwargs)

        # else:
        #     # Creating a new deposition, as deposition id was not supplied.
        #     self.deposition, self.bucket = self.create_deposition().values()

    def list(self, params=None):
        return self._api_request(
            self._baseurl + "/api/deposit/depositions", params=params, json=True,
        )

    def create(self, data={}):
        resp = self._api_request(
            self._baseurl + "/api/deposit/depositions",
            method="POST",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
            json=True,
        )
        return {
            "id": resp["id"],
            "title": resp["title"],
            "bucket": resp["links"]["bucket"],
        }

    def retrieve(self, deposition=None):
        try:
            if deposition is not None:
                d = deposition
            else:
                d = self.deposition
        except AttributeError as e:
            return "You need to supply deposition id: {}".format(e)
        return self._api_request(
            self._baseurl + "/api/deposit/depositions/{}".format(d), json=True,
        )

    def update(self, data, deposition=None):
        try:
            if deposition is not None:
                d = deposition
            else:
                d = self.deposition
        except AttributeError as e:
            return "You need to supply deposition id: {}".format(e)
        return self._api_request(
            self._baseurl + "/api/deposit/depositions/{}".format(d),
            method="PUT",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
            json=True,
        )

    def delete(self, deposition=None):
        try:
            if deposition is not None:
                d = deposition
            else:
                d = self.deposition
        except AttributeError as e:
            return "You need to supply deposition id: {}".format(e)
        resp = self._api_request(
            self._baseurl + "/api/deposit/depositions/{}".format(d), method="DELETE",
        )
        return resp.status_code

    def download(self):
        stats = self._stats()
        download_url = stats.download
        r = self._api_request(download_url)

        local_md5 = hashlib.md5()

        # Download file.
        with open(self.local_file(), "wb") as rf:
            for chunk in r.iter_content(chunk_size=1024 * 1024 * 10):
                local_md5.update(chunk)
                rf.write(chunk)
        local_md5 = local_md5.hexdigest()

        if local_md5 != stats.checksum:
            raise AssertionError(
                "File checksums do not match for remote file id: {}".format(stats.id)
            )

    def upload(self):
        with open(self.local_file(), "rb") as lf:
            self._api_request(
                self.bucket + "/{}".format(os.path.basename(self.remote_file())),
                method="PUT",
                data=lf,
            )

    # @property
    # def list(self):
    #     return [i for i in self.get_files()]

    # @property
    # def name(self):
    #     return self.local_file()
