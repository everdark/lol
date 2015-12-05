# lol
This repo is in early beta and hence is highly dynamic.

### System dependencies

+ ~~[Redis](http://redis.io)~~
+ ~~[mongoDB](https://www.mongodb.org)~~
+ The ELK stack
    + [elasticsearch](https://www.elastic.co/products/elasticsearch)
    + [logstash](https://www.elastic.co/products/logstash)
    + [kibana](https://www.elastic.co/products/kibana)
+ [Docker](https://www.docker.com) and [docker-compose](https://docs.docker.com/compose)
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

### How to start

The entire system is built on multiple docker containers with docker-compose.
To start the entire system, simply run:
```
docker build -t baseimg ./base
docker-compose up -d
```
The default path to elasticsearch data is `/mnt/data/elasticsearch`,
and the default path to temporary file dumps from crawler is `/mnt/data/logstash`.
You propably would like to change these two pathes in `docker-compose.yml` before running the system.

### Docker images
#### `baseimg`

Built on a minimal `ubuntu:14.04` with utilities of `openjdk`, `wget`, `curl`, and `unzip`.
This `baseimg` image must be built before running `docker-compose`.
Build the image by:
```
cd docker/base
docker build -t baseimg .
```
The `elastic` and `logstash` images are both built on top of the `baseimg`. 

#### `crawler`

To run the crawler (written in python) against [RIOT API server](https://developer.riotgames.com/).
Built on official [`python:2.7`](https://hub.docker.com/_/python/) image, 
with modules mentioned in [System Dependencies](### System dependencies) all installed.
The image will be auto built by `docker-compose up -d`. 

By default, any crawled results will be dumped to path `/mnt/data/logstash` in hourly file rotation manner,
and will auto purge after 7 days.
You can change the behavior in `crawlertools.py` before starting the system.

#### `elastic`

The image of elasticsearch installation.
You may want to edit config files under `config` in advance to meet your environment setup.
The image will be auto built by `docker-compose up -d`. 

#### `logstash`

The image of logstash installation.
The image will be auto built by `docker-compose up -d`.

The logstash container uses file input to insert data from file dumped by `crawler` in `/mnt/data/logstash`,
to `elastic` container where the actuall index data will be stored at `/mnt/data/elasticsearch`.
You can adjust the behavior of logstash by editing the file under `logstash/config`.

When there is no index predefined (the ground-zero case) at `elastic`, 
the `logstash` image is also responsible to create one.
See `/logstash/entrypoint_create_index.sh` for more details.

#### `kibana`

The image is directly pulled from [official kibana docker hub](https://hub.docker.com/_/kibana/).
The image will be auto built by `docker-compose up -d`.

To visit kibana web portal, try hit `127.0.0.1:5601`. 



