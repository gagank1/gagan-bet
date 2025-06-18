# First stage: Build the React app on host arch without emulation
FROM --platform=$BUILDPLATFORM node:20.5.1 AS build
WORKDIR /workspace

COPY ./frontend/package.json ./frontend/package-lock.json ./
RUN npm install
COPY ./frontend .
RUN npm run build
# the COPY commands are separated for better caching.
# If dependencies didn’t change but code did, docker will use the cached npm packages


# Second stage: Build the Flask app
FROM python:3.13
WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# same cacheing strategy as above
COPY *.py ./
COPY --from=build /workspace/build ./frontend/build

EXPOSE 8000
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--workers", "9", "app:app"]
