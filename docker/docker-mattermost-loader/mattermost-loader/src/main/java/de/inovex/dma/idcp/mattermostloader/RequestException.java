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

public class RequestException extends Exception {
	
	private static final long serialVersionUID = -7848499291203617724L;
	private int htmlErrorCode = -1;
	
	public RequestException(String message, int htmlErrorCode){
		super(message);
		this.htmlErrorCode = htmlErrorCode;
	}
	
	public RequestException(String message){
		super(message);
	}
	
	public int getHTMLErrorCode(){
		return this.htmlErrorCode;
	}
	
}
