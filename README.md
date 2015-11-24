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


### Docker

Build the base image (a minimal `ubnutu:14.04` with `openjdk`, `wget`, and `unzip` utilities) first:
```
cd docker/base
docker build -t baseimg .
```
Then the other images can be built accordingly:
```
cd ../docker/elasticsearch && docker build -t elastic .
cd ../docker/logstash && docker build -t logstash .
cd ../docker/kibana && docker build -t kibana .
```
You may want to edit any config file under `config` in advance to meet your environment setup.
After that, the image can be run with, for example, the elasticsearch image:
```
docker run -Pd elastic
```
To test the elasitsearch on-the-fly, try `docker run -it elastic bash` and play around within the container. 
The initial user `elastic` is a sudoer so you may want to `sudo su` with the default passwd "elastic" to switch to `root`.
The other images have similar setup.
For more details, see the `Dockerfile` in each folder.



