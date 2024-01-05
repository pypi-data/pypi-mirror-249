from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.admin.schedule.get_schedule_item import _get_schedule_item

import requests, json

def _update_schedule_item_search_filter(AUTH_TOKEN, URL, ID, ITEM_ID, COLLECTIONS, DAYS, DURATION_TIME_CODE, END_SEARCH_DATE, END_SEARCH_DURATION_IN_MINUTES, END_TIME_CODE, RELATED_CONTENT, SEARCH_DATE, SEARCH_DURATION_IN_MINUTES, SEARCH_FILTER_TYPE, TAGS, TIME_CODE, DEBUG):

    API_URL = f"{URL}/admin/schedule/{ID}/item/{ITEM_ID}"

    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    SCHEDULE_ITEM = _get_schedule_item(AUTH_TOKEN, URL, ID, ITEM_ID, DEBUG)

    BODY = {
        "collections": COLLECTIONS or SCHEDULE_ITEM["collections"],
        "days": DAYS or SCHEDULE_ITEM["days"],
        "durationTimeCode": DURATION_TIME_CODE or SCHEDULE_ITEM["durationTimeCode"],
        "endSearchDate": END_SEARCH_DATE or SCHEDULE_ITEM["endSearchDate"],
        "endSearchDurationInMinutes": END_SEARCH_DURATION_IN_MINUTES or SCHEDULE_ITEM["endSearchDurationInMinutes"],
        "endTimeCode": END_TIME_CODE or SCHEDULE_ITEM["endTimeCode"],
        "relatedContent": RELATED_CONTENT or SCHEDULE_ITEM["relatedContent"],
        "scheduleItemType": "1",
        "searchDate": SEARCH_DATE or SCHEDULE_ITEM["searchDate"],
        "searchDurationInMinutes": SEARCH_DURATION_IN_MINUTES or SCHEDULE_ITEM["searchDurationInMinutes"],
        "searchFilterType": SEARCH_FILTER_TYPE or SCHEDULE_ITEM["searchFilterType"],
        "sourceType": "2",
        "tags": TAGS or SCHEDULE_ITEM["tags"],
        "timeCode": TIME_CODE or SCHEDULE_ITEM["timeCode"]
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: PUT,\nBODY: {json.dumps(BODY, indent=4)}")

    try:
        RESPONSE = requests.put(API_URL, headers= HEADERS, data= json.dumps(BODY))
        
        if not RESPONSE.ok:
            raise Exception()
    except:
        _api_exception_handler(RESPONSE, "Update Schedule Item Search Filter Failed")