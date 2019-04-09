#### 7/4
To do:
- Fix creation of ticket id
  - Need to put creation of ticket id as a background task, and whenever tickets are created the creation of id is a critical section
  - django-background-tasks for background tasks
    https://django-background-tasks.readthedocs.io/en/latest/
  - QuerySet.select_for_update() to lock row when doing operations

  - All data will be bucketed into multiple tickets (with the first 'ticket' holding information for this entire table)
    - Each ticket will have (ticket_id)(size{for first 'ticket' this represent total number of tickets in database})(user)(administrator assigned to ticket)(resolved_by)(read_by)
  - Within each ticket a table will be created "Ticket_{ticket id}", except for the first 'ticket'
    - Each ticket will have (post_id {starting from 0})(title)(description)(more can come later)

- Add ticket replying
- Add image attachment, textfile and pdf attachement to ticket (will need ticket id (and possibly reply))
- Add email and sms notification
- Add email and sms notificattion whenever ticket reply/ticket create
- Add automatic account creation when new ticket is created


Note: to delete all existing databases:
```
$ sudo mysql -u root -p
$ USE `50003`;
$ DROP TABLE create_extended_user;
$ DROP TABLE create_extended_user_groups;
$ DROP TABLE create_extended_user_user_permissions;
$ DROP TABLE ticket_creation_all_tickets;
$ DROP TABLE ticket_creation_ticket;
$ DROP TABLE ticket_creation_ticket_details;

```



#### 1/4
- Recreated model to handle User data: Extended_User in createuser
--- createuser_extended-user is a table found in database `50003` in mysql and all fields are present, including phonenumber - hence i'd consider this a successful transition from the classic User model to our Extended_User
--- Creation of user account and logging in works fine


#### 22/3
- Things that're standardized:
--- Loading of templates - render for templates within the app, httpresponseredirect for templates outside the particular app
--- Error messages in templates - By default, error_message is in template is None


##### 11/3
- Managed to set up mysql on django with zhaohong's help
- Run
```sudo apt-get install mysql-server```
- If you cant log in, try finding account info of "debian-sys-maint" and log in using that, it has root privileges and can let you reset root password
- If you're logging in root, run
```sudo mysql -u root -p```
then insert new password
- Create new user (according to our settings.py) and new database `50003`. Rmb use ` .
- run
```
$ pip3 install mysqlclient
$ python3 manage.py migrate
$ python3 manage.py runserver
```
- Implementing pass test case for createuser now (in /Source/website/createuser/tests.py)
Test was not detected when ```python3 manage.py test createuser``` is run
https://docs.djangoproject.com/en/2.1/intro/tutorial05/


##### 3/3
- Tried to use docker to set up mysql, died so hard am gna continue some other time
- Used mysql base but when i run docker image there's no response, even when i get the port right. I suspect running mysql docker runs something else that i do not know of, need to find out more
- Next step: Run docker without mysql, then mysql with appropriate RUN and CMDs to know how to use mysql base images better
- Now i'm setting up mysql to run the website without docker first
https://www.digitalocean.com/community/tutorials/how-to-create-a-django-app-and-connect-it-to-a-database
- ok because i forgot my mysql passoword, this itself is also cancer. tried burning and reinstalling but didnt work. consider using docker or burn ubuntu and install xubuntu and shunbian reinstall mysql
https://www.digitalocean.com/community/tutorials/how-to-create-a-django-app-and-connect-it-to-a-database
https://www.digitalocean.com/community/tutorials/how-to-install-the-latest-mysql-on-ubuntu-16-04#step-2-—-installing-mysql


##### 26/2
- Fixed finding of "create profile" template. Redid login as a separate app.
- Creating user: {username: user1, password: 1234, ID:1, email:boi@gmail.com, phonenumber:87654321}
- Creation of user is successful, missing a couple of possible errors (same username, password checking etc.)


##### 24/2
- I realised login, and home page should belong in a separate app, instead of being in the website/ dir. 
- Need to write app for home, log-in and then account creation
https://docs.djangoproject.com/en/2.1/intro/tutorial03/

##### 19/2
- Currently server has issues opening create-user.index i think the problem lies in the DIRs that the bootloader is looking at. Might have to configure the DIR in TEMPLATES of settings.py to accomodate apps other than the main log-in page. But must be able to revert to original cos settings.py is used by the rest of the team.

##### 16/2
- Learning how Users work, and creating notes for User management
- Halfway through creating the form for account creation (Just created Form class). Taking reference from:
https://docs.djangoproject.com/en/2.1/topics/forms/

##### 8/2
- Created web interface to log-in and log out using the following guide
https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/
- Will need to work on hosting website on heroku, and dependencies taken care of by docker. To implement these with Django, use the following guides:
https://docs.docker.com/compose/install/
https://docs.docker.com/compose/django/

##### 29/1
- Each of us are to create our own questions to clarify our project requirements by tonight 2359. I am to contact the client in Accenture to prepare a day to ask questions.

##### 28/1
- Project 2 is chosen, done in Python. None of us are experienced/interested in game development. Zhao hong has experience in web development (Python Flask/Django)
