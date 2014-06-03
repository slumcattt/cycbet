https://devcenter.heroku.com/articles/getting-started-with-django

The above url covers most of it, but not well.

Have django installed
download and install git as standard
pip install virtualenv (you will need a virtualenv)

cmd
>cd to Desktop
>mkdir myproject
>cd myproject
>virtualenv venv (will create venv folder inside current myproject directory)
>C:\Users\Aiden\Desktop\myproject\venv\scripts\activate.bat (cmd prompt will now have (venv))
>pip install django-toolbelt (get come error about psycog2)
save .exe to some place (download from http://stickpeople.com/projects/python/win-psycopg/)
>(venv) cd to .exe
>(venv) easy_install psycopg2-2.5.3.win32-py2.7-pg9.3.4-release.exe
I think this gets what wasn't gotten with the error

>(venv) cd to myproject directory

Desktop
	-myproject
		-venv

>(venv)C:..Desktop/myproject> django-admin.py startproject mproject . (the . is muy importante!)

Now:
Desktop
	-myproject
		-myproject
			-settings.py
			-wsgi.py
		-manage.py
		-venv

You can now run locally, but you must configure for heroku.

>(venv)C:..Desktop/myproject>pip freeze>requirements.txt

add Procfile (no extension) to product root directory, add stuff from heroku tutorial to settings.py and
wsgi.py

Now, if you runserver you get an error. Fix by:

>(venv)C:..Desktop/myproject>pip install dj-database-url
>(venv)C:..Desktop/myproject>pip install dj-static

Now go into git to commit and deploy to heroku as in tutorial

go into git bash
$cd..to my project

(probably want to make a .gitignore file)
http://stackoverflow.com/questions/10744305/how-to-create-gitignore-file

    1.Create the text file gitignore.txt
    2.Open it in a text editor and add your rules, then save and close
    3.Hold SHIFT, right click the folder you're in, then select Open command window here
    4.Then rename the file in the command line, with ren gitignore.txt .gitignore

*.pyc
mybitcoinrpc/  (copy bitcoinrpc folder (jgarzik pip install bitcoin-python thing) to myproject directory, 
rename mybitcoinrpc, add a config file, make it able to connect to my wallet and change the config file to 
connect_to_remote (add rpcallowip=WHATEVR.MY.IP.IS)

$git init
$git add .
$git commit -m "first commit"

