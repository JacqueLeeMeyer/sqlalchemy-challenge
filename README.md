# sqlalchemy-challenge
Module 10 Challenge

For Challenge 10 I used SQLAlchemy to reflect two tables: **station** and **measurement**.

I used matplotlib to create a graph of all precipitation data for the last 12 months.

![image](https://github.com/JacqueLeeMeyer/sqlalchemy-challenge/assets/149394665/d2090ad6-fc73-4874-a7a0-9d02604091d8)

I also created a histogram using the 12 months of precip data for Station: USC00519281

![image](https://github.com/JacqueLeeMeyer/sqlalchemy-challenge/assets/149394665/06ab6ecf-b48c-459e-a176-9bba9d26dfc5)

I then used FLASK to create an API with the following routes:

> /api/v1.0/precipitation<br/>
> /api/v1.0/stations<br/>
> /api/v1.0/tobs<br/>
> /api/v1.0/<start><br/>
> /api/v1.0/<start>/<end><br/>

Sources used:

https://flask.palletsprojects.com/en/3.0.x/

Module 10 in class work.
