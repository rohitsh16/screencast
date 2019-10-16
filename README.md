# Screencast

### Build Instructions :

1. Clone the repository. 
2. Start a new virtualenv. 
3. Install the dependencies.
4. Create a .env file.
5. Create apps in Facebook and Google and then in the .env file write the env variables along with the corresponding values.

```
SECRET_KEY=abcd
SOCIAL_AUTH_FACEBOOK_KEY=1846346325670686
SOCIAL_AUTH_FACEBOOK_SECRET=5e6fbada3ddfbdc6a52e2091ec31d353
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=4gd6d8644d
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=7j9377f3f

```

6. Complete the migrations.
7. Create a superuser.
8. Run the server.


### Instructions :

```
$ clone the repo

$ virtualenv myenv

$ cd screencast

$ pip install -r requirements.txt

$ touch .env

$ python manage.py makemigrations 

$ python manage.py migrate

$ python manage.py createsuperuser

$ python manage.py runserver

```
