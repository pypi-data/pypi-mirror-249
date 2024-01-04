from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler

import requests
from urllib.parse import urlencode

def _clear_continue_watching(AUTH_TOKEN, URL, USER_ID, ASSET_ID, DEBUG):

    API_URL = f"{URL}/account/clear-watching"

    PARAMS = {
        "userId": USER_ID,
        "assetId": ASSET_ID
    }

    API_URL = f"{API_URL}?{urlencode(PARAMS)}"

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + AUTH_TOKEN 
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST")

    try:
        RESPONSE = requests.post(API_URL, headers=HEADERS)
        if not RESPONSE.ok:
            raise Exception()
    
    except:
        _api_exception_handler(RESPONSE, "Clear Continue Watching Failed")      