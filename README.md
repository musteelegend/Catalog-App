## Catalog App ##

## What's included: ##

##Quickstart
##Install
*Install [Python](https://www.python.org/downloads/)
*Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
*Install [Vagrant](https://www.vagrantup.com/downloads)

**project.py**
This is a python file, it has all the blueprints for all the other classes defined, and contains the handlers for specific tasks, where each handler is mapped to a specific URL.

**static folder**
This folder contains the CSS files main.css, bootstrap.min.css and the Javascript file bootstrap.min.js used for styling the templates

**templates folder**
This folder contains HTML files that connect the pages together and help make it a fully interactive blog.

**database folder**
This folder cantains the code that creates the tables for the database and holds the data there after.

**login_handlers folder**
This folder contains the code that handles login using oauth providers, Facebook and Google. It also has user registration and localized login.

**logout_handlers folder**
Contains the code to logout of the application

**main_handers folder**
This folder contains the handlers for catalog and items. This handlers create, show, delete or edit catalogs or items in this catalogs

**REST_handlers folder**
This code provides the JSON version of the items and catalog tables in the datase

## How to Run this Program: ##
From the terminal, run:

    git clone https://github.com/musteelegend/Catalog-App.git Catalog-App

This will give you a directory named **Catalog-App** complete with the source code for the flask application, a vagrantfile, and a pg_config.sh file for installing all of the necessary tools.

** Run the virtual machine!

Using the terminal, change directory to oauth (**cd Catalog-App**), then type **vagrant up** to launch your virtual machine.


## Running the Catalog App
Once it is up and running, type **vagrant ssh**. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt. When you want to log out, type **exit** at the shell prompt.  To turn the virtual machine off (without deleting anything), type **vagrant halt**. If you do this, you'll need to run **vagrant up** again before you can log into it.

## How to view this application ##
To view this page visit the below URL

https://localhost:5000/login