The goal is to generate a simple Django application with simply SQLite as the database, and with

* a single Model called Fund, representing the data in the attached sample_fund_data.csv
* a way to import such Fund objects by uploading a CSV file matching the sample provided, via a file upload form on a Django web page: the Django app should then parse that file and create corresponding Fund objects in the database
* a web page displaying:
the list of funds available in the database as a table with one column per field on the Fund model
a dropdown at the top of the page, allowing you to select a Strategy value, and filter the funds displayed on the page by one of the available Strategy choices
at the bottom of the table, display the total number of Funds in the database
if the current page is filtered by a Strategy value, then this number should be the number of Fund objects matching the filter
at the bottom of the table, display one number that is the sum of all Fund AUM values (AUM is one number field listed in the sample CSV file)
* A REST API endpoint that can
list Fund objects that are in the database, in a JSON format
a way to filter the objects by the Strategy field, by appending a query parameter ?strategy=[value] to the URL of that endpoint
another endpoint to view a JSON representation of a single Fund object identified by its id field
* As a bonus, write one or more automated tests within the Django app, checking that some of the specs above are working. Tests can be run with the command manage.py test
