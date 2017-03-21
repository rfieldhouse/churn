# churn
INTRODUCTION

Hi, I'm Robert Fieldhouse and I created ClientKeeper as a short-term project at Insight Data Science. Business relationships are crucial for success, and software for managing those relationships is becoming both more important and more sophisticated. This project involves predicting engagement and churn in business-to-business relationships.

PREREQUISITES

Python 2.7.13
Packages:
os
sys
pickle
datetime
logging
collections
sqlalchemy
mysql.connector
pandas
numpy
matplotlib
prettyplotlib
seaborn
sklearn
glob
qgrid

USAGE

This app is intended for use on a private data set. The pipeline can be started using the launch.sh script. This launcher script converts the jupyter notebooks here into python scripts and runs them to process the data required as input for a visualization dashboard.

The private database requires four environment variables to be set to access the database: UNAME, PASSWD, DBNAME, PORTNUM. Two additional environment variables are required for the visualization dashboard: SOCKETPORT and also STATICDIR.

TOOLS

Front end: Spyre (based on Cherrypy and jinja2)
Back end: Python, MySQL

VERSIONING

Version control using Github.

AUTHOR

Robert Fieldhouse

ACKNOWLEDGEMENTS

Thanks to fellows and program directors at Insight Data Science.

MORE INFO:
Read a project report here:
https://medium.com/@robert.fieldhouse/engagement-and-churn-in-b2b-relationships-97677f4e8704#.3g7tlcwmw