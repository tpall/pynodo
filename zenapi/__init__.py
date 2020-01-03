__author__ = "Taavi Päll"
__copyright__ = "Copyright 2020, Taavi Päll"
__email__ = "tapa741@gmail.com"
__license__ = "MIT"

import os
import hashlib
import requests
import json
from collections import namedtuple
from abc import ABCMeta, abstractmethod

ZenDepoInfo = namedtuple("ZenDepoInfo", "id title bucket")
ZenFileInfo = namedtuple("ZenFileInfo", "checksum filesize id download")


class Zenodo(metaclass=ABCMeta):
    """
    Zenodo personal access token must be passed in as 'access_token' argument.
    Separate registration and access token is needed for Zenodo sandbox
    environment at https://sandbox.zenodo.org.
    """

    @abstractmethod
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
        self._path = "/api/deposit/depositions"
        self._application_json = {"Content-Type": "application/json"}
        self._missing_deposition_id_error = "You need to supply deposition id: {}"

        # Check if access token is valid
        try:
            self._try_access
        except Exception as e:
            print(
                "The Zenodo server could not verify that you are authorized to access your resources. You supplied the wrong credentials (e.g. a bad access_token): {}".format(
                    e
                )
            )

        if "deposition" in kwargs:
            self.deposition = kwargs.pop("deposition")

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

    @property
    def _try_access(self):
        return self._api_request(self._baseurl + self._path, json=True)


class Depositions(Zenodo):
    def __init__(self, *args, access_token, **kwargs):

        super().__init__(self, *args, access_token=access_token, **kwargs)

    def list(self, params=None):
        return self._api_request(self._baseurl + self._path, params=params, json=True)

    def create(self, data={}):
        resp = self._api_request(
            self._baseurl + self._path,
            method="POST",
            headers=self._application_json,
            data=json.dumps(data),
            json=True,
        )
        return ZenDepoInfo(resp["id"], resp["title"], resp["links"]["bucket"])

    def retrieve(self, deposition=None):
        try:
            if deposition is not None:
                d = deposition
            else:
                d = self.deposition
        except AttributeError as e:
            return self._missing_deposition_id_error.format(e)
        return self._api_request(
            self._baseurl + self._path + "/{}".format(d), json=True
        )

    def update(self, data, deposition=None):
        try:
            if deposition is not None:
                d = deposition
            else:
                d = self.deposition
        except AttributeError as e:
            return self._missing_deposition_id_error.format(e)
        return self._api_request(
            self._baseurl + self._path + "/{}".format(d),
            method="PUT",
            headers=self._application_json,
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
            return self._missing_deposition_id_error.format(e)
        resp = self._api_request(
            self._baseurl + self._path + "/{}".format(d), method="DELETE"
        )
        return resp.status_code


class DepositionFiles(Depositions):
    def __init__(self, *args, access_token, **kwargs):

        super().__init__(self, *args, access_token=access_token, **kwargs)

    def list(self):
        resp = self._api_request(
            self._baseurl + self._path + "/{}/files".format(self.deposition),
            headers=self._application_json,
            json=True,
        )
        return {
            os.path.basename(f["filename"]): ZenFileInfo(
                f["checksum"], int(f["filesize"]), f["id"], f["links"]["download"]
            )
            for f in resp
        }

    def upload(self, local_file, remote_file=None):
        if remote_file is None:
            remote_file = local_file
        with open(local_file, "rb") as h:
            self._api_request(
                self.bucket + "/{}".format(os.path.basename(remote_file)),
                method="PUT",
                data=h,
            )

    def download(self, remote_file, dest="."):
        fileinfo = self.files[remote_file]
        r = self._api_request(fileinfo.download)

        local_md5 = hashlib.md5()

        # Download file.
        with open(os.path.join(dest, remote_file), "wb") as rf:
            for chunk in r.iter_content(chunk_size=1024 * 1024 * 10):
                local_md5.update(chunk)
                rf.write(chunk)
        local_md5 = local_md5.hexdigest()

        if local_md5 != fileinfo.checksum:
            raise AssertionError(
                "File checksums do not match for remote file: {} with id: {}".format(
                    remote_file, fileinfo.id
                )
            )

    def delete(self, remote_file):
        fileinfo = self.files[remote_file]
        resp = self._api_request(
            self._baseurl
            + self._path
            + "/{}/files/{}".format(self.deposition, fileinfo.id),
            method="DELETE",
        )
        return resp.status_code

    @property
    def files(self):
        return self.list()

    @property
    def bucket(self):
        return self.retrieve()["links"]["bucket"]
