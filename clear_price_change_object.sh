echo "starting daily cron scripts"
cd /cronjob
python3 -m venv venv
pip install -r /cronjob/requirements.txt
python3 /cronjob/clear_price_change_object.py