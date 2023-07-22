from streamlit.connections import ExperimentalBaseConnection
import os
import requests
import streamlit as st
import json
import py7zr


class PinataConnection(ExperimentalBaseConnection[requests.Session]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._resource = self._connect(**kwargs)

    def _connect(self, **kwargs) -> requests.Session:
        session = requests.Session()

        if 'jwt' in kwargs:
            jwt = kwargs.pop('jwt')
        elif 'jwt' in self._secrets:
            jwt = self._secrets['jwt']
        else:
            jwt = None

        if jwt is not None:
            session.headers.update({
                'Authorization': f'Bearer {jwt}',
            })
        else:
            if 'api_key' in kwargs and 'secret_api_key' in kwargs:
                api_key = kwargs.pop('api_key')
                secret_api_key = kwargs.pop('secret_api_key')
            elif 'api_key' in self._secrets and 'secret_api_key' in self._secrets:
                api_key = self._secrets['api_key']
                secret_api_key = self._secrets['secret_api_key']
            else:
                api_key = None
                secret_api_key = None

            if api_key is not None and secret_api_key is not None:
                session.headers.update({
                    'pinata_api_key': str(api_key),
                    'pinata_secret_api_key': str(secret_api_key),
                })
            else:
                raise ValueError("Missing authentication details. Please provide either a JWT token or API keys.")

        return session

    def cursor(self):
        return self._resource

    def upload_file(self, file, custom_key_values=None):
        with self._resource as s:
            pinata_metadata = {
                "name": file.name,
            }
            if custom_key_values is not None:
                pinata_metadata["keyvalues"] = custom_key_values

            response = s.post(
                'https://api.pinata.cloud/pinning/pinFileToIPFS',
                files={'file': file.read()},
                data={
                    'pinataOptions': '{"cidVersion": 1}',
                    'pinataMetadata': json.dumps(pinata_metadata)
                },
            )
        return response.json()

    def upload_directory(self, directory_path, custom_key_values=None):
        # Create a 7z file from the directory
        with py7zr.SevenZipFile("temp.7z", 'w') as archive:
            archive.writeall(directory_path, 'base')

        with self._resource as s:
            with open("temp.7z", "rb") as f:
                pinata_metadata = {
                    "name": os.path.basename(directory_path),
                }
                if custom_key_values is not None:
                    pinata_metadata["keyvalues"] = custom_key_values

                response = s.post(
                    'https://api.pinata.cloud/pinning/pinFileToIPFS',
                    files={'file': f.read()},
                    data={
                        'pinataOptions': '{"cidVersion": 1}',
                        'pinataMetadata': json.dumps(pinata_metadata)
                    },
                )
        # Remove the temporary 7z file
        os.remove("temp.7z")

        return response.json()

    def pin_by_cid(self, cid, name="cid_content", custom_key_values=None):
        payload = {
            "hashToPin": cid,
            "pinataMetadata": {
                "name": name,
                "keyvalues": custom_key_values if custom_key_values else {}
            }
        }
        with self._resource as s:
            response = s.post(
                'https://api.pinata.cloud/pinning/pinByHash',
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
        return response.json()

    def pin_by_json(self, content, name="json_content", custom_key_values=None):
        payload = {
            "pinataOptions": {
                "cidVersion": 1
            },
            "pinataMetadata": {
                "name": name,
                "keyvalues": custom_key_values if custom_key_values else {}
            },
            "pinataContent": content
        }
        with self._resource as s:
            response = s.post(
                'https://api.pinata.cloud/pinning/pinJSONToIPFS',
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
        return response.json()

    def update_metadata(self, ipfs_pin_hash, name=None, keyvalues=None):
        payload = {
            "ipfsPinHash": ipfs_pin_hash,
        }
        if name is not None:
            payload["name"] = name
        if keyvalues is not None:
            payload["keyvalues"] = keyvalues

        with self._resource as s:
            response = s.put(
                'https://api.pinata.cloud/pinning/hashMetadata',
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
        if response.status_code == 200:
            return {"success": True}
        else:
            return {"success": False, "status_code": response.status_code}

    def query(self, status=None, hash_contains=None, page_limit=1000, ttl: int = 3600):
        @st.cache_data(ttl=ttl)
        def _get_pins(_status, _hash_contains, _page_limit):
            params = {
                'pageLimit': _page_limit,
            }
            if _status is not None:
                params['status'] = _status
            if _hash_contains is not None:
                params['hashContains'] = _hash_contains

            with self._resource as s:
                response = s.get(
                    'https://api.pinata.cloud/data/pinList',
                    params=params
                )
            return response.json()

        return _get_pins(status, hash_contains, page_limit)

    def list_by_jobs(self, status=None, ipfs_pin_hash=None, limit=1000, offset=0, sort='ASC', ttl: int = 3600):
        @st.cache_data(ttl=ttl)
        def _list_by_jobs(_status, _ipfs_pin_hash, _limit, _offset, _sort):
            params = {
                'sort': _sort,
                'limit': _limit,
                'offset': _offset
            }
            if _status is not None:
                params['status'] = _status
            if _ipfs_pin_hash is not None:
                params['ipfs_pin_hash'] = _ipfs_pin_hash

            with self._resource as s:
                response = s.get(
                    'https://api.pinata.cloud/pinning/pinJobs',
                    params=params
                )
            return response.json()

        return _list_by_jobs(status, ipfs_pin_hash, limit, offset, sort)

    def unpin(self, ipfs_hash):
        with self._resource as s:
            response = s.delete(
                f'https://api.pinata.cloud/pinning/unpin/{ipfs_hash}'
            )
        if response.status_code == 200:
            return {"success": True}
        else:
            return {"success": False, "status_code": response.status_code}

    def data_usage(self):
        with self._resource as s:
            response = s.get('https://api.pinata.cloud/data/userPinnedDataTotal')
        return response.json()
