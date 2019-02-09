# Chainlink

See what issues projects you're using are having so you can help strengthen your dependencies.

There are two parts to this project:

### Rest API

A Flask REST API that handles getting a list of github packages based on the requirements
file given. Uses python-rq, supervisord, and redis to make multiple requests at once.


```bash
# Run development environment. Starts redis, supervisord, and the flask app
./run.sh dev
```

### Web Frontend

A Vue frontend that gets github packages of a requirements.txt and then gets the github issues
directly from the github API.

```bash
# All frontend code is in frontend/
cd frontend/
# Install node dependencies
yarn
# Run development server
yarn serve
# Build production
yarn build
```


