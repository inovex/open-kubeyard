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

package de.inovex.dma.idcp.mattermostloader.model;

/**
 * Represents the cleaned data with all the unwanted information removed
 *
 */
public class CleanHookData {

	private String channel_name;
	private String post_id;
	private String user_id;
	private String user_name;
	private String team_domain;
	private String team_id;
	private String text;
	private String channel_id;
	private long timestamp;
	
	
	public CleanHookData() {}

	public CleanHookData(HookData data){
		this.setChannel_name(data.getChannel_name());
		this.setChannel_id(data.getChannel_id());
		this.setPost_id(data.getPost_id());
		this.setUser_id(data.getUser_id());
		this.setUser_name(data.getUser_name());
		this.setTeam_domain(data.getTeam_domain());
		this.setTeam_id(data.getTeam_id());
		this.setText(data.getText());
		this.setChannel_id(data.getChannel_id());
		this.setTimestamp(data.getTimestamp());
	}

	public String getChannel_name() {
		return channel_name;
	}

	public void setChannel_name(String channel_name) {
		this.channel_name = channel_name;
	}

	public String getPost_id() {
		return post_id;
	}

	public void setPost_id(String post_id) {
		this.post_id = post_id;
	}

	public String getUser_id() {
		return user_id;
	}

	public void setUser_id(String user_id) {
		this.user_id = user_id;
	}

	public String getUser_name() {
		return user_name;
	}

	public void setUser_name(String user_name) {
		this.user_name = user_name;
	}

	public String getTeam_domain() {
		return team_domain;
	}

	public void setTeam_domain(String team_domain) {
		this.team_domain = team_domain;
	}

	public String getTeam_id() {
		return team_id;
	}

	public void setTeam_id(String team_id) {
		this.team_id = team_id;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public String getChannel_id() {
		return channel_id;
	}

	public void setChannel_id(String channel_id) {
		this.channel_id = channel_id;
	}

	public long getTimestamp() {
		return timestamp;
	}

	public void setTimestamp(long timestamp) {
		this.timestamp = timestamp;
	}

	
}


