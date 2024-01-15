echo -ne "\033]0;hub/degree\007"
cd /usr/local/hub/degree/backend-flask
docker compose up -d
poetry install
poetry run python app.py
