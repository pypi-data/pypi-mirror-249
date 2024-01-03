from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _copy_asset(AUTH_TOKEN, URL, ASSET_ID, BATCH_ACTION, CONTENT_DEFINITION_ID, SCHEMA_NAME,
                TARGET_IDS, USER_ID, ACTION_ARGUMENTS, RESOLVER_EXCEMPT, DEBUG):

    API_URL = f"{URL}/admin/asset/{ASSET_ID}/copy"

    HEADERS = {
        "Content-Type": "application/json",
      	"Authorization": "Bearer " + AUTH_TOKEN
    }

    BODY = {
        "batchAction": BATCH_ACTION,
        "contentDefinitionId": CONTENT_DEFINITION_ID,
        "schemaName": SCHEMA_NAME,
        "targetIds": TARGET_IDS,
        "userId": USER_ID,
        "actionArguments": ACTION_ARGUMENTS,
        "resolverExempt": RESOLVER_EXCEMPT
    }

    if DEBUG:
        print(f"URL: {API_URL}\nMETHOD: POST\nBODY: {json.dumps(BODY, indent=4)}")

    try:
        RESPONSE = requests.post(API_URL, headers=HEADERS, data=json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()
        
        return RESPONSE.json()
    
    except:
        _api_exception_handler(RESPONSE, "Copy asset failed")