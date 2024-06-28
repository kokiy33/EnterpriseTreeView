import json
import os
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv

from org_info.helper import remove_duplicates
from org_info.model import OrgInfo
from org_info.parser import BusyoParser

load_dotenv()

class PapattoAPIError(Exception):
    """Custom exception for Papatto API errors"""
    pass

class Papatto:
    BASE_URL = "https://www.papatto.info/papatto"
    LOGIN_URL = f"{BASE_URL}/index.php"
    ORG_CHART_URL = f"{BASE_URL}/orgChart.php"

    @staticmethod
    def get_org_infos(corp_number: str) -> List[OrgInfo]:
        raw_data = Papatto._fetch_raw_data(corp_number)
        
        bp = BusyoParser()
        org_infos = [
            bp.parse_busyo(busyo)
            for busyo in Papatto._convert_raw_data_to_list(raw_data)
        ]
        
        return remove_duplicates(org_infos)

    @staticmethod
    def _fetch_raw_data(corp_number: str) -> Dict[str, Any]:
        session = requests.Session()
        Papatto._login(session)
        return Papatto._fetch_org_chart(session, corp_number)

    @staticmethod
    def _login(session: requests.Session) -> None:
        data = {
            'uid': os.environ.get('PAPATTO_USERNAME'),
            'pswd': os.environ.get('PAPATTO_PASSWORD'),
        }
        response = session.post(Papatto.LOGIN_URL, data=data, allow_redirects=False)
        if not response.status_code in [200, 302]:
            raise PapattoAPIError(f"Failed to login to Papatto, Status code: {response.status_code}")

    @staticmethod
    def _fetch_org_chart(session: requests.Session, corp_number: str) -> Dict[str, Any]:
        params = {
            'shogonor': '*',
            'compno': corp_number,
        }
        response = session.get(Papatto.ORG_CHART_URL, params=params)
        if response.status_code != 200:
            raise PapattoAPIError("Failed to fetch organization chart data")
        
        try:
            return response.json()
        except json.JSONDecodeError:
            raise PapattoAPIError("Invalid JSON response from Papatto API")

    @staticmethod
    def _convert_raw_data_to_list(raw_data: Dict[str, Any]) -> List[str]:
        rows = []

        def serialize(dic: Dict[str, Any], parent_key: str = "") -> None:
            for key, value in dic.items():
                new_key = f"{parent_key};{key}" if parent_key else key

                if new_key not in rows:
                    rows.append(new_key)

                if isinstance(value, dict) and value:
                    serialize(value, new_key)

        serialize(raw_data["data"])
        return rows