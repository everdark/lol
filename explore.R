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

query <- "queueType:NORMAL_5x5_BLIND"
res <- Search(index="match", type="details", fields=NULL,
              default_operator="AND", q=query, 
              search_type="scan", scroll="1m", size=100) %>% scrollAll

timeinfo <- Search(index="match", type="timeinfo", search_type="scan", scroll="1m", size=100) %>% 
            scrollAll %>%
            lapply(function(x) x$`_source`) %>%
            rbindlist
max(table(timeinfo$createTime)) # maximum number of games per second

