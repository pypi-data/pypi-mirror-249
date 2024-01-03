from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler

import json, requests

def _media_search(AUTH_TOKEN, URL, SEARCH_QUERY, IDS, FIELD_NAME, 
                 SORT_ORDER, DEBUG):

    API_URL = f"{URL}/media/search"
        
    # Create header for the request
    HEADERS = {
  	    "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    # Build the payload BODY
    BODY = {  
        "searchQuery": SEARCH_QUERY,
        "ids": IDS, 
        "sortFields": [  
            {  
                "fieldName": FIELD_NAME,
                "sortType": SORT_ORDER  
            }  
        ]  
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
        _api_exception_handler(RESPONSE, "Media search failed")

