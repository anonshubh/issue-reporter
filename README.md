## An Issue Reporting App which handles issues and resolves it conveniently in Team.

**Setup and Run Locally**
---
*Requirements:- Python 3.8+*<br>
1) `git clone https://github.com/anonshubh/synergee.git`
(For Developer: Use your Forked URL) 
2) `cd synergee`
3) `python -m venv env`
4) `source env/bin/activate` (Mac/Linux)<br>
   `env/Scripts/activate.ps1` (Windows-Powershell)
5) `pip install -r requirements.txt`
6) `python manage.py runserver`

**For Users**
1) Test-user is with username as testuser and password as demouser@123
2) Test-user has all functionalities which are possessed by CRs/Team Leads

**For Developers**
(Built Using Django)
1) Website consists of 4 django apps profiles, polling,infolist and reporter.
2) User Authentication is implemented in profiles App.
3) Issue Reporting is implemented in reporters App.
4) User Polls Functionality is implemented in Polling App.
5) All django templates are inheriting from ~/templates/base.html
6) User Authentications templates are at Global Project Level.
7) Issue Reporting templates are Local to reporter App.
8) Upvotes and Downvotes are asynchronous implemented with VanillaJS only.

**Technology Stack**
---
Django 3.1.* <br>
db: postgres 12
