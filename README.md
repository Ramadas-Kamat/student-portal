# AUTOCLAZZ

The Autoclazz is a web based application to automate meet joining, specially designed to benefit Digital education during the current Pandemic era. 
The project is developed during the SCL-Maxo hackathon organized by Sushiksha and World Konkani Center. 
The application is built using Python’s Django framework and enables students to join the scheduled online classes on time.

## Installation Procedure

The following section describes the commands needed to install the Autoclazz project into the local system.

Use git clone to get a copy of the source code.

`$git clone https://github.com/Ramadas-Kamat/student-portal.git`

It is assumed that the user system already has Python 3 and pip installed. Django can be installed using the following command:

`$ pip install django`

All the required python modules can be installed using the following command:


`$ pip install -r requirements.txt`

To run the project on the desired browser, these commands have to be used.

```
$ python manage.py collectstatic
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

In case of any errors using manage.py to run the server, it is recommended that all the cache related information across directories be deleted and these three commands be executed again.



