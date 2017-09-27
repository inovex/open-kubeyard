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

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import de.inovex.dma.idcp.mattermostloader.model.CleanHookData;
import de.inovex.dma.idcp.mattermostloader.model.HookData;
import de.inovex.dma.idcp.mattermostloader.model.MattermostDumpData;

public class MattermostTransformer {

	private KafkaLogger logger = new KafkaLogger();
	
	public void logHookRecord(HookData record){
		
		//remove unwanted datasets
		CleanHookData clean = new CleanHookData(record);
		
		String json = this.generateJson(clean);
		
		if(json != null){
			logger.log(json);
		}
	}
	
	public void logInDumpFormat(HookData record){
		
		MattermostDumpData dump = new MattermostDumpData(record);
		
		String json = this.generateJson(dump);
		
		if(json != null){
			logger.log(json);
		}
	}
	
	private String generateJson(Object o){
		//Generate JSON String
		ObjectMapper mapper = new ObjectMapper();

		String json = null;
		try {
			json = mapper.writeValueAsString(o);
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		}
		
		return json;
	}
	
	
}
