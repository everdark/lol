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
+ The base image
The elasticsearch and logstash image are built on top of the base image, 
which in turn is built on a minimal `ubuntu:14.04` with utilities of `openjdk`, `wget`, and `unzip`.
So build the base image first by:
```
cd docker/base
docker build -t baseimg .
```

+ The elasticsearch image
After base image was built, try:
```
cd ../docker/elasticsearch && docker build -t elastic .
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

+ The logstash image
After base image was built, try:
```
cd ../docker/logstash && docker build -t logstash .
```

+ The kibana image
The kibana docker image is directly built from `ubuntu:14.04` so there is no need to build the base image in advance.
Simply `cd docker/kibana && docker build -t kibana .` will do the job.
You would possibly like to configure the file `config/kibana.yml` to meet your environment setup before the actual build.
After image is built, to start the kibana server:
```
docker run -d --net=host kibana
```
Notice that `host` mode networking is used so the kibana ip will be bind to your docker host, with default port 5601.
The default `bridge` mode tends to cause trouble in node.js so is avoided.



