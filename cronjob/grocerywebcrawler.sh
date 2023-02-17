python3 -m venv venv
pip install --no-cache-dir --upgrade -r /cronjob/requirements.txt
python3 /cronjob/webcrawl.py
python3 /cronjob/pricechange.py
