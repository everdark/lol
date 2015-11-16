
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
                        "type": "long"
                        },
                    "matchMode": {
                        "type": "string"
                        },
                    "matchType": {
                        "type": "string"
                        },
                    "matchVersion": {
                        "type": "string"
                        },
                    "queueType": {
                        "type": "string"
                        },
                    "mapId": {
                        "type": "long"
                        },
                    "season": {
                        "type": "string"
                        },
                    "region": {
                        "type": "string"
                        },
                    "platformId": {
                        "type": "string"
                        },
                    "participantIdentities": {
                        "type": "nested",
                        "properties": {
                            "player":        {"type": "nested"},
                            "participantId": {"type": "long"}
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
                "filter": {
                    "term": {
                        "queueType": "RANKED_SOLO_5x5"
                        }
                    } 
                },
            "%s_normalgame" % index_name: {
                "filter": {
                    "term": {
                        "queueType": "NORMAL_5x5_BLIND"
                        }
                    }
                },
            "%s_aram" % index_name: {
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



