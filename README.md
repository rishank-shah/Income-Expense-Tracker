# Income Expense Tracker Using Django

### Requirements for running project 
- [python-3.8.2 (32-bit)](https://www.python.org/downloads/release/python-382/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [git-bash](https://git-scm.com/downloads)
- [postgresql](https://www.postgresql.org/download/)
- [Gmail Account](https://www.google.com/intl/en-GB/gmail/about/#)
- [Weasy Print](https://weasyprint.readthedocs.io/en/latest/)

#### NOTE : If running on windows please use git-bash
### Steps for running project
```
https://github.com/rishank-shah/Income-Expense-Tracker.git
cd Income-Expense-Tracker
cp .env.example .env
```
##### Fill the .env file with the correct database and email credentials, then in terminal execute follwing commands

```
virtualenv venv --python=python3.8.2
source venv/Scripts/activate
pip install -r requirements.txt
source .env
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### If all commands run successfully website will be running on PORT 8000 on localhost [http://localhost:8000](http://localhost:8000)
