package at.tugraz.yelp;

import at.tugraz.util.GenerateData;
import com.google.gson.Gson;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class YelpDataGen extends GenerateData {

	private String userPath;
	private String businessPath;
	private String checkinPath;
	//private String photoPath;
	private String reviewPath;

	private HashMap<String, User> userMap = new HashMap<>();
	private HashMap<String, Business> businessMap = new HashMap<>();
	private HashMap<String, Checkin> checkinMap = new HashMap<>();
	//private HashMap<String, Photo> photoMap = new HashMap<>();

	private Gson gson = new Gson();

	public YelpDataGen(String business, String checkin, String review, String user) {
		this.userPath = user;
		this.businessPath = business;
		this.checkinPath = checkin;
		//this.photoPath = path + "/yelp_academic_dataset_photo.json";
		this.reviewPath = review;

		userData();
		checkinData();
		//photoData();
		businessData();

	}

	private void userData() {
		try(BufferedReader br = new BufferedReader(new FileReader(userPath))) {
			String line;
			while((line = br.readLine()) != null) {
				User user = gson.fromJson(line, User.class);
				userMap.put(user.getUser_id(), user);
			}
		}
		catch(Exception e) {
			throw new RuntimeException(e);
		}
	}

	private void checkinData() {
		try(BufferedReader br = new BufferedReader(new FileReader(checkinPath))) {
			String line;
			while((line = br.readLine()) != null) {
				Checkin checkin = gson.fromJson(line, Checkin.class);
				checkinMap.put(checkin.getBusiness_id(), checkin);
				checkin.setBusiness_id(null);
			}
		}
		catch(Exception e) {
			throw new RuntimeException(e);
		}
	}

//	private void photoData() {
//		try(BufferedReader br = new BufferedReader(new FileReader(photoPath))) {
//			String line;
//			while((line = br.readLine()) != null) {
//				Photo photo = gson.fromJson(line, Photo.class);
//				photoMap.put(photo.getBusiness_id(), photo);
//				photo.setBusiness_id(null);
//			}
//		}
//		catch(Exception e) {
//			throw new RuntimeException(e);
//		}
//	}

	private void businessData() {
		try(BufferedReader br = new BufferedReader(new FileReader(businessPath))) {
			String line;
			while((line = br.readLine()) != null) {
				Business business = gson.fromJson(line, Business.class);
				Checkin checkin = checkinMap.get(business.getBusiness_id());
				//Photo photo = photoMap.get(business.getBusiness_id());
				//if(checkin == null )
				//	throw new RuntimeException("there is no check in");
				business.setCheckin(checkin);
				businessMap.put(business.getBusiness_id(), business);
			}
		}
		catch(Exception e) {
			throw new RuntimeException(e);
		}
	}

	public String getReviewPath() {
		return reviewPath;
	}

	public HashMap<String, User> getUserMap() {
		return userMap;
	}

	public HashMap<String, Business> getBusinessMap() {
		return businessMap;
	}

	public HashMap<String, Checkin> getCheckinMap() {
		return checkinMap;
	}

//	public HashMap<String, Photo> getPhotoMap() {
//		return photoMap;
//	}

	public static void main(String[] args) throws IOException, InterruptedException {
		String in_yelp_business = args[0];
		String in_yelp_checkin = args[1];
		String in_yelp_review = args[2];
		String in_yelp_user = args[3];
		outDataPath = args[4];

		createDataFile("yelp","json");
		YelpDataGen yelp = new YelpDataGen(in_yelp_business, in_yelp_checkin, in_yelp_review, in_yelp_user);

		Gson gson = new Gson();
		Map<String, User> userMap = yelp.getUserMap();
		Map<String, Business> businessMap = yelp.getBusinessMap();
		try(BufferedReader br = new BufferedReader(new FileReader(yelp.reviewPath))) {
			String line;
			while((line = br.readLine()) != null) {
				Review review = gson.fromJson(line, Review.class);
				User user = userMap.get(review.getUser_id());
				Business business = businessMap.get(review.getBusiness_id());
				review.setUser_id(null);
				review.setBusiness_id(null);
				review.setBusiness(business);
				review.setUser(user);
				dataFileHandler.write(gson.toJson(review));
				dataFileHandler.write("\n");
			}
		}

		flushFileHandlers();
	}
}
