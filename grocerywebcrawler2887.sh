echo "starting daily cron scripts"
cd /cronjob
python3 -m venv venv
pip install -r /cronjob/requirements.txt
python3 /cronjob/webcrawl2887.py