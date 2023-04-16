env.setup:
	python3 -m venv .venv
	echo "run the following manually"
	echo "source .venv/bin/activate"
	echo "pip install -r requirements.txt"

run:
	uvicorn app.main:app --workers 1 --host 0.0.0.0 --port 8000 --reload
