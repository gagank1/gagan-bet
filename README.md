# gagan.bet

This is the code for the website https://gagan.bet.

Tech stack:
- Frontend: React with react-router-dom and react-toastify
- Backend: Flask (served by Gunicorn)
- Datastore/Job Queue: Redis
- Continuous Deployment: Github Actions (see .github/workflows)
- Reverse proxy: nginx
- Hosting: Hetzner Cloud (VPS)

Runs in 3 Docker containers orchestrated with docker compose. One for the Flask backend, one for the worker that processes requests, and one for redis.

Nginx reverse proxies and handles SSL. All requests are forwarded to gunicorn including static file serving. It directly serves the react build folder.

To configure nginx:
Copy the included configuration file into the default configuration in sites-available. Then run certbot to enable HTTPS.

## Run App

Requirements:
- Docker

Start the containers with `docker compose up --build`. Visit http://localhost:8000 to view the app.
