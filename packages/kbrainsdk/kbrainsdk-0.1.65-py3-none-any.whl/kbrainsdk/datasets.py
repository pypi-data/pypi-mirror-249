from kbrainsdk.validation.datasets import validate_list_datasets, validate_search_datasets
from kbrainsdk.apibase import APIBase

class Datasets(APIBase):

    def list_datasets(self, email, token, client_id, oauth_secret, tenant_id):
        
        payload = {
            "email": email,
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_list_datasets(payload)

        path = f"/datasets/list/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def search_datasets(self, query, topic, citations, email, token, client_id, oauth_secret, tenant_id):
        
        payload = {
            "email": email,
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id,
            "query": query,
            "topic": topic,
            "citations": citations
        }

        validate_list_datasets(payload)
        validate_search_datasets(payload)

        path = f"/datasets/search/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response