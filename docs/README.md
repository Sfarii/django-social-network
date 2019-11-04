Social network documentation!
========================================

This structure is based on research and own experience of developing Django apps.

# Requirements
python 3.5 or higher;

# Installation
Creating an isolated Python environment.

Create a project folder and a venv folder within:

```shell
$ python3 -m venv venv
```
# Install dependencies
Now, you will need to set up virtual environment that will keep the application and its dependencies isolated from the main system.

Next run the following command with the name of your temporary virtual environment.

```shell 
$ source venv/bin/activate
```

Now, run following command to install Flask dependency inside it:

```shell
$ pip install -r requirements/base.txt
```

# Usage

Run this command to run the built-in web server and access the application in your browser at http://localhost:8000:

```shell
$ python3 manage.py runserver
```