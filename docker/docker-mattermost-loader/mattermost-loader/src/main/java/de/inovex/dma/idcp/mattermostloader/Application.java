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

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
	
	public static String kafkaTopic = "test";
	public static String kafkaConnect = "kafka.kubeyard:9092";

    public static void main(String[] args) {
    	
    	for(int i =0; i < args.length; i++){
    		if(args[i].equals("--kafkatopic")){
    			Application.kafkaTopic = args[i+1];
    			
    		} else if (args[i].equals("--kafkaconnect")){
    			Application.kafkaConnect = args[i+1];
    			
    		}
    		
    	}
    	
    	
    	
    	SpringApplication.run(Application.class, args);
    }
}
/*
--kafkatopic
test
--kafkaconnect
kafka.kubeyard:9092
*/