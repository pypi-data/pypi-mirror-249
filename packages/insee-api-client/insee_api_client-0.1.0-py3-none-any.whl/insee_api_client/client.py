from base64 import b64encode

import requests as rq

from insee_api_client import utils, resources

class Client:
    BASE_URL = 'https://api.insee.fr'
    API_TYPE_TO_VERSION = {
        'sirene': 'V3'
    }

    def __init__(self, api_key, api_secret, token=None, api_type_to_version={}):
        access_token = token if token else self._generate_token(api_key, api_secret)
        self._session = rq.Session()
        self._session.headers = {
            'Authorization': f"Bearer {access_token}"
        }

        self.api_type_to_version = {
            **self.API_TYPE_TO_VERSION,
            **api_type_to_version
        }

        self._resources = {
            'sirene': resources.SirenePool(
                utils.urljoin(
                    self.BASE_URL, 
                    self.api_type_to_base_path.get('sirene')
                ), self._session
            )
        }

    @property
    def api_type_to_base_path(self):
        return {
            'sirene': f"entreprises/sirene/{self.api_type_to_version.get('sirene')}"
        }

    def _generate_token(self, api_key, api_secret):
        auth_url = utils.urljoin(
            self.BASE_URL, 'token'
        )
        encoded_auth = b64encode(
            f"{api_key}:{api_secret}".encode()
        ).decode()

        res_auth = rq.post(
            auth_url,
            headers={'Authorization': f"Basic {encoded_auth}"},
            data={'grant_type': 'client_credentials'}
        )
        if res_auth.status_code != 200:
            raise ValueError(
                f'Error during authentication: {res_auth.status_code} - {res_auth.text}'
            )
        
        return res_auth.json().get('access_token')
    
    @property
    def resources(self):
        return self._resources
    
    @property
    def sirene(self):
        return self._resources['sirene']