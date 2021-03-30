# Income Expense Tracker Using Django

### Table of Contents
- [Main Features](#main-features)
- [Requirements](#requirements-for-running-project)
- [Steps for running project](#steps-for-running-project)

### Main Features
* Add Expenses and Incomes by different catgeory and source.
* Users can export their expenses and incomes in an excel and csv. (filters are present to download data by year, week, month and today)
* Visualize data by a graph. Graphs are using filtering to show data of month, year, week and today.
* Users can change graph options. (eg: piechart, bargraph, linegraph, etc)
* Users can export their expenses and incomes in an excel, csv and pdf.
* Users can import incomes and expenses from a csv.
* Users can also search expenses and incomes present in their account

### Requirements for running project 
- [python > 3.5.x](https://www.python.org/downloads/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [postgresql](https://www.postgresql.org/download/)
- [Gmail account with less secure apps on](https://www.google.com/intl/en-GB/gmail/about/#)
- [Weasy Print](https://weasyprint.readthedocs.io/en/latest/)
- [Cloudinary account](https://cloudinary.com/)

### Steps for running project
```
git clone https://github.com/rishank-shah/Income-Expense-Tracker.git
cd Income-Expense-Tracker
cp .env.example .env
```
##### Fill the .env file with the correct database, email credentials and cloudinary api credentials, then in terminal execute following commands

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
source .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

##### If all commands run successfully website will be running on PORT 8000 on localhost [http://localhost:8000](http://localhost:8000)
