import logging
import requests
import json

class ApiLogHandler(logging.Handler):
    def __init__(self, api_url):
        super().__init__()
        self.api_url = api_url

    def emit(self, record):
        log_entry = self.format(record)
        payload = {'test': log_entry}
        headers = {
            'Authorization': 'Bearer 3b1dff0addbc26029334563d98b35183bd68577b'
        }
        # requests.post(self.api_url, data=json.dumps(payload), headers=headers)
        response = requests.request("POST", self.api_url, headers=headers, data=payload)

class Bugrack:
    API_LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'api': {
                'level': 'ERROR',
                'class': 'bug_track.ApiLogHandler',  # Replace 'your_module' with the actual module name
                'api_url': 'https://productivity.colanapps.in/api/bugtrack/',  # Replace with your API endpoint
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['api'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }

    def __init__(self):
        logging.config.dictConfig(self.API_LOGGING)
