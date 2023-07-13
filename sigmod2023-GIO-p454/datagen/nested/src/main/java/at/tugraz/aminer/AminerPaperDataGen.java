package at.tugraz.aminer;

import at.tugraz.util.GenerateData;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

public class AminerPaperDataGen extends GenerateData {
	private String authorPath;
	private String paperPath;
	private int maxAffiliationsSize;
	private int maxPaperReferencesSize;
	private int maxPaperAuthorsSize;
	private int maxResearchInterestsSize;

	HashMap<Long, Author> authorMap = new HashMap<Long, Author>();
	HashMap<String, Long> authorNameMap = new HashMap<String, Long>();
	HashMap<Long, Paper> papers = new HashMap<Long, Paper>();

	public AminerPaperDataGen(String paper, String author) {
		this.paperPath = paper;
		this.authorPath = author;
		loadAuthorData();
		loadPaperData();
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

	// Load Paper Data
	private void loadPaperData() {
		String index = "#index ";
		String title = "#* ";
		String author = "#@ ";
		String affiliation = "#o ";
		String year = "#t ";
		String venue = "#c ";
		String reference = "#% ";
		String pAbstract = "#! ";
		try(BufferedReader br = new BufferedReader(new FileReader(paperPath))) {
			String line;
			Paper paper = null;
			String strValue;
			int count = 0;
			while((line = br.readLine()) != null) {
				if(line.startsWith(index)) {
					if(paper != null)
						papers.put(paper.getIndex(), paper);
					paper = new Paper();
					strValue = line.substring(index.length());
					paper.setIndex(Long.parseLong(strValue));
				}
				else if(line.startsWith(title)) {
					strValue = line.substring(title.length());
					paper.setTitle(strValue);
				}
				else if(line.startsWith(author)) {
					strValue = line.substring(author.length());
					String[] strValues = strValue.split(";");

					ArrayList<Author> al = new ArrayList<>();
					for(String s : strValues) {
						Long aid = authorNameMap.get(s);
						Author au = authorMap.get(aid);
						if(au != null)
							al.add(au);
					}
					maxPaperAuthorsSize = Math.max(maxPaperAuthorsSize, al.size());
					paper.setAuthors(al);
					//maxPaperAuthorsSize = Math.max(maxPaperAuthorsSize, strValues.length);
				}
				//				else if(line.startsWith(affiliation)) {
				//					strValue = line.substring(affiliation.length());
				//					String[] strValues = strValue.split(";");
				//					maxPaperAffiliationsSize = Math.max(maxPaperAffiliationsSize, strValues.length);
				//					ArrayList<String> ta = new ArrayList<>();
				//					Collections.addAll(ta, strValues);
				//					paper.setPaperAffiliations(ta);
				//				}
				else if(line.startsWith(year)) {
					strValue = line.substring(year.length());
					try {
						paper.setYear(Integer.parseInt(strValue));
					}
					catch(Exception e) {
					}

				}
				else if(line.startsWith(venue)) {
					strValue = line.substring(venue.length());
					paper.setPublicationVenue(strValue);
				}
				else if(line.startsWith(reference)) {
					strValue = line.substring(reference.length());
					ArrayList<Long> refs = paper.getReferences();
					if(refs == null)
						refs = new ArrayList<>();
					refs.add(Long.parseLong(strValue));
					paper.setReferences(refs);
					maxPaperReferencesSize = Math.max(maxPaperReferencesSize, refs.size());
				}
				else if(line.startsWith(pAbstract)) {
					strValue = line.substring(pAbstract.length());
					paper.setPaperAbstract(strValue);
				}
				count++;

			}

		}
		catch(Exception e) {
			throw new RuntimeException(e);
		}
	}

	public HashMap<Long, Paper> getPapers() {
		return papers;
	}

	public int getMaxAffiliationsSize() {
		return maxAffiliationsSize;
	}

	public int getMaxPaperReferencesSize() {
		return maxPaperReferencesSize;
	}

	public int getMaxPaperAuthorsSize() {
		return maxPaperAuthorsSize;
	}

	public static void main(String[] args) throws IOException {
		String in_paper = args[0];
		String in_author = args[1];
		outDataPath = args[2];
		AminerPaperDataGen aminer = new AminerPaperDataGen(in_paper, in_author);

		HashMap<Long, Paper> papers = aminer.getPapers();

		createDataFile("aminer-paper", "json");
		for(Long pk : papers.keySet()) {
			Paper paper = papers.get(pk);
			String jsonStr = paper.getJSON();
			dataFileHandler.write(jsonStr);
			dataFileHandler.write("\n");
		}
		flushFileHandlers();
	}

}
