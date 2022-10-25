**My Brawl Stats**
==================

Django application to get control over your own stats from the Brawl Stars game.

**Configuration**[^1]
---------------------

### **Creating virtual enviroment**

```console
$ # Linux
$ sudo apt-get install python3-venv    # If needed
$ python3 -m venv .venv
$ source .venv/bin/activate
```

### **VSCode configuration**

Open Command Palette... (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>) and select >Python: Select Interpreter.

```console
$ # Upgrade pip and install Django
$ python -m pip install --upgrade pip
$ python -m pip install django
```

### **Django installation**

First steps to install a Django project from scratch.

```console
$ django-admin startproject <project_name> .
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py startapp <app_name>
```

### **Dependencies**

Save all dependencies to the requirements.txt file

```console
$ # To save dependencies
$ python -m pip freeze > requirements.txt
$ # To install dependencies
$ python -m pip install -r requirements.txt
```

### **Last step**

```console
$ # Run server and enjoy! :yum:
$ python manage.py runserver
```

**Disclaimer**
--------------

This material is unofficial and is not endorsed by Supercell. For more information see : **[Supercell's Fan Content Policy](www.supercell.com/fan-content-policy)**.


[^1]: As this is my first Django app, this README contains some basic and unnecesary information to install and configure a Django project from scratch. That information will eventually disappear.
