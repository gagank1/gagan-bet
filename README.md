# gagan.bet

This is the code for the website https://gagan.bet.

Tech stack:
- Frontend: React with react-router-dom and react-toastify
- Backend: FastAPI (served by uvicorn)
- Database: Firestore
- Hosting: Google Cloud Run

See API docs at https://gagan.bet/docs.

## Run App

You must have Docker installed already. Build the image using `build.sh` and start a container using `run.sh`. For firestore to work locally, you must have the service account key downloaded, and `run.sh` must be modified accordingly.
