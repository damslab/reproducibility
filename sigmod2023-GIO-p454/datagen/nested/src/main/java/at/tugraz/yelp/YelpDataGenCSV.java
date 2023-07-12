package at.tugraz.yelp;

import at.tugraz.util.GenerateData;
import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;

public class YelpDataGenCSV extends GenerateData {

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

	public YelpDataGenCSV(String path) {
		this.userPath = path + "/yelp_academic_dataset_user.json";
		this.businessPath = path + "/yelp_academic_dataset_business.json";
		this.checkinPath = path + "/yelp_academic_dataset_checkin.json";
		//this.photoPath = path + "/yelp_academic_dataset_photo.json";
		this.reviewPath = path + "/yelp_academic_dataset_review.json";

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

	public static void main(String[] args) throws IOException, InterruptedException {
		mainGenerateData(args, "yelp");
		createDataFile("yelp","csv");

		Gson gson = new Gson();
		try(BufferedReader br = new BufferedReader(new FileReader(inDataPath+"/yelp_academic_dataset_review.json"))) {
			String line;
			while((line = br.readLine()) != null) {
				Review review = gson.fromJson(line, Review.class);
				dataFileHandler.write(review.getCSV());
				dataFileHandler.write("\n");
			}
		}

		flushFileHandlers();
	}
}
