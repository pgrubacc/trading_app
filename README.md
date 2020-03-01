# trading_app
Simple Django/React app used to perform and display trades in different currencies.

It's deployed as three separate containers - one for the backend (Django), 
one for the database and the last one for the frontend (React).

The servers used are Django's built-in one and a simple node one provided by node start.
This is a setup to be used for development purposes. For production, you'd likely want to use
a proper solution like uWSGI/nginx.

It uses a third party API (https://fixer.io/) to get the list of supported currencies and
to get conversion rates for different currencies. The backend uses the API on startup 
to acquire a list of supported currencies.

**Note**: The free plan of the API only provides the ability to get exchange rates for EUR as the
base currency. The backend will return a 503 error in this case and this is not handled on the 
frontend yet.

Setup
------------------------------
Prerequisites: a docker-compose that supports version 3.7 has to be present on your machine.

The project depends on 3 .env files which are not checked in the repo. You can see how they're 
supposed to look by checking the .template files. To start without much hassle, you can simply 
take the template files and copy them into files without the template extension:

    cp .db_env.template .db_env
    cp api/api/settings/.env.template api/api/settings/.env
    cp .client_env.template .client_env

After that, all that's left is to build and run:
.. code::

    docker-compose build
    docker-compose up

By default, the backend will be available at port 8002, and the frontend at port at 8001.
You should be able to check the frontend page at localhost:8001.

If you want to check the backend API docs, you can visit localhost:8002/api/

To run the backend tests, execute the following command inside the backend container:
.. code::

    python manage.py test

To refresh the database with new currencies from the exchange API, the following command is 
provided:
.. code::

    python manage.py populate_db_currencies

It is ran during Django the container startup.

Things to improve:
------------------------------
Frontend:
 - Split the frontend project into more components and add validation for all API calls
 - Handle the following case: user prepares to make a transaction and then waits for some 
 time. An additional check should be made to see if the rate changed and warn the user
 - Add tests

Backend:
 - Handle the case if the third party API removes support for some currencies. Right now, 
 there's no check if any of the currencies are gone during the populate currencies startup step
 - Improve logging for manage.py populate_db_currencies
 - Implement a caching option in case we want to save exchange API bandwidth
