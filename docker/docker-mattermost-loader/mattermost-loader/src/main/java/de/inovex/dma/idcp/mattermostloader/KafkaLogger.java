//Copyright 2017 inovex GmbH
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.

package de.inovex.dma.idcp.mattermostloader;

import java.util.LinkedList;
import java.util.Properties;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

public class KafkaLogger {
	
	private KafkaProducer<String, String> kafkaProducer = null;
	
	
	public void log(String data) {
		this.createProducer();
		this.logRecord(data);
		this.closeProducer();
	}
	
	public void log(LinkedList<String> data){
		this.createProducer();
		for(String record : data){
			this.logRecord(record);
		}
		this.closeProducer();
	}
	
	private void createProducer(){
		Properties properties = new Properties();
		properties.put("bootstrap.servers", Application.kafkaConnect);
		properties.put("key.serializer", // serializer class for keys
				"org.apache.kafka.common.serialization.StringSerializer");
		properties.put("value.serializer", // serializer class for values
				"org.apache.kafka.common.serialization.StringSerializer");
		
		
		kafkaProducer = new KafkaProducer<>(properties);
	}
	
	private void closeProducer(){
		kafkaProducer.flush();
		kafkaProducer.close();
	}
	
	private void logRecord(String record){
		kafkaProducer.send(new ProducerRecord<String, String>(Application.kafkaTopic, record));
	}
	
	
}



