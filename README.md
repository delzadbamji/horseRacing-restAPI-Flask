# horseRacing-restAPI-Flask

This app is a simulation of a simple betting platform of a derby race.


Here, you are expected to query a custom-built REST API for a horse and get the details of the horses. 
<If this GET request is not performed before placing the bet, then an error shall be raised>

Once the horse data is retrieved, you can choose a horse that matches your budget and place a bet.
If you place a bet on a horse that you can't afford, an error shall be raised.

If the bet is successful, a success message is sent with the horse's data.

Curerently, the API only returns a 200 or 404 status.

If we add authentication to the page, we can also add a 401 status.

In the future, the user-side data will also be stored in a db to be able to have a robust client-server application.
Since the main focus of this application was server-side, the UI is left basic. 
