# Accenture ITS
A modern support ticket system which allows non-admin to submit and reply to tickets, and admin to reply, sort, and manage existing tickets. The ticket system also includes email and SMS notification functionalities for both admin and nonadmin users, and they may attach files to their tickets/replies. This ticket support system is currently locally hosted, and relies on local MySQL server to host ticket data, and AWS S3 service to store any files attached to tickets/replies.

Note: As of 23/5/19, the AWS account which the system is tied to is no longer accessible. Use an alternate AWS account to maintain the same functionalities instead.

---

### To use
1. Create superuser for the ticket system. Run:
   ```
   $ python manage.py createsuperuser --username=joe --email=joe@example.com
   ```
2. Create necessary backend for ticket system. Run:
   ```
   $ python manage.py makemigrations
   $ python manage.py migrate
   ```
3. Run server. Run:
   ```
   $ python manage.py runserver
   ```

---

Note: This website requires tokens to both use POSTMAN API and to access Accenture's ACNAPI. Contact one of the project members if you require the token.


Documentations by SolsticeDante
