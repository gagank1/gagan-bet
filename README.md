# gagan.bet

This is the code for the website https://gagan.bet.

Tech stack:
- Frontend: React with react-router-dom and react-toastify
- Backend: Flask (served by Gunicorn)
- Datastore: Redis
- Reverse proxy: nginx

Runs in 3 Docker containers orchestrated with docker compose. One for the Flask backend, one for the worker that processes requests, and one for redis.

Nginx reverse proxies and handles SSL. All requests are forwarded to gunicorn including static file serving. It directly serves the react build folder.

To configure nginx:
Copy the included configuration file into the default configuration in sites-available. Then run certbot to enable HTTPS.

To run the app:
Build the react app in `frontend/` with `npm run build`. Then start the containers with `docker compose up --build`.

