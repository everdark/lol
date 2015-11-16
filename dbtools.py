
def initElasticIndices(es, index_name="match"):
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
            }, 
        "mappings": {
            "details": {
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
                            "type": "nested"
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
                        "type": "nested"
                        },
                    "participants": {
                        "type": "nested"
                        },
                    "teams": {
                        "type": "nested"
                        },
                    "timeline": {
                        "type": "nested"
                        }
                    }
                }
            },
            # soure filtering in alias is NOT working
        "aliases": {
            "brief": {
                "_source": [ "matchCreation", 
                            "matchDuration", 
                            "matchMode",
                            "matchType",
                            "matchVersion",
                            "queueType",
                            "mapId",
                            "season",
                            "region",
                            "platformId"]
                }
            }
        }
    # alias_settings = {}
    es.indices.create(index=index_name, body=index_settings)
    # es.indices.put_alias(index=index_name, name="brief", body=alias_settings)
    return None



