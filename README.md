# Logs Analysis
This is a SQL-based project. Python code is used to connect PostgreSQL database and execute queries. Three simple reports are generated.

## Content
There are two files in the project:
* analysis.py -- source code
* output.txt -- sample report output 

## Usage
In order to generate reports, you need to perform two steps:
1. Please execute the following query first to create a view:  
```
CREATE VIEW articleviews AS 
  SELECT substring(path from length('/article/') + 1) AS slug, count(*) AS views 
  FROM log 
  WHERE path != '/' AND method = 'GET' AND status = '200 OK' 
  GROUP BY slug
```
2. Run the `analysis.py` script:  
```
$ python analysis.py
```
