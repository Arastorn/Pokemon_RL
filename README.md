# Pokemon_RL

## Installation setup :

### Start by installing virtualenv

We'll start by installing virtualenv, a tool to create isolated Python environments. We need to use virtual environments to keep the dependencies used by different Python projects separate, and to keep our global site-packages directory clean. We'll go one step further and install virtualenvwrapper, a set of extensions that make using virtualenv a whole lot easier by providing simpler commands.

```
pip3 install virtualenv
pip3 install virtualenvwrapper
```


 - make sure your python version is 3.5.2 by running the command bellow

```
python3 -V
```


If you doesn't have the right python3 version just download it and set the VIRTUALENVWRAPPER_PYTHON path to it !

Download Python3.5.2 :

```
https://www.python.org/downloads/release/python-352/
```

- Add new variables to your path ( ./bashrc | ./zshrc)

```
vim ~/zshrc
```

- And add the following lines at the end:

```
export WORKON_HOME=$HOME/Envs
export PROJECT_HOME=$HOME/Devel
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 //python3.5.2 path
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source ~/.local/bin/virtualenvwrapper.sh
```

 - Once this is done

```
 zsh
 ```

### Creating the virtual environment

To create and activate a virtualenv, run the following commands:

```
mkvirtualenv poke-venv
workon poke-venv
```


### install the project and dependencies

git glone the repo on the folder you want and go through it:

```
git clone git@github.com:Arastorn/Pokemon_RL.git
cd Pokemon_RL
```

- Now make sure you are in your venv poke-env and then

```
pip install -r requirement.txt
```

## Start and run the server :

 - write this in your terminal :

```
export FLASK_APP=run.py
```

 - then run the server :

```
 flask run
 ```

## Usefull commands

To remove a virtualenv :

```
rmvirtualenv my-env
```
