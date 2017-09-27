{
  "dataSources": [
    {
      "spec": {
        "dataSchema": {
          "dataSource": "divolte",
          "parser": {
            "type": "avro_stream",
            "avroBytesDecoder": {
              "type": "schema_inline",
              "schema": {
                "namespace": "io.divolte.record",
                "type": "record",
                "name": "CustomEventRecord",
                "fields": [
                  { "name": "timestamp",    "type": "long" },
                  { "name": "remoteHost",   "type": "string"},
                  { "name": "eventType",    "type": ["null", "string"], "default": null },
                  { "name": "location",     "type": ["null", "string"], "default": null },
                  { "name": "referer",      "type": ["null", "string"], "default": null },
                  { "name": "partyId",      "type": ["null", "string"], "default": null },
                  { "name": "sessionId",    "type": ["null", "string"], "default": null },
                  { "name": "pageViewId",   "type": ["null", "string"], "default": null },
                  { "name": "host",         "type": ["null", "string"], "default": null },
                  { "name": "localPath",    "type": ["null", "string"], "default": null },
                  { "name": "queryString",  "type": ["null", "string"], "default": null },
                  { "name": "queryMap",
                    "type": [
                      "null",
                      {
                        "type": "map",
                        "values":
                        {
                          "type": "array",
                          "items": "string"
                        }
                      }
                    ],
                    "default": null
                  },
                  { "name": "paramMap",
                    "type": [
                      "null",
                        {
                          "type": "map",
                          "values": {
                            "type": "array",
                            "items": "string"
                          }
                        }
                      ],
                      "default": null
                  },
                  { "name": "xClientIp", "type": ["null", "string"], "default": null },
                  { "name": "cityId", "type": ["null", "int"], "default": null },
                  { "name": "cityName", "type": ["null", "string"], "default": null },
                  { "name": "continentCode", "type": ["null", "string"], "default": null },
                  { "name": "continentId", "type": ["null", "int"], "default": null },
                  { "name": "continentName", "type": ["null", "string"], "default": null },
                  { "name": "countryCode", "type": ["null", "string"], "default": null },
                  { "name": "countryId", "type": ["null", "int"], "default": null },
                  { "name": "countryName", "type": ["null", "string"], "default": null },
                  { "name": "latitude", "type": ["null", "double"], "default": null },
                  { "name": "longitude", "type": ["null", "double"], "default": null },
                  { "name": "metroCode", "type": ["null", "int"], "default": null },
                  { "name": "timeZone", "type": ["null", "string"], "default": null },
                  { "name": "mostSpecificSubdivisionCode", "type": ["null", "string"], "default": null },
                  { "name": "mostSpecificSubdivisionId", "type": ["null", "int"], "default": null },
                  { "name": "mostSpecificSubdivisionName", "type": ["null", "string"], "default": null },
                  { "name": "postalCode", "type": ["null", "string"], "default": null }
                ]
              }
            },
            "parseSpec": {
              "timestampSpec": {
                "column": "timestamp",
                "format": "auto"
              },
              "dimensionsSpec": {
                "dimensions": [
                  "partyId",
                  "sessionId",
                  "referer",
                  "location",
                  "host",
                  "continentName",
                  "continentCode",
                  "countryName",
                  "countryCode",
                  "cityName",
                  "cityId",
                  "latitude",
                  "longitude"
                ]
              },
              "format": "timeAndDims"
            }
          },
          "granularitySpec": {
            "segmentGranularity": "hour",
            "type": "uniform",
            "queryGranularity": "none"
          },
          "metricsSpec": [
            {
              "type": "count",
              "name": "count"
            },
            {
              "type": "hyperUnique",
              "name": "party_id_met",
              "fieldName": "partyId"
            },
            {
              "type": "hyperUnique",
              "name": "session_id_met",
              "fieldName": "sessionId"
            },
            {
              "type": "hyperUnique",
              "name": "referer_met",
              "fieldName": "referer"
            },
            {
              "type": "hyperUnique",
              "name": "location_met",
              "fieldName": "location"
            },
            {
              "type": "hyperUnique",
              "name": "host_met",
              "fieldName": "host"
            },
            {
              "type": "hyperUnique",
              "name": "continentCode_met",
              "fieldName": "continentCode"
            },
            {
              "type": "hyperUnique",
              "name": "countryCode_met",
              "fieldName": "countryCode"
            },
            {
              "type": "hyperUnique",
              "name": "cityId_met",
              "fieldName": "cityId"
            }
          ]
        },
        "tuningConfig": {
          "type": "realtime",
          "maxRowsInMemory": "100000",
          "intermediatePersistPeriod": "PT10M",
          "windowPeriod": "PT10M"
        }
      },
      "properties": {
        "topicPattern.priority": "1",
        "topicPattern": "divolte"
      }
    }
  ],
  "properties": {
    "zookeeper.connect": "zookeeper.kubeyard:{{ default "2181" .Values.zookeeper.ports.client }}",
    "druid.discovery.curator.path": "/druid/discovery",
    "druid.selectors.indexing.serviceName": "druid/overlord",
    "commit.periodMillis": "15000",
    "consumer.numThreads": "2",
    "kafka.zookeeper.connect": "zookeeper.kubeyard:{{ default "2181" .Values.zookeeper.ports.client }}",
    "kafka.group.id": "tranquility-kafka"
  }
}
