from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _bulk_update_metadata(AUTH_TOKEN, URL, CONTENT_IDS, COLLECTION_IDS, RELATED_CONTENT_IDS, 
                          TAG_IDS, SCHEMA_NAME, DEBUG):
    
    API_URL = f"{URL}/admin/content/bulk-metadata-update"

    # Create header for the request
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    BODY = {
        "contents": CONTENT_IDS,
        "collections": COLLECTION_IDS,
        "relatedContents": RELATED_CONTENT_IDS,
        "tags": TAG_IDS,
        "schemaName": SCHEMA_NAME
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST\nBODY: {json.dumps(BODY, indent= 4)}")

    try:
        # Send the request
        RESPONSE = requests.post(API_URL, headers= HEADERS, data= json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()
    
    except:
        _api_exception_handler(RESPONSE, "Bulk update metadata failed")