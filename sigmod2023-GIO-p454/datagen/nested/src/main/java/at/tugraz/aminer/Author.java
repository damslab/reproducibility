package at.tugraz.aminer;

import at.tugraz.util.RootData;

import java.util.ArrayList;

//	#index ---- index id of this author
//	#n     ---- name  (separated by semicolons)
//	#a     ---- affiliations  (separated by semicolons)
//	#pc    ---- the count of published papers of this author
//	#cn    ---- the total number of citations of this author
//	#hi    ---- the H-index of this author
//	#pi    ---- the P-index with equal A-index of this author
//	#upi   ---- the P-index with unequal A-index of this author
//	#t     ---- research interests of this author  (separated by semicolons)

public class Author extends RootData {
	private Long index;
	private String name;
	private ArrayList<String> authorAffiliations;
	private Integer paperCount;
	private Integer citationNumber;
	private Float hIndex;
	private Float pIndex;
	private Float upIndex;
	private ArrayList<String> researchInterests;

	public void setIndex(Long index) {
		this.index = index;
	}

	public void setName(String name) {
		this.name = name;
	}

	public void setAuthorAffiliations(ArrayList<String> authorAffiliations) {
		this.authorAffiliations = authorAffiliations;
	}

	public void setPaperCount(Integer paperCount) {
		this.paperCount = paperCount;
	}

	public void setCitationNumber(Integer citationNumber) {
		this.citationNumber = citationNumber;
	}

	public void sethIndex(Float hIndex) {
		this.hIndex = hIndex;
	}

	public void setpIndex(Float pIndex) {
		this.pIndex = pIndex;
	}

	public void setUpIndex(Float upIndex) {
		this.upIndex = upIndex;
	}

	public void setResearchInterests(ArrayList<String> researchInterests) {
		this.researchInterests = researchInterests;
	}

	public Long getIndex() {
		return index;
	}

	public String getName() {
		return name;
	}

	public ArrayList<String> getAuthorAffiliations() {
		return authorAffiliations;
	}

	public Integer getPaperCount() {
		return paperCount;
	}

	public Integer getCitationNumber() {
		return citationNumber;
	}

	public Float gethIndex() {
		return hIndex;
	}

	public Float getpIndex() {
		return pIndex;
	}

	public Float getUpIndex() {
		return upIndex;
	}

	public ArrayList<String> getResearchInterests() {
		return researchInterests;
	}
}
