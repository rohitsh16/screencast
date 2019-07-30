# Screencast Quiz App

> This is a Quiz app.

##  Starting the Project 

* Fork and Clone the repository


* Create a virtualenv with python and activate it
```
virtualenv env

source env/bin/activate
```

* Move into the folder and install required dependencies
```
pip install -r requirements.txt
```

* Set the following environment variables either in your terminal
  or inside a `.env` file that would reside inside `screencast/` dir.
```
SOCIAL_AUTH_FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
TOTAL_LEVELS
```

* Run the Migrations
```
python manage.py makemigrations

python manage.py migrate

``` 
* Run the development server 
```
python manage.py runserver

```
* Head to server http://localhost:8000 to view the app.

## For Contribution

* Solve an issue or add any feature.
* Open any issue or request some nice features.

