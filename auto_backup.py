import schedule
import time
from backup import export_backup

schedule.every().day.at("02:00").do(export_backup)

while True:
    schedule.run_pending()
    time.sleep(60)

