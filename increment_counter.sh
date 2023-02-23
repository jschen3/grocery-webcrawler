echo "incrementing counter"
cd /cronjob
python3 -m venv venv
pip install -r /cronjob/requirements.txt
python3 /cronjob/counter.py
