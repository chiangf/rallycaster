import json


def get_response_data(response):
    return json.loads(response.data)
