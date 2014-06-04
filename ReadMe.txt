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

actually do this:
requirements.txt

Django==1.6
dj-database-url==0.2.2
dj-static==0.0.5
gunicorn==18.0
psycopg2==2.5.1
static==0.4
wsgiref==0.1.2
bitcoin-python==0.3
virtualenv==1.11.6

no need to have a mybitcoinrpc now that i have bitcoin-python in requirements.txt

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


$git init
$git add .
$git commit -m "first commit"

To commit git needs to know 'who I am'

$git --global user.email 'myemail@dsddsds.com"
$git --global user.name 'Aiden"

Now commit

download heroku toolbelt from heroku site:
After installing the Toolbelt, you’ll have access to the heroku command from your command shell. 
Authenticate using the email address and password you used when creating your Heroku account:



$ heroku login
Enter your Heroku credentials.
Email: adam@example.com
Password:
Could not find an existing public key.
Would you like to generate one? [Yn]
Generating new SSH public key.
Uploading ssh public key /Users/adam/.ssh/id_rsa.pub

Press enter at the prompt to upload your existing ssh key or create a new one, used for pushing code later on.

$heroku create

$git push heroku master
Might get some errors:
make sure requirements.txt is the same as on heroku django site
in git bash do 
$git mv Procfile.txt Procfile
$git add .
$git commit -m "renamed procfile"

git push heroku master
$heroku keys:add (might need to do this if i get a public key error)
---------------------
Then, every time you want to deploy to heroku
$ git add -A
$ git commit -m "commit for deploy to heroku"
...

$ git push -f heroku


============

host bitcoind on some site (digitalocean)
have website on another

start a 'droplet' on digital ocean

Follow instructions to make a friendly local UI for doing the rest:
https://www.digitalocean.com/community/articles/how-to-log-into-your-droplet-with-putty-for-windows-users

when you login the first time, use the password emailed to gmail acct

copy the reddit script:
http://www.reddit.com/r/Bitcoin/comments/1se3zd/how_to_create_a_full_bitcoin_node_in_a_5_ubuntu/

The preceding script set the rpcuser rpcpassword to random in the wallets bitcoin.conf file
- I don't want them random because I want to connect to this from my other website using bitcoinrpc calls
bitcoinrpc
in putty console
cd ~/.bitcoin

vim bitcoin.conf
i
make bitcoin.conf look like:
server=1
daemon=1
rpcuser=aiden
rpcpassword=hfhjh
rpcallowip=*
:x

then set up firewall using ufw (I have to disable the firewall for some reason - more https://www.digitalocean.com/community/articles/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server)

sudo ufw enable
sudo ufw allow 8322/tcp
sudo ufw allow 22/tcp
sudo ufw default deny incoming
sudo ufw allow from 71.178.208.222 #my ip, subject to change
sudo ufw allow from (https://devcenter.heroku.com/articles/proximo - use this to get a static OUTBOUND ip for heroku app)

now the bitcoin and putty ports are open (8322 and 22, respectively and all incoming requests are blocked
except for coming from my heroku and my local, but because I don't have a static ip yet, i'm just going to disable ufw
>sudo ufw disable)


reboot

Now I have a real-deal connection with:
c=b.connect_to_remote('aiden','Peyton18','107.170.92.113',8332)



digital ocean credit DODEPLOY



