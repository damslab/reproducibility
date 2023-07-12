package at.tugraz.aminer;

import at.tugraz.util.RootData;
import java.util.ArrayList;

//	#index ---- index id of this paper
//	#*     ---- paper title
//	#@     ---- authors (separated by semicolons)
//	#o     ---- affiliations (separated by semicolons, and each affiliaiton corresponds to an author in order)
//	#t     ---- year
//	#c     ---- publication venue
//	#%     ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
//	#!     ---- abstract

public class Paper extends RootData {

	private Long index;
	private String title;
	private ArrayList<Author> authors;
	private Integer year;
	private String publicationVenue;
	private ArrayList<Long> references;
	private String paperAbstract;

	public Long getIndex() {
		return index;
	}

	public void setIndex(Long index) {
		this.index = index;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public void setAuthors(ArrayList<Author> authors) {
		this.authors = authors;
	}

	public void setYear(Integer year) {
		this.year = year;
	}

	public void setPublicationVenue(String publicationVenue) {
		this.publicationVenue = publicationVenue;
	}

	public void setReferences(ArrayList<Long> references) {
		this.references = references;
	}

	public void setPaperAbstract(String paperAbstract) {
		this.paperAbstract = paperAbstract;
	}

	public ArrayList<Long> getReferences() {
		return references;
	}

	public String getTitle() {
		return title;
	}

	public ArrayList<Author> getAuthors() {
		return authors;
	}

	public Integer getYear() {
		return year;
	}

	public String getPublicationVenue() {
		return publicationVenue;
	}

	public String getPaperAbstract() {
		return paperAbstract;
	}
}
