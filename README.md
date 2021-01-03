# Final course assignment



 ```
Students:

Antonis Kalampogias P18050
Thodoris Charalampopoulos P18169
 ```



We have developed 2 major parts for the project miniDB

- [x] Server - Client (Difficulty 3)

- [x] SQL Compiler (Difficulty 2)

## Server - Client

This program consists of 2 files 

```
Server.py
Client.py
```



### Server.py

will be the main file for executing and delivering the query to the client

Here the code creates a socket connection on the users pc and upon connection from another socket, it calls the miniDB desired source code to execute the message as a query and then transmit the results of the query to the inbound connection.



### Client.py

This is the second part of the project that upon startup will try to connect to the port *Server.py* is on, if this statement is true *Server* will begin the execution of the received query and will send to the Receiver the results.



## SQL Compiler

This program consists of 1 file 

```
SQLcompiler.py
```

Examples on how to use

```sql
1. create database Example
2. create table exampleTable ( Name varchar, Age int, Address varchar)
3. select * from exampleTable
4. drop database Example
```

This function will basically implement the basic functions one can encounter in any SQL compiler available on the market.

**IMPORTANT NOTE** 

Please bare in mind that for the compiler to successfully execute all of your queries, you will have to pay attention to your spacings, for example notice from the above examples `2.`. Notice the spaces applied between the name of the table as well as the spaces inside the parenthesis and the commas, this is because the compiler looks for words individually between the spaces and commas to understand what it is to be done.