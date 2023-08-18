# gagan.bet

This is the code for the website https://gagan.bet.

Tech stack:
- Frontend: React with react-router-dom and react-toastify
- Backend: Flask (served by Gunicorn)
- Datastore/Job Queue: Redis
- Continuous Deployment: Github Actions (see .github/workflows)
- Reverse proxy: nginx-proxy-manager
- Hosting: Hetzner Cloud (VPS)

Runs in 3 Docker containers orchestrated with docker compose. One for the Flask backend, one for the worker that processes requests, and one for redis.

## Run App

Requirements:
- Docker

The first time you're running the app, run `docker network create scoobydoo`. This is so the services can communicate with nginx-proxy-manager in production.

From then on you can start the containers with `docker compose up --build`. Visit http://localhost:8000 to view the app.
