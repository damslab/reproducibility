package at.tugraz.aminer;

import at.tugraz.util.GenerateData;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

public class AminerAuthorDataGen extends GenerateData {

	private String authorPath;
	private int maxAffiliationsSize;
	private int maxResearchInterestsSize;

	HashMap<Long, Author> authorMap = new HashMap<Long, Author>();
	HashMap<String, Long> authorNameMap = new HashMap<String, Long>();

	public AminerAuthorDataGen(String path) {
		this.authorPath = path;
		maxAffiliationsSize = 0;
		maxResearchInterestsSize = 0;
		loadAuthorData();
	}

	// Load Author Data
	private void loadAuthorData() {
		String index = "#index ";
		String n = "#n ";
		String a = "#a ";
		String pc = "#pc ";
		String cn = "#cn ";
		String hi = "#hi ";
		String pi = "#pi ";
		String upi = "#upi ";
		String t = "#t ";

		try(BufferedReader br = new BufferedReader(new FileReader(authorPath))) {
			String line;
			Author author = null;
			String strValue;

			while((line = br.readLine()) != null) {
				if(line.startsWith(index)) {
					if(author != null)
						authorMap.put(author.getIndex(), author);
					author = new Author();
					strValue = line.substring(index.length());
					author.setIndex(Long.parseLong(strValue));
				}
				else if(line.startsWith(n)) {
					strValue = line.substring(n.length());
					author.setName(strValue);
					authorNameMap.put(strValue, author.getIndex());
				}
				else if(line.startsWith(a)) {
					strValue = line.substring(a.length());
					String[] strValues = strValue.split(";");
					maxAffiliationsSize = Math.max(maxAffiliationsSize, strValues.length);
					ArrayList<String> ta = new ArrayList<>();
					Collections.addAll(ta, strValues);
					author.setAuthorAffiliations(ta);
				}
				else if(line.startsWith(pc)) {
					strValue = line.substring(pc.length());
					author.setPaperCount(Integer.parseInt(strValue));
				}
				else if(line.startsWith(cn)) {
					strValue = line.substring(cn.length());
					author.setCitationNumber(Integer.parseInt(strValue));
				}
				else if(line.startsWith(hi)) {
					strValue = line.substring(hi.length());
					author.sethIndex(Float.parseFloat(strValue));
				}
				else if(line.startsWith(pi)) {
					strValue = line.substring(pi.length());
					author.sethIndex(Float.parseFloat(strValue));
				}
				else if(line.startsWith(upi)) {
					strValue = line.substring(upi.length());
					author.sethIndex(Float.parseFloat(strValue));
				}
				else if(line.startsWith(t)) {
					strValue = line.substring(t.length());
					String[] strValues = strValue.split(";");
					maxResearchInterestsSize = Math.max(maxResearchInterestsSize, strValues.length);
					ArrayList<String> ta = new ArrayList<>();
					Collections.addAll(ta, strValues);
					author.setResearchInterests(ta);
				}
			}

		}
		catch(Exception e) {
			throw new RuntimeException(e);
		}
	}

	public HashMap<Long, Author> getAuthorMap() {
		return authorMap;
	}

	public static void main(String[] args) throws IOException {
		inDataPath = args[0];
		outDataPath = args[1];
		AminerAuthorDataGen aminer = new AminerAuthorDataGen(inDataPath);
		HashMap<Long, Author> authors = aminer.getAuthorMap();
		createDataFile("aminer-author", "json");
		for(Long ak : authors.keySet()) {
			Author author = authors.get(ak);
			String jsonStr = author.getJSON();
			dataFileHandler.write(jsonStr);
			dataFileHandler.write("\n");
		}
		flushFileHandlers();
	}
}
