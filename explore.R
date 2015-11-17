#!/usr/bin/env Rscript

library(elastic)
library(magrittr)
library(data.table)

readIniConfig <- function(fname) {
    if ( !file.exists(fname) )
        stop(sprintf("File %s not found.", fname))
    conf <- read.table(fname, sep='=', fill=TRUE, header=FALSE, strip.white=TRUE,
                       col.names=c("key", "val"), stringsAsFactors=FALSE, comment.char=";")
    section_pos <- grepl("^\\[.*\\]$", conf$key)
    section_name <- gsub("\\[|\\]", '', conf$key[section_pos])
    conf <- split(conf, cumsum(section_pos))
    names(conf) <- section_name
    lapply(conf, function(x) setNames(x$val, x$key)[-1])
}

scrollAll <- function(res) {
    dat <- list()
    repeat {
        res <- elastic::scroll(res$`_scroll_id`)
        hits <- res$hits$hits
        if ( !length(hits) ) 
            break
        dat <- c(dat, res$hits$hits)
    }
    dat
}

config <- readIniConfig("conf.ini")
connect(es_base=config$database["elasticsearch_host"],
        es_port=config$database["elasticsearch_port"])


#### some test run

## get time info
timeinfo <- Search(index="match1", type="details", fields=c("insertTime", "matchCreation"),
                   search_type="scan", scroll="1m", size=1000) %>% 
            scrollAll %>% {
                do.call(rbind, lapply(., function(x) unlist(x$fields))) / 1000
            } %>%
            as.data.table
timeinfo %<>% .[, matchCreation:=as.POSIXct(matchCreation, origin="1970-01-01")]

# match-creation traffics per second
count_by_sec <- timeinfo[, .N, by=createTime] %T>% setkey(., createTime)
plot(count_by_sec, type='l')


## how many distinct players?
query <- '
{
    "_source": [ "participantIdentities" ],
    "query": {
        "filtered": {
            "query": {
                "match_all": {}
            },
            "filter": {
                "term" : { "queueType": "RANKED_SOLO_5x5" }
            }
        }
    }
}'

system.time( # 100 records need 15 sec on pi
players <- Search("match", "details", body=query, size=100)
)
pp <- lapply(players$hits$hits, function(x) x$`_source`$participantIdentities) %>%
{
    lapply(., function(x) 
           sapply(x, function(y) y$player$summonerId))
}

system.time( # scroll over 45,000 docs: 1411 sec 
players <-  Search(index="match", type="details", body=query,
                   search_type="scan", scroll="1m", size=1000) %>% scrollAll
)

