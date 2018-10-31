## LOGS Analysis Project

### Introduction
This is a project where your work is to analyse data with SQL queris from a huge database of a newspaper site to answer 3 question.
>1. What are the most popular three articles of all time?
>2. Who are the most popular article authors of all time? 
>3. On which days did more than 1% of requests lead to errors?

#### The Database
The database contains 3 tables Articles, Authors & log. Each table are arranged with a primary key and foreign key relationship among them. The data can be found [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

### Running the program

#### Requirements
* Linux Environment 
* Python
* Postgre SQL

If you are using a virtual machine you can donwload the VM configuration file for this project [here](https://github.com/udacity/fullstack-nanodegree-vm).

#### Loading the data
To load the data, `cd` into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`.
Here's what this command does:

* `psql` — the PostgreSQL command line program
* `-d news` — connect to the database named news which has been set up for you
* `-f newsdata.sql` — run the SQL statements in the file newsdata.sql

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

#### Creating Views

After connecting with the database run the following sql code to create neccessery vies to run the program.
```
create view map as select authors.name,articles.slug
  from authors join articles on articles.author = authors.id;

create view visit as select time::date as day,status from log;

create view performance as select v.day,v.requests,f.error
 from (select day,count(status) as error
 from visit where status like ('%404%') group by day) f 
 join (select day,count(status) requests from visit group by day) v
   on  v.day = f.day;
```

#### Running the script
```
python2 new.py
```
This will present all the three questions above in a nice format.
