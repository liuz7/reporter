import logging

DEBUG = False
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LOCATION = 'reporter.log'
LOGGING_LEVEL = logging.INFO
PPE_REPORT_PATH = "/usr/local/nagios/etc/scripts/robot_check_report"
PPE_SCRIPT_PATH = "/usr/local/nagios/etc/scripts/search-it-automation/Library/script/ppe_run.py"