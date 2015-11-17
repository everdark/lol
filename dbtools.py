
def initElasticIndices(es, index_name="match", doc_type="details"):
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
            }, 
        "mappings": {
            doc_type: {
                "dynamic_templates": [
                    { "default_string_mapping": {
                        "match_mapping_type": "string",
                        "mapping": {
                            "type":  "string",
                            "index": "not_analyzed"
                            }
                        }},
                    { "default_object_mapping": {
                        "match_mapping_type": "object",
                        "mapping": {
                            "type": "object"
                            }
                        }}
                    ],
                "properties": {
                    "insertTime": {
                        "type":   "date",
                        "format": "epoch_millis"
                        },
                    "matchCreation": {
                        "type":   "date",
                        "format": "epoch_millis"
                        },
                    "matchDuration": {
                        "type": "integer"
                        },
                    "matchMode": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                    "matchType": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                    "matchVersion": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                    "queueType": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                    "mapId": {
                        "type": "integer"
                        },
                    "season": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                    "region": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                    "platformId": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                    "participantIdentities": {
                        "type": "nested",
                        "properties": {
                            "player":        {"type": "nested"},
                            "participantId": {"type": "integer"}
                            }
                        },
                    "participants": {
                        "type": "object"
                        },
                    "teams": {
                        "type": "object"
                        },
                    "timeline": {
                        "type": "object"
                        }
                    }
                }
            },
        "aliases": {
            "%s_solorank" % index_name: {
                "routing": "RANKED_SOLO_5x5",
                "filter": {
                    "term": {
                        "queueType": "RANKED_SOLO_5x5"
                        }
                    } 
                },
            "%s_normalgame" % index_name: {
                "routing": "NORMAL_5x5_BLIND",
                "filter": {
                    "term": {
                        "queueType": "NORMAL_5x5_BLIND"
                        }
                    }
                },
            "%s_aram" % index_name: {
                "routing": "ARAM_5x5",
                "filter": {
                    "term": {
                        "queueType": "ARAM_5x5"
                        }
                    }
                }
            }
        }
    es.indices.create(index=index_name, body=index_settings)
    return None



