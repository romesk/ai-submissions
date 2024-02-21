# Setup virtual environment
setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

# Run migrations
migrate:
	. ../.venv/bin/activate && flask db upgrade

# Rollback migrations
rollback:
	. .venv/bin/activate && flask db downgrade

# Start the development server
run:
	. venv/bin/activate && python run.py