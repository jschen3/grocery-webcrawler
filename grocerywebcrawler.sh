echo "starting daily cron scripts"
cd /cronjob
python3 -m venv venv
pip install --no-cache-dir --upgrade -r /cronjob/requirements.txt
python3 ./webcrawl.py
python3 ./pricechange.py
