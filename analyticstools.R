
library(elastic)
library(magrittr)
library(data.table)
library(jsonlite)

############################
## define helper functions #
############################
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

searchWithBody <- function(index, type, body, size) {
    res <-
        if ( is.null(size) ) {
            Search(index=index, type=type, body=body,
                   search_type="scan", scroll="1m", size=1000) %>% scrollAll
        } else {
            Search(index=index, type=type, body=body, size=size)$hits$hits
        }
    res
}

checkStaticFile <- function() {
    if ( !file.exists("statics/champion_id.json") )
        system("./dump_statics_champ.py")
    if ( !file.exists("statics/item.json") )
        system("./dump_statics_item.py")
}

getChampionIdByName <- function(champ_name, champ_table=champion_id) {
    out <- integer(0)
    for ( ch in champ_name ) {
        res <- champ_table[grep(ch, name, ignore.case=TRUE)]
        nr <- nrow(res)
        if ( nr == 1 ) {
            out <- c(out, res$id)
        } else if ( nr > 1 ) {
            stop(sprintf("Champion name '%s' ambiguous to uniquely identify a champion.", ch))
        } else {
            stop(sprintf("No champion identified by given name '%s'.", ch))
        }
    }
    out
}

getMatchByChampion <- function(champ, keep=NULL, size=NULL) {
    if ( !is.numeric(champ) )
        champ <- getChampionIdByName(champ)
    term <- 
        if ( length(champ) == 1 ) {
            sprintf('"term" : { "participants.championId": %s }', champ)
        } else {
            sprintf('"terms" : { "participants.championId": [%s] }', 
                    paste(champ, collapse=','))
        }
    source_filter <- 
        paste('"_source": ',
        if ( !is.null(keep) ) {
            paste0('[', paste(sprintf('"%s"', keep), collapse=','), ']')
        } else {
            "true"
        }, collapse='')
    query <- sprintf('
    {
        %s,
        "query": {
            "filtered": {
                "query": {
                    "match_all": {}
                },
                "filter": {
                    %s
                }
            }
        }
    }', source_filter, term)
    res <- searchWithBody(index="match", type="details", body=query, size=size)
    res
}

getItemsByChampion <- function(champ, size=NULL) {
    stats <- getMatchByChampion(champ=champ, size=size) %>%
        lapply(function(x) x$`_source`$participants) %>%
        lapply(function(x) 
               x[sapply(x, function(y) 
                           y$championId == getChampionIdByName(champ))]) %>%
        lapply(function(x) x[[1]]$stats) %>%
        rbindlist(fill=TRUE)
    stats[, grep("item", names(stats)), with=FALSE]
}

###########################
## define helper objects ##
###########################
config <- readIniConfig("config/conf.ini")
checkStaticFile()
champion_id <- as.data.table(stream_in(file(config$static["champion_id"])))
item_id <- as.data.table(stream_in(file(config$static["item"])))



