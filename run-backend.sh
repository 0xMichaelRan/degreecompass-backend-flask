echo -ne "\033]0;degree-backend\007"
cd /usr/local/hub/degree-compass/backend-flask
docker compose up -d
poetry install
poetry run python app.py
