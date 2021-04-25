# Income Expense Tracker Using Django

#### Website Deployed on [Heroku](https://expenseincometrackerdjango.herokuapp.com/)

### Table of Contents
- [Main Features](#main-features)
- [Requirements](#requirements-for-running-project)
- [Steps for running project](#steps-for-running-project)
- [Generate dummy data](#generate-dummy-data)

### Main Features
- [x] Add Expenses and Incomes by different catgeory and source.
- [x] Users can export their expenses and incomes in Excel, CSV or PDF. (filters are present to download data by year, week, month and today)
- [x] Visualize data by a graph. Graphs are using filtering to show data of month, year, week and today.
- [x] Users can change graph options. (eg: piechart, bargraph, linegraph, etc)
- [x] Users can import incomes and expenses from a csv and excel.
- [x] Users can also search expenses and incomes present in their account

### Requirements for running project 
- [python > 3.5.x](https://www.python.org/downloads/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Gmail account with less secure apps on](https://www.google.com/intl/en-GB/gmail/about/#)
- [Weasy Print](https://weasyprint.readthedocs.io/en/latest/)
- [Cloudinary account](https://cloudinary.com/)
- [Sentry account](https://sentry.io/welcome/)

### Steps for running project
```bash
git clone https://github.com/rishank-shah/Income-Expense-Tracker.git
cd Income-Expense-Tracker
cp .env.example .env
```
##### Fill the .env file with the correct database, email credentials and cloudinary api credentials, then in terminal execute following commands

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
source .env
python manage.py migrate
python manage.py runserver
```

##### NOTE: If you dont want Sentry Error Monitoring remove lines [177](expense_project/settings.py#L177) to [183](expense_project/settings.py#L183) from [settings.py](expense_project/settings.py#L177)
```py
if DEBUG == False and os.environ.get('SENTRY_DSN','') != '':
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )
```

### Generate dummy data
```bash
cd Income-Expense-Tracker
source venv/bin/activate
source .env
python generate_data.py
```

##### If all commands run successfully website will be running on PORT 8000 on localhost [http://localhost:8000](http://localhost:8000)
