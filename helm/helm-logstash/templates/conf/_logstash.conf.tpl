input {
  kafka {
    bootstrap_servers => "kafka:9092"
    topics => ['test']
  }
}

filter {
  mutate {
    #the standard configuration sets the raw input to message
    #the json also contains a messagefield so we have to rename the
    #standard one bfore parsing the json
    rename => { "message" => "jsonsource" }
  }
  json {
    source => "jsonsource"
  }
}


output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
  }
}
