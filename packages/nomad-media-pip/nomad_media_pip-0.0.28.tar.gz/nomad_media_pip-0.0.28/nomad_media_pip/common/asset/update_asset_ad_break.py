from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _update_asset_ad_break(AUTH_TOKEN, URL, ASSET_ID, AD_BREAK_ID, TIME_CODE, TAGS, LABELS,
                           DEBUG):

    API_URL = f"{URL}/admin/asset/{ASSET_ID}/adbreak/{AD_BREAK_ID}"

    HEADERS = {
        "Content-Type": "application/json",
      	"Authorization": "Bearer " + AUTH_TOKEN
    }

    BODY = {
        "id": AD_BREAK_ID,
        "timecode": TIME_CODE,
        "tags": TAGS,
        "labels": LABELS
    }

    if DEBUG:
        print(f"URL: {API_URL}\nMETHOD: PUT\nBODY: {json.dumps(BODY, indent=4)}")

    try:
        RESPONSE = requests.put(API_URL, headers=HEADERS, data=json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()
        
        return RESPONSE.json()
    
    except:
        _api_exception_handler(RESPONSE, "Update ad break failed") 