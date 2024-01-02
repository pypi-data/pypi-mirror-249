class Butrack:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': 'django.log',
                'formatter': 'verbose'
            },
            'console': {
                'level': 'ERROR',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file', 'console'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }