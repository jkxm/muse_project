## Introduction

This is my job search web application for the muse.

There are two views, the first is the actual job search
The second is to convert json files into model objects and save them into the database.

Database filled with jobs from the Muse API

## To run application:

Please cd into the project folder and install the packages that I used for this application with the following commands

```bash
pip install -r requirements.txt
```

Once installed, run the server to use application

```bash
python manage.py runserver
```

Job search application is found through http://127.0.0.1:8000/
The API to database view is found through http://127.0.0.1:8000/api_to_db/


## Built With
Django
Flexdatalist
W3 CSS
