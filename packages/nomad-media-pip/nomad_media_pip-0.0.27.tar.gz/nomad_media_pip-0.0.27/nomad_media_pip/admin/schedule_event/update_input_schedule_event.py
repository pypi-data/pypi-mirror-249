from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.admin.schedule_event.event_types import _EVENT_TYPES
from nomad_media_pip.admin.schedule_event.get_input_schedule_event import _get_input_schedule_event

import requests, json

def _update_input_schedule_event(AUTH_TOKEN, URL, ID, CHANNEL_ID, INPUT, BACKUP_INPUT,
                                 FIXED_ON_AIR_TIME_UTC, DEBUG):
    
    API_URL = f"{URL}/liveChannel/{CHANNEL_ID}/liveScheduleEvent/{ID}"

    SCHEDULE_EVENT_INFO = _get_input_schedule_event(AUTH_TOKEN, URL, CHANNEL_ID,
                                                    ID, DEBUG)
    
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    BODY = {
        "type": {
            "id": _EVENT_TYPES["liveInput"],
            "description": "Live Input"
        }
    }

    BODY['id'] = ID if ID and ID != SCHEDULE_EVENT_INFO['id'] else SCHEDULE_EVENT_INFO['id']
    BODY['channelId'] = CHANNEL_ID if CHANNEL_ID and CHANNEL_ID != SCHEDULE_EVENT_INFO['channelId'] else SCHEDULE_EVENT_INFO['channelId']
    BODY['liveInput'] = INPUT if INPUT and INPUT != SCHEDULE_EVENT_INFO['input'] else SCHEDULE_EVENT_INFO['input']
    BODY['liveInput2'] = BACKUP_INPUT if BACKUP_INPUT and BACKUP_INPUT != SCHEDULE_EVENT_INFO['backupInput'] else SCHEDULE_EVENT_INFO['backupInput']
    BODY['fixedOnAirTimeUTC'] = FIXED_ON_AIR_TIME_UTC if FIXED_ON_AIR_TIME_UTC and FIXED_ON_AIR_TIME_UTC != SCHEDULE_EVENT_INFO['fixedOnAirTimeUTC'] else SCHEDULE_EVENT_INFO['fixedOnAirTimeUTC']

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: PUT,\nBODY: {json.dumps(BODY, indent=4)}")

    try:
        RESPONSE = requests.put(API_URL, headers= HEADERS, data= json.dumps(BODY))
        
        if not RESPONSE.ok:
            raise Exception()
    except:
        _api_exception_handler(RESPONSE, "Update Input Schedule Event Failed")