
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

checkStaticFile <- function() {
    if ( !file.exists("statics/champion_id.json") )
        system("./dump_champion_info.py")
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

getMatchByChampion <- function(champ, size=NULL) {
    if ( !is.numeric(champ) )
        champ <- getChampionIdByName(champ)
    term <- 
        if ( length(champ) == 1 ) {
            sprintf('"term" : { "participants.championId": %s }', champ)
        } else {
            sprintf('"terms" : { "participants.championId": [%s] }', 
                    paste(champ, collapse=','))
        }
    query <- sprintf('
    {
        "query": {
            "filtered": {
                "query": {
                    "match_all": {}
                },
                "filter": {
                    "term" : { "participants.championId": %s }
                }
            }
        }
    }', champ)
    res <-
        if ( is.null(size) ) {
            Search(index="match", type="details", body=query,
                   search_type="scan", scroll="1m", size=1000) %>% scrollAll
        } else {
            Search(index="match", type="details", body=query, size=size)$hits$hits
        }
    res
}

###########################
## define helper objects ##
###########################
checkStaticFile()
champion_id <- as.data.table(stream_in(file(config$static["champion_id"])))



