divolte {
  global {
    server {
      host = 0.0.0.0
      port = {{ default 8290 .Values.port }}
      use_x_forwarded_for = false
      serve_static_resources = true
    }
    mapper {
      threads = 2
      user_agent_parser {
        type = non_updating
        cache_size = 1000
      }
      duplicate_memory_size = 1000000
      ip2geo_database = "/var/lib/divolte/ip2geo/GeoLite2-City.mmdb"
    }
    kafka {
      enabled = true
      threads = 2
      buffer_size = 1048576
      producer = {
        bootstrap.servers = "{{ default "kafka" .Values.kafka.hosts.name }}.kubeyard:{{ default "9092" .Values.kafka.hosts.port }}"
        client.id = divolte.collector
        compression.type = gzip
        acks = 0
        retries = 5
      }
    }
    hdfs {
      enabled = false
      threads = 2
      client {
      }
		}
  }
  sources {
    browser = {
      type = browser
      party_cookie = _dvp
      party_timeout = 730 days
      session_cookie = _dvs
      session_timeout = 30 minutes
      cookie_domain = ""
      javascript {
        name = divolte.js
        logging = false
        debug = false
        auto_page_view_event = true
      }
    }
    app = {
      type = json
    }
  }
  mappings {
    custom_mapping = {
      schema_file = /etc/divolte-collector/CustomEventRecord.avsc
      mapping_script_file = /etc/divolte-collector/custom-mapping.groovy
      sources = [browser,app]
      sinks = [hdfs,kafka]
    }
  }
  sinks {
    kafka = {
      type = kafka
      topic = "divolte"
    }
    hdfs = {
      type = hdfs
      file_strategy {
        roll_every = 60 minutes
        sync_file_after_records = 1000
        sync_file_after_duration = 30 seconds
        working_dir = /tmp
        publish_dir = /tmp
      }
      replication = 1
    }
  }
}
