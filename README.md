# appsaway
Job Application Tracker

Track your job applications and the companies you apply for. Easily generate reports, search items, and keep up with the statuses of each application easily. No more losing information on who you've applied to. Send out hundreds of applications and manage them with ease!

## Features:
- Keep companies up-to-date with contact details and notes
- Track applications with status, app date, follow-up date, interview date and type and more depending on type

  Application Types: Contract, Freelance, and Permanent.

## Requirements:
- Python 3.10.0
- virtualenv

## Install (Local):
1. Clone the repo and activate virtualenv in the project directory.
2. Activate the virtualenv `source bin/activate`
3. Install the requirements `pip install -r requirements.txt`
4. Update appsaway/settings.py to reflect your needed settings. Default is for Heroku deployment.
  - ALLOWED_HOSTS *(Ex. "ALLOWED_HOSTS = ['yourdomain.com']" or * for all)*
  - SESSION_KEY *(Ex. SECRET_KEY = 'yoursecretkeyhere')*
5. Make backend models `./manage.py makemigrations backend`
6. Build the database `./manage.py migrate`
7. Run the server with `./manage.py runserver`

For remote or production installs please use a production webserver and database. Please see Django documentation for further details.
