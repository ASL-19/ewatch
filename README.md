# Election Watch 

To enable responsive governance and informed engagement with presidential elections, Election Watch project will raise awareness 
about electoral processes and enable informed engagement with presidential elections, through independent, credible and accessible 
educational content hosted on an this platform, including: 
  - Developing voter educational materials to facilitate improved understanding of electoral processes, and the powers and 
  constraints of the president,
  - Election monitoring to enable informed engagement with the presidential elections.

This repository contains the Web Server backend of the system. The platform backend is written in Django and 
provides admin access as well as API end points.

## Running Django Locally

### 1 Django APIs

#### 1.2 Setup
The backend engine is built on top of  [Django](https://www.djangoproject.com/) which we recommend to run it inside a 
virtual environment. In order to install the dependencies, use <code>pip</code> command and read all the dependencies
from <code>requirements.txt</code> file:
```bash
pip install -r requirements.txt
```

#### 1.3 Structure
There are three main applications inside the project directory (listed below). 

- ewatch: Main app to contain project configurations and settings
- blog: Contains a simple and customized pseudo-blog application to take care of the blog-type content.
- candidate: App to take care of Candidate profiles
- timeline: App to take care of News timeline
- preferences: Holds preferences data for the site

Other directories are:

- locale: to take care of translations
- STATIC: to hold static content for dev site, on production site they get stored on S3
- MEDIA: to hold media uploads for the blog, on production site they get stored on S3
- logs: to hold application, gunicorn, nginx and supervisor logs

### 2 Database
It's highly recommended to use PostgreSQL as your database since django fully supports it. However, using MySQL and other
databases should be fine too. The current project works with Postgres as its default.

### 3 Configuration
Configuration of sensitive secrets inside the app should be handled through environment variables

Save the following into a file named `environment`
```bash
export BASE_DIR=<Absolute path of the project root directory>
export BUILD_ENV=<development|production>
export DATABASE_HOST=<host>
export DATABASE_USER=<username>
```

then run `source environment` to set the variables

### 4 Serving the application
Choosing Webserver depends on your previous experiences. The most straightforward webserver to test the application 
is Apache mod_wsgi. 

In the Django root:
```bash
python manage.py runserver
```
