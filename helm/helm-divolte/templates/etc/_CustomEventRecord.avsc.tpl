{
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
