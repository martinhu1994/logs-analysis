# Logs Analysis
This is a SQL-based project. Given a set of data from a newspaper site, I built a tool to discover what kind of articles the site's readers like.

## Prerequisites
In order to run my project successfully and get consistent result, you need to set up working environment and load data into database.
#### Installing Virtual Machine
You will need to install two tools, `Virtual Box` and `Vagrant`. `Virtual Box` is the software that actually runs the virtual machine and `Vagrant` is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.
1. Download `Virtual Box` [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) with version 5.1 for your operating system and install it. You only need _platform package_. You do not need the extension pack or the SDK. 
2. Download `Vagrant` [here](https://www.vagrantup.com/downloads.html) for your operating system and install it. 
3. Download the VM configuration [here](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip). Unzip the package and you will get a directory `FSND-Virtual-Machine`.
4. Open a shell and change working directory to `FSND-Virtual-Machine/vagrant` and run
```
$ vagrant up
```
This command will cause `Vagrant` to download the Linux operating system and install it. This may take quite a while.

5. When the installation is finished, you can run 
```
$ vagrant ssh
```
This command logs you into the Linux VM you just installed. You will see the shell prompt starting with **vagrant**.
#### Populating Data
1. Download data from this [link](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). 
2. Unzip the package and you will get a `newsdata.sql` file. Place this file under `FSND-Virtual-Machine/vagrant` directory in your host machine, and it will be accessible to your virtual machine.  
3. Login to your vagrant virtual machine with `$ vagrant ssh` command if you logged out and execute
```
$ cd /vagrant
$ psql -d news -f newsdata.sql
```
Note: you don't need to worry about the installation of database, since the PostgreSQL database comes along with the the Linux system that you installed on your virtual machine, and `news` database is already there. 
## Program Design
#### Tables in Database 
There are three tables in the `news` database:
* authors -- information about the authors of articles, includes `name`, `bio`, and `id` attributes
* articles -- the articles themselves, includes `author`, `title`, `slug`, `lead`, `body`, `time`, and `id` attributes
* log -- one entry for each time a user has accessed the site, includes `path`, `ip`, `method`, `status`, `time`, and `id` attributes
#### Functions in Source Code
The source code file is `analysis.py`, which includes three functions generating simple reports. In the first function, I join the view `articleviews`(you will see how to get it in the following **Usage** section) with table `articles`. In the second function, I join the view `articleviews`, table `articles`, and table `authors` all together. In the last function, I join the results from two sub queries and do calculation. The result from database are processed and my tool prints out formatted reports. 

## Usage
Please follow the steps below to generate the reports:
1. Clone or download my repository and place the whole directory under `FSND-Virtual-Machine/vagrant` directory on your host machine
2. Login to your virtual machine with a shell by executing
```
$ vagrant ssh
```
3. Connect to `news` database
```
$ psql -d news
```
4. Create the view `articleviews` with following query  
```
CREATE VIEW articleviews AS 
  SELECT substring(path from length('/article/') + 1) AS slug, count(*) AS views 
  FROM log 
  WHERE path != '/' AND method = 'GET' AND status = '200 OK' 
  GROUP BY slug
```
5. Disconnect with database and change the shell working directory
```
$ cd /vagrant/logs-analysis
```
6. Run the `analysis.py` script 
```
$ python analysis.py
```
