from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler

import json, requests

def _create_form(AUTH_TOKEN, URL, ID, FIRST_NAME, LAST_NAME, ACTIVE, 
          START_DATE, LOOKUP_ID, DESCRIPTION, DEBUG):

    API_URL = f"{URL}/media/form/{ID}"
        
    # Create header for the request
    HEADERS = {
  	    "Authorization": "Bearer "+ AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    # Build the payload BODY
    BODY = {
        "firstName": FIRST_NAME,
        "lastName": LAST_NAME,
        "active": ACTIVE,
        "startDate": START_DATE,
        "state": {
            "lookupId": LOOKUP_ID,
            "description": DESCRIPTION
        }
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST\nBODY: {json.dumps(BODY, indent=4)}")

    try:
        # Send the request
        RESPONSE = requests.post(API_URL, headers= HEADERS, data= json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()

        return RESPONSE.json()

    except:
        _api_exception_handler(RESPONSE, "Forms failed")

