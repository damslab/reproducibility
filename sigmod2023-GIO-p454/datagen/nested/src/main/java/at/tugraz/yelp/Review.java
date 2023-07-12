package at.tugraz.yelp;

import at.tugraz.util.RootData;

public class Review extends RootData {
	private String review_id;
	private String user_id;
	private String business_id;
	private String stars;
	private String date;
	private Business business;
	private User user;
	private Integer useful;
	private Integer funny;
	private Integer cool;
	private String text;

	public String getReview_id() {
		return review_id;
	}

	public String getCSV(){
		StringBuilder sb = new StringBuilder();
		sb.append(review_id).append("\t");
		sb.append(user_id).append("\t");
		sb.append(business_id).append("\t");
		sb.append(stars).append("\t");
		sb.append(date).append("\t");
		sb.append(useful).append("\t");
		sb.append(funny).append("\t");
		sb.append(cool).append("\t");
		sb.append(text.replace("\n", "").replace("\r", "").replace("\"",""));

		return sb.toString();
	}

	public void setReview_id(String review_id) {
		this.review_id = review_id;
	}

	public String getUser_id() {
		return user_id;
	}

	public void setUser_id(String user_id) {
		this.user_id = user_id;
	}

	public String getBusiness_id() {
		return business_id;
	}

	public void setBusiness_id(String business_id) {
		this.business_id = business_id;
	}

	public String getStars() {
		return stars;
	}

	public void setStars(String stars) {
		this.stars = stars;
	}

	public String getDate() {
		return date;
	}

	public void setDate(String date) {
		this.date = date;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public Integer getUseful() {
		return useful;
	}

	public void setUseful(Integer useful) {
		this.useful = useful;
	}

	public Integer getFunny() {
		return funny;
	}

	public void setFunny(Integer funny) {
		this.funny = funny;
	}

	public Integer getCool() {
		return cool;
	}

	public void setCool(Integer cool) {
		this.cool = cool;
	}

	public Business getBusiness() {
		return business;
	}

	public void setBusiness(Business business) {
		this.business = business;
	}

	public User getUser() {
		return user;
	}

	public void setUser(User user) {
		this.user = user;
	}
}
