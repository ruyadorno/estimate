estimate
========

http://ruyadorno.github.io/estimate

Application to help time estimation for digital agencies.

## Main Goals ##

 - Time estimations should get way easier and faster for the whole team.
 - This should be an easy to use tool for newcomers.

## Demo ##

We have a temporary demonstration version on http://estimate-demo.olh.am running the develop branch. Just log in using an OpenID account and test the application.

## Dependencies ##

 - [Django 1.5.1](https://www.djangoproject.com/)
 - python-openid 2.2.5
 - [django-openid-auth 0.5](https://launchpad.net/django-openid-auth)

## Installation ##

Some knowledge on the Django web framework is required for setting up an Estimate application. Though it might be a bit more challenging for someone without a previous experience on it, there are plenty of documentation and tutorials available.
You can find below the steps to install Estimate on a server and some useful links.

 - Configure a django installation on a webserver of your preference, though I have only tested it on Apache with wsgi, any other popular option should be fine too. You can find more instruction on those in the [Django Documentation](https://docs.djangoproject.com/en/1.5/howto/deployment/wsgi/)
 - Clone the repo on your server in a folder of your preference
 - Create a python virtual environment for your installation, this step is probably optional but highly recomended. For more instructions check the [Virtualenv website](http://www.virtualenv.org/)
 - Install the project dependencies with `pip install -r requirements.txt`
 - Create a `estimate/local_settings.py` file, you should use `estimate/local_settings_template.py` as a reference.
 - Configure your database, MySQL as an example will need an extra `pip install MySQL-python`
 - Configure django project, such as sync the database and collect the static files

## License ##

Released under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
