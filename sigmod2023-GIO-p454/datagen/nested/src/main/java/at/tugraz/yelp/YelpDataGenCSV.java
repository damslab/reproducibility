package at.tugraz.yelp;

import at.tugraz.util.FileHandler;
import at.tugraz.util.GenerateData;
import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class YelpDataGenCSV extends GenerateData {

	public static void main(String[] args) throws IOException {
		inDataPath = args[0];
		outDataPath = args[1];

		createDataFile("yelp","csv");
		Gson gson = new Gson();
		try(BufferedReader br = new BufferedReader(new FileReader(inDataPath))) {
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
