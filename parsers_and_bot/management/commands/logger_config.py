configuring_dict = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format':
                '{levelname} - {asctime} - Module:{module} - Function:{funcName} Line:{lineno} - Message:"{message}"',
                'style': '{',
        },
    },

    'handlers': {
        'to_file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'std_format',
            'filename': 'logs/job_filter_app.log',
            'mode': 'a',
        },
    },

    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['to_file'],
        },
    },
}
