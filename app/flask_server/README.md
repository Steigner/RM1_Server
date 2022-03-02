# RoboMedicinae1 - Server
## Python Flask
As mentioned, the application should be run as a development server through the Flask server. This is one of the easiest ways to test and preview the application.

**Dependencies:**
* Poetry [=>](https://python-poetry.org/)

Install Poetry, config by docs, and use.

```console
user@user-pc:~$ poetry install
user@user-pc:~$ poetry run python run.py
```

or

* PIP [=>](https://pip.pypa.io/en/stable/)

```console
user@user-pc:~$ python3 -m venv my_venv
user@user-pc:~$ source my_venv/bin/activate
(my_venv) user@user-pc:~$ pip install -r requirements.txt
(my_venv) user@user-pc:~$ python3 run.py
```

## JavaScript libraries
Javascript libraries is imported by **cdnjs**, so for function is neccesary to be connected to internet. But one options is to use offline import, and I ziped libraries in folder **./app/flask_server/app/static/js/lib**.

## Test Brute Force
This is a very simple demonstration of brute force password cracking, to test it you need to disable CRSF in the code. CSRF(Cross-Site Request Forgery). This disable is situated in sciprt **.app/flask_server/app/forms.py**

Run test:

```console
user@user-pc:~$ poetry run python run.py
user@user-pc:~$ poetry run python test_bruteforce.py
```

## Black
For code I decided to use Python formatter Black, to use, it simply type for example:

```console
user@user-pc:~$ poetry run black script_what_you_want.py
user@user-pc:~$ poetry run black --line-length 79 ./folder_what_you_want
```

## Prettier
Code formatter for JS, CSS i used extension to Visual Studio Code Prettier. In **./app/flask_server/app/static** is situated config file for prettier **.prettierrc.json**.

**Dependencies:**
* Prettier [=>](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

## UnitTest
The application also has a basic Python unittests, can be changed as needed. To start:

```console
user@user-pc:~$ poetry run python test_app.py
```

**----------------------------------------------------------------------**

Ran 16 tests in 49.476s

OK
