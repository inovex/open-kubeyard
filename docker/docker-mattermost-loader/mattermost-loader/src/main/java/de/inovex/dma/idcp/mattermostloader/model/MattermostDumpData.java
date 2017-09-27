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


public class MattermostDumpData {
	
	private String id;
	private long create_at;
	private long update_at;
	private long edit_at;
	private long delete_at;
	private boolean is_pinned;
	private String user_id;
	private String channel_id;
	private String root_id;
	private String parent_id;
	private String original_id;
	private String message;
	//type needs to be called _mm because logstash has a secure attribute type that conflicts otherwise
	private String type_mm;
	private String hashtags;
	private String pending_post_id;
	private String first_name;
	private String last_name;
	private String username;
	private String channel_name;

	public MattermostDumpData() {}
	
	public MattermostDumpData(HookData data) {
		
		this.setId(data.getPost_id());
		this.setCreate_at(data.getTimestamp());
		this.setUpdate_at(data.getTimestamp());
		this.setEdit_at(0);
		this.setDelete_at(0);
		this.setIs_pinned(false);
		this.setUser_id(data.getUser_id());
		this.setChannel_id(data.getChannel_id());
		this.setRoot_id("");
		this.setParent_id("");
		this.setOriginal_id("");
		this.setMessage(data.getText());
		this.setType_mm("");
		this.setHashtags("");
		this.setPending_post_id("");
		this.setFirst_name("");
		this.setLast_name("");
		this.setUsername(data.getUser_name());
		this.setChannel_name(data.getChannel_name());
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public long getCreate_at() {
		return create_at;
	}

	public void setCreate_at(long create_at) {
		this.create_at = create_at;
	}

	public long getUpdate_at() {
		return update_at;
	}

	public void setUpdate_at(long update_at) {
		this.update_at = update_at;
	}

	public long getEdit_at() {
		return edit_at;
	}

	public void setEdit_at(long edit_at) {
		this.edit_at = edit_at;
	}

	public long getDelete_at() {
		return delete_at;
	}

	public void setDelete_at(long delete_at) {
		this.delete_at = delete_at;
	}

	public boolean isIs_pinned() {
		return is_pinned;
	}

	public void setIs_pinned(boolean is_pinned) {
		this.is_pinned = is_pinned;
	}

	public String getUser_id() {
		return user_id;
	}

	public void setUser_id(String user_id) {
		this.user_id = user_id;
	}

	public String getChannel_id() {
		return channel_id;
	}

	public void setChannel_id(String channel_id) {
		this.channel_id = channel_id;
	}

	public String getRoot_id() {
		return root_id;
	}

	public void setRoot_id(String root_id) {
		this.root_id = root_id;
	}

	public String getParent_id() {
		return parent_id;
	}

	public void setParent_id(String parent_id) {
		this.parent_id = parent_id;
	}

	public String getOriginal_id() {
		return original_id;
	}

	public void setOriginal_id(String original_id) {
		this.original_id = original_id;
	}

	public String getMessage() {
		return message;
	}

	public void setMessage(String message) {
		this.message = message;
	}

	public String getType_mm() {
		return type_mm;
	}

	public void setType_mm(String type) {
		this.type_mm = type;
	}

	public String getHashtags() {
		return hashtags;
	}

	public void setHashtags(String hashtags) {
		this.hashtags = hashtags;
	}

	public String getPending_post_id() {
		return pending_post_id;
	}

	public void setPending_post_id(String pending_post_id) {
		this.pending_post_id = pending_post_id;
	}

	public String getFirst_name() {
		return first_name;
	}

	public void setFirst_name(String first_name) {
		this.first_name = first_name;
	}

	public String getLast_name() {
		return last_name;
	}

	public void setLast_name(String last_name) {
		this.last_name = last_name;
	}

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}

	public String getChannel_name() {
		return channel_name;
	}

	public void setChannel_name(String channel_name) {
		this.channel_name = channel_name;
	}
	
	
}
