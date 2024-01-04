from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.helpers.slugify import _slugify

import requests, json

def _create_and_update_event(AUTH_TOKEN, URL, CONTENT_ID, CONTENT_DEFINITION_ID, NAME, SERIES,
                             START_DATETIME, END_DATETIME, PRIMARY_PERFORMER, 
                             SHORT_DESCRIPTION, LONG_DESCRIPTION, THUMBNAIL_IMAGE, HERO_IMAGE, 
                             LOGO_IMAGE, INTELLIGENT_PROGRAM, EXTERNAL_URL, VENUE, PERFORMERS, 
                             GENRES, MEDIA_ATTRIBUTES, LANGUAGES, PRODUCTS, FEATURED_GROUPS, 
                             GROUP_SEQUENCE, RELATED_MEDIA_ITEMS, RECOMMENDED_SIMILAR_ITEMS, 
                             CONTENT_RATINGS, IS_DISABLED, LIVE_CHANNEL, DEBUG):
    
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    if (CONTENT_ID == ""):
        API_URL = f"{URL}/content/new?contentDefinitionId={CONTENT_DEFINITION_ID}"

        if DEBUG:
            print(f"URL: {API_URL},\nMETHOD: GET")

        try:
            RESPONSE = requests.get(API_URL, headers= HEADERS)

            if not RESPONSE.ok:
                raise Exception()

            INFO = RESPONSE.json()
            CONTENT_ID = INFO["contentId"]
        except:
            _api_exception_handler(RESPONSE, "Create Event Failed")

    API_URL = f"{URL}/content/{CONTENT_ID}"

    BODY = {
        "contentId": CONTENT_ID,
        "contentDefinitionId": CONTENT_DEFINITION_ID,
        "properties": {
            "contentRatings": CONTENT_RATINGS,
            "disabled": IS_DISABLED if IS_DISABLED is not None else False,
            "endDate": END_DATETIME,
            "externalUrl": EXTERNAL_URL,
            "featuredGroups": FEATURED_GROUPS if FEATURED_GROUPS is not None else [],
            "genres": GENRES if GENRES is not None else [],
            "groupSequence": GROUP_SEQUENCE,
            "heroImage": HERO_IMAGE,
            "intelligentProgram": INTELLIGENT_PROGRAM,
            "languages": LANGUAGES if LANGUAGES is not None else [],
            "liveChannel": LIVE_CHANNEL,
            "logoImage": LOGO_IMAGE,
            "longDescription": LONG_DESCRIPTION,
            "mediaAttributes": MEDIA_ATTRIBUTES if MEDIA_ATTRIBUTES is not None else [],
            "name": NAME,
            "performers": PERFORMERS if PERFORMERS is not None else [],
            "primaryPerformer": PRIMARY_PERFORMER,
            "products": PRODUCTS if PRODUCTS is not None else [],
            "recommendedSimilarItems": RECOMMENDED_SIMILAR_ITEMS if RECOMMENDED_SIMILAR_ITEMS is not None else [],
            "relatedMediaItems": RELATED_MEDIA_ITEMS if RELATED_MEDIA_ITEMS is not None else [],
            "series": SERIES,
            "shortDescription": SHORT_DESCRIPTION,
            "startDate": START_DATETIME,
            "thumbnailImage": THUMBNAIL_IMAGE,
            "venue": VENUE
        }
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST,\nBODY: {json.dumps(BODY, indent= 4)})")

    try:
        RESPONSE = requests.post(API_URL, headers= HEADERS, data= json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()

        return RESPONSE.json()
    except:
        _api_exception_handler(RESPONSE, "Create Event Failed")