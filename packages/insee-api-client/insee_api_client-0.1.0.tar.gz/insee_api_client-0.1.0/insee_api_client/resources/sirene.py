from insee_api_client.utils import urljoin
from insee_api_client.resources import base

class SireneSirenPool(
    base.ResourcePool,
    base.ListableResource,
    base.CreatableResource,
    base.GettableResource
):
    @property
    def non_diffusibles(self):
        return base.QueryPool(
            urljoin(self._endpoint, 'nonDiffusibles'),
            self._session
        )

    @property
    def refus_immatriculation_rcs(self):
        return base.QueryPool(
            urljoin(self._endpoint, 'refusImmatriculationRcs'),
            self._session
        )

class SireneSiretPool(
    base.ResourcePool,
    base.ListableResource,
    base.CreatableResource,
    base.GettableResource    
):
    @property
    def liens_succession(self):
        return base.QueryPool(
            urljoin(self._endpoint, 'liensSuccession'),
            self._session
        )

    @property
    def non_diffusibles(self):
        return base.QueryPool(
            urljoin(self._endpoint, 'nonDiffusibles'),
            self._session
        )        

class SirenePool(
    base.ResourcePool
):
    @property
    def siren(self):
        return SireneSirenPool(
            urljoin(self._endpoint, 'siren'),
            self._session            
        )
    
    @property
    def siret(self):
        return SireneSiretPool(
            urljoin(self._endpoint, 'siret'),
            self._session            
        )
    
    @property
    def informations(self):
        return base.QueryPool(
            urljoin(self._endpoint, 'informations'),
            self._session
        )       