fort_flask - take a sip
==========
A fort tree inspired image board in flask.

Currently does not have users, or multiple boards. Can only view replies to 
parent thread in the reply view.

All the functions use sqlite3 instead of sqlalchemy. Images stored locally in static/uploads.

Terrible just terrible.

Initial code taken from flask tutorial on their site.

To initialize the database run the following in a python script or interpreter:

    from fort_flask import init_db
    init_db

bleh
