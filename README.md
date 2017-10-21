# **MicroArticles**
*created by Chris Givanoudis*

----------

### **Description**
MicroArticles is web application that allows users to publish articles and post comments.  The application is using **Microservices Artitecture**. This application is an example for developing **Microservices in Docker**, by using the **Docker** platform. This code base is part of my paper with title *Developing of Microservices in Docker*. This paper was make for my master degree at the **Department of Applied Informatics of University of Macedonia**.  


----------

### **Special Thanks**

I would like to give me special thanks to the people  that help me create this project.

 - My Family
 -  My Professor
 -  The members and students of the Department of Applied Informatics of University of Macedonia

----------

### **Installation**

The appliction needs the **Docker** platform in order to run. Also needs **npm** package of Node.js to build the user interface of the website.

**Docker Install Links**
- [Install Docker on Linux (Ubuntu)](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)
- [Install Docker on Windows](https://docs.docker.com/docker-for-windows/install/)
- [Install Docker on Mac](https://docs.docker.com/docker-for-mac/install/)

**Node.js Install** *(only for user interface build)*
- [Node.js](https://nodejs.org/en/download/)

----------

### **Deploy MicroArticles**
First we need to download the code base or clone it to the local machine.
```sh
git clone https://github.com/chgivan/MicroArticles.git 
```
 When the download is finishes, we can contuine. 


**IF** we want to build the **user interface**, navigate to the **app folder** and run the following command. 
```sh 
npm run build
```
The build files are locating in the **dist folder**.


Back to the root folder of ours project.  We need to build the source code base into **Docker Images**. We can use the **docker-compose.yml** file for this job.

```sh
docker-compose build
```

When the build is complete, we need to switch the Docker to **swarm-mode**.

```sh
docker swarm init –advertise-addr <Docker Host IP>
```
**IF** we are running the docker on a virtual machine through **docker-machine**. we can found the IP with the following command.
```sh 
docker-machine ip
```

**Finally,** we can deploy the application with the command:

```sh
docker stack deploy -c docker-compose.yml app
```

The HTML user interface is available at  your **Docker Host IP**.

Two useful command are **ps** and **rm**. The first prints the info of the Docker Services and the second stop the application.
```sh
docker stack ps app
docker stack rm app
```

### **Useful Links**
 - [Docker](https://www.docker.com/)
 - [Docker Documentation](https://docs.docker.com/)
 - [Docker Hub](https://hub.docker.com/explore/)
 - [Flask (a python Rest API)](http://flask.pocoo.org/)
 - [Pony ORM (a python ORM Framework)](https://ponyorm.com/)
 - [Pymongo (a python MongoDB API)](http://api.mongodb.com/python/current/tutorial.html)
 - [Requests (a python HTTP Requests Library)](http://docs.python-requests.org/en/master/)
 - [Nginx (HTTP Load Balancer)](https://www.nginx.com/)
 - [Vue.js (JS Framework)](https://vuejs.org/)
 - [BootStrap (CSS Framework)](http://getbootstrap.com/)
 - [Node.js (JS Engine)](https://nodejs.org/en/) 

