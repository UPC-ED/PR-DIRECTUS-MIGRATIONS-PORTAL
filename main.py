import requests
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
 
load_dotenv()

class APICMSService:
    def __init__(self) -> None:
        self.url =APICMSService.get_url_cms()

    def api_response(self, url: str) -> Dict[str, Any]:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    def get_data_from_table(self, table: str) -> List[Dict[str, Any]]:
        url = self.url + f"/items/{table}"
        records = self.api_response(url)['data']
        return records

    def get_data_from_file(self, file_code: str) -> List[Dict[str, Any]]:
        url = self.url + f"/files/{file_code}"
        records = self.api_response(url)['data']
        return records   
    
    def get_data_from_users(self) -> List[Dict[str, Any]]:
        url = self.url + f"/users"
        records = self.api_response(url)['data']
        return records


def extract_directus_collections(data_coleccions,stage):
    list_coleccions = []
    for coleccion in data_coleccions:
        if coleccion["meta"].get("group") and stage in coleccion["meta"].get("group"):
            list_coleccions.append(coleccion["collection"])
    return list_coleccions


if __name__ == "__main__":
    url_1 = os.environ.get("PORTAL_1")
    response_1 = requests.get( url_1 + "/collections" )
    data_coleccions_1 = response_1.json()["data"]
    list_coleccions_1 = extract_directus_collections(data_coleccions_1,"pregrado_programa_")

    url_2 = os.environ.get("PORTAL_2")
    response_2 = requests.get( url_2 + "/collections" )
    data_coleccions_2 = response_2.json()["data"]
    list_coleccions_2 = extract_directus_collections(data_coleccions_2,"epe_programa_")

    for coleccion in list_coleccions_1[-10:]:
        response_coleccions = requests.get( url_1 + "/items/" + coleccion).json()["data"]
        response_coleccions_ = []
        for response_coleccion in response_coleccions:
            response_coleccion.pop("id")
            response_coleccion.pop("date_updated")
            response_coleccions_.append(response_coleccion)
