# lol
This repo is in early beta and hence is highly dynamic.

### System dependencies

+ ~~[Redis](http://redis.io)~~
+ ~~[mongoDB](https://www.mongodb.org)~~
+ [elasticsearch](https://www.elastic.co): The backend of the system.
+ [logstash](https://www.elastic.co/products/logstash)
+ [docker](https://www.docker.com)
+ [Python2.7](https://www.python.org/download/releases/2.7/): General purpose language chosen to implement the infrastructure.
+ Python modules
    + [`requests`](http://docs.python-requests.org/en/latest/)
    + [`python-daemon`](https://pypi.python.org/pypi/python-daemon/)
    + ~~[`redis`](https://pypi.python.org/pypi/redis)~~
    + ~~[`pymongo`](https://api.mongodb.org/python/current/)~~
    + [`elasticsearch`](https://elasticsearch-py.readthedocs.org)
+ [R 3.2.*](https://www.r-project.org): Used for analytics.
+ R packages
    + [`elastic`](https://cran.r-project.org/package=elastic)
    + [`magrittr`](https://cran.r-project.org/web/packages/magrittr/vignettes/magrittr.html)
    + [`data.table`](https://github.com/Rdatatable/data.table)


### docker

+ Build the elasticsearch docker image
```
cd docker
docker build -t elastic .
```
You may want to edit the config files under `docker/config` in advance to meet your environment setup.
After that, the image can be run with:
```
docker run -Pd elastic
```
To test the elasitsearch on-the-fly, try `docker run -it elastic bash` and paly around within the container. 
The initial user `elastic` is a sudoer so you may want to `sudo su` with the default passwd "elastic" to switch to `root`.



