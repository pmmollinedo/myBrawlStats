from datetime import datetime

from .helpers import fetch_from_api

from .services import BrawlStarsApiException

def get_cron_log_init():
    now = datetime.now()
    return f'{now.strftime("%d/%m/%Y %H:%M:%S")} -'

# Logs are saved at ../logs/cron_jobs.log
def fetch_from_api_cron():
    print(f'{get_cron_log_init()} CRON JOB - started.')
    try:
        fetch_from_api()
        print(f'{get_cron_log_init()} BrawlStarsAPI successful connection.')
    except BrawlStarsApiException as api_ex:
        print(f'{get_cron_log_init()} An error ocurred - HTTP code [{api_ex.error_code}] message [{str(api_ex)}].')
    except Exception as e:
         print(f'{get_cron_log_init()} Fatal error while XX data.')
    print(f'{get_cron_log_init()} CRON JOB - finished.\n')