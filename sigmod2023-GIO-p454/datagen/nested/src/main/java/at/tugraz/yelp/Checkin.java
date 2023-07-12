package at.tugraz.yelp;

import at.tugraz.util.RootData;

public class Checkin extends RootData {
	private String business_id;
	private String data;

	public String getBusiness_id() {
		return business_id;
	}

	public void setBusiness_id(String business_id) {
		this.business_id = business_id;
	}

	public String getData() {
		return data;
	}

	public void setData(String data) {
		this.data = data;
	}
}
