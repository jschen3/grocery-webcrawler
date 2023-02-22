echo "incrementing counter"
cd /cronjob
python3 -m venv venv
pip install --no-cache-dir --upgrade -r /cronjob/requirements.txt
python3 ./counter.py