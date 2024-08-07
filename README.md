# Description

A fullstack web application using React, Material-UI, Flask and SQLite.
Has user registration, login, password reset.

Can be installed as PWA on mobile devices.

Deployed on a webserver with Nginx and Gunicorn in Docker containers. The deployment is automated with Github Actions and a Watchtower container to update the Docker containers.

Example animation of a gallery:
![Gallery](https://github.com/rafael-ottersberg/react-mui-flask-webapp/blob/master/webapp_gallery.gif?raw=true)

# Installation

Install npm and run

```
npm install
```

in the project folder.

Create a virtual python environment and install the dependencies in the file backend/requirements.txt

```
python
pip install -r requirements.txt
```

initialise database by running:

```
python init_db.py
```

# Starting the webapp (development)

npm is configured to start both, the frontend and the backend/api:

```
npm start
```

Start the the backend:

```
cd backend
flask run
```

# Deploying on the webserver

Nginx is install on the web server to serve the web applications.  
The backend is accessed via a reverse proxy and is served with gunicorn.

### Settings for domain.ch (production)

Location of github repo: ~/production/react-mui-flask-webapp  
Location web files: /var/www/domain.ch  
Settings for nginx: /etc/nginx/sites-available/domain.ch

Backend api served on: http://localhost:5002  
Name of api service (gunicorn): camp-prod-api

### Settings for dev.domain.ch (development)

Location of github repo: ~/react-mui-flask-webapp  
Location web files: /var/www/dev.domain.ch  
Settings for nginx: /etc/nginx/sites-available/dev.domain.ch

Backend api served on: http://localhost:5001  
Name of api service (gunicorn): camp-dev-api

## Updating the webapp on the webserver.

```
cd react-mui-flask-webapp
# --or--
cd production/react-mui-flask-webapp
```

```
git pull
# git checkout tags/<tag> -b <branch>

conda activate camp-frontend

# npm install

rm -r build && npm run build && sudo cp -r build/* /var/www/dev.domain.ch/html/
# --or--
rm -r build && npm run build && sudo cp -r build/* /var/www/domain.ch/html/

sudo systemctl restart camp-dev-api
# --or--
sudo systemctl restart camp-prod-api
```

## Using Docker

Create a Github personal access token here: https://github.com/settings/tokens

Save the PAT in a file, e. g. called `pw.txt` and then log in to the Container
registry of Github.

```shell
# Replace USERNAME with your Github username
cat pw.txt | docker login ghcr.io -u USERNAME --password-stdin
```

Get the `deployment` folder by copying it or cloning the repository.

Ensure that both the `deployment/domain.ch` and
`deployment/dev.domain.ch` folders contain a `db.sqlite` file.

### Run service

#### Using service description

This is the preferred way as it should start on server start:

```shell
# Start dev service
sudo systemctl start camp-dev-docker

# Stop dev service
sudo systemctl stop camp-dev-docker
```

#### Manual

This is only included as documentation, please use the section above to
start/stop the server.

Run `deployment/domain.ch/docker-compose.sh up -d` for production and
`deployment/dev.domain.ch/docker-compose.sh up -d` for staging/dev. Both frontend
and backend are exposed through an ingress on a single port per environment.
Those ports can be used in a system wide ingress (e. g. nginx) to expose it via
HTTPS on specific domains.

### Run python shell to change database

```shell
# In /home/rafael/react-mui-flask-webapp/deployment/dev.domain.ch or /home/rafael/react-mui-flask-webapp/deployment/domain.ch
sudo ./docker-compose.sh exec backend python3
```

# Database migrations

If new tables or columns are added in the flask app or removed from the database, Flask_Migrate can be used to migrate the db.sqlite.

```
cd backend
```

If flask migrate is used for the first time:

```
flask db init
```

Everytime you migrate:

```
flask db migrate -m "migration message"
flask db upgrade
```

## Modify db entries

### Set up IPython

```
from api import app
from api.extensions import db
from api.models.user import User
app.app_context().push()
```

### Select user

```
user = User.query.filter_by(email="rafael.ottersberg@gmx.ch").first()
user = User.query.get(1)
```

### Modify or delety user

```
user.vorname = "Rafael"

db.session.delete(user)
```

### Commit changes to database

```
db.session.commit()
```

# Local development

There is a `docker-compose.yml` file which can be used for local development.
First you need to add the VAPID_PRIVATE_KEY and EMAIL to the last two lines in
the file. Afterwards you can use the application with the following commands:

```
# Start app
docker-compose up -d

# Stop app and remove containers
docker-compose down

# To apply changes in frontend
npm run build

# To apply changes in the backend
docker-compose restart backend
```
