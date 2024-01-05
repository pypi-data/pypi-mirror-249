from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.common.asset.get_annotations import _get_annotations

import requests, json

def _update_annotation(AUTH_TOKEN, URL, ASSET_ID, ANNOTATION_ID, START_TIME_CODE, 
                       END_TIME_CODE, FIRST_KEYWORD, SECOND_KEYWORD, DESCRIPTION, COUNTRY,
                       CONTENT_ID, IMAGE_URL, DEBUG):
    
    API_URL = f"{URL}/asset/{ASSET_ID}/annotation/{ANNOTATION_ID}"

    HEADERS = {
        "Content-Type": "application/json",
      	"Authorization": "Bearer " + AUTH_TOKEN
    }

    ASSET_ANNOTATIONS = _get_annotations(AUTH_TOKEN, URL, ASSET_ID, DEBUG)
    ANNOTATION = next((annotation for annotation in ASSET_ANNOTATIONS if annotation["id"] == ANNOTATION_ID), None)

    BODY = {
        "id": ANNOTATION_ID,
        "startTimecode": START_TIME_CODE or ANNOTATION["startTimecode"],
        "endTimecode": END_TIME_CODE or ANNOTATION["endTimecode"],
        "properties": {
            "firstKeyword": FIRST_KEYWORD or ANNOTATION["properties"]["firstKeyword"],
            "secondKeyword": SECOND_KEYWORD or ANNOTATION["properties"]["secondKeyword"],
            "description": DESCRIPTION or ANNOTATION["properties"]["description"],
            "country": COUNTRY or ANNOTATION["properties"]["country"]
        },
        "contentId": CONTENT_ID or ANNOTATION["contentId"],
        "imageUrl": IMAGE_URL or ANNOTATION["imageUrl"]
    }

    if DEBUG:
        print(f"URL: {API_URL}\nMETHOD: PUT\nBODY: {json.dumps(BODY, indent=4)}")

    try:
        RESPONSE = requests.put(API_URL, headers=HEADERS, data=json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()
        
        return RESPONSE.json()
    
    except:
        _api_exception_handler(RESPONSE, "Update annotation failed")
                       