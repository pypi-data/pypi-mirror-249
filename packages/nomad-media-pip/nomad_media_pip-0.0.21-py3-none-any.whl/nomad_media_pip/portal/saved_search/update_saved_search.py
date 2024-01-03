from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.portal.saved_search.get_saved_search import _get_saved_search

import requests, json

def _update_saved_search(AUTH_TOKEN, URL, ID, NAME, FEATURED, BOOKMARKED, PUBLIC, SEQUENCE, 
                         TYPE, QUERY, OFFSET, SIZE, FILTERS, SORT_FIELDS, 
                         SEARCH_RESULT_FIELDS, SIMILAR_ASSET_ID, MIN_SCORE, 
                         EXCLUDE_TOTAL_RECORD_COUNT, FILTER_BINDER, DEBUG):
    
    API_URL = f"{URL}/portal/savedsearch/{ID}"

    HEADERS = {
        "Content-Type": "application/json",
      	"Authorization": "Bearer " + AUTH_TOKEN
    }

    SAVED_SEARCH_INFO = _get_saved_search(AUTH_TOKEN, URL, ID, DEBUG)

    BODY = {
        "name": NAME or SAVED_SEARCH_INFO["name"],
        "featured": FEATURED or SAVED_SEARCH_INFO["featured"],
        "bookmarked": BOOKMARKED or SAVED_SEARCH_INFO["bookmarked"],
        "public": PUBLIC or SAVED_SEARCH_INFO["public"],
        "pageSize": SIZE or SAVED_SEARCH_INFO["pageSize"],
        "sequence": SEQUENCE or SAVED_SEARCH_INFO["sequence"],
        "type": TYPE or SAVED_SEARCH_INFO["type"],
        "user": SAVED_SEARCH_INFO["user"],
        "criteria": {
            "query": QUERY or SAVED_SEARCH_INFO["criteria"]["query"],
            "pageOffset": OFFSET or SAVED_SEARCH_INFO["criteria"]["pageOffset"],
            "pageSize": SIZE or SAVED_SEARCH_INFO["criteria"]["pageSize"],
            "filters": FILTERS or SAVED_SEARCH_INFO["criteria"]["filters"],
            "sortFields": SORT_FIELDS or SAVED_SEARCH_INFO["criteria"]["sortFields"],
            "searchResultFields": SEARCH_RESULT_FIELDS or SAVED_SEARCH_INFO["criteria"]["searchResultFields"],
            "similarAssetId": SIMILAR_ASSET_ID or SAVED_SEARCH_INFO["criteria"]["similarAssetId"],
            "minScore": MIN_SCORE or SAVED_SEARCH_INFO["criteria"]["minScore"],
            "excludeTotalRecordCount": EXCLUDE_TOTAL_RECORD_COUNT or SAVED_SEARCH_INFO["criteria"]["excludeTotalRecordCount"],
            "filterBinder": FILTER_BINDER or SAVED_SEARCH_INFO["criteria"]["filterBinder"]
        }
    }

    if DEBUG:
        print(f"URL: {API_URL}\nMETHOD: POST\nBODY: {json.dumps(BODY, indent=4)}")

    try:
        RESPONSE = requests.post(API_URL, headers=HEADERS, data=json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()
        
        return RESPONSE.json()
    
    except:
        _api_exception_handler(RESPONSE, "Add saved search failed")