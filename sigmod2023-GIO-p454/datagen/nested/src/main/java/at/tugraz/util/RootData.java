package at.tugraz.util;

import com.google.gson.Gson;

import org.apache.commons.lang3.tuple.ImmutablePair;
import org.apache.commons.lang3.tuple.Pair;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

public abstract class RootData {

	protected Pair<ArrayList<Types.ValueType>, ArrayList<Object>> addPairSchemaValue(
		Pair<ArrayList<Types.ValueType>, ArrayList<Object>> pair, Types.ValueType vt, Object o) {
		if(pair == null)
			pair = new ImmutablePair<>(new ArrayList<Types.ValueType>(), new ArrayList<Object>());
		pair.getKey().add(vt);
		pair.getValue().add(o);
		return pair;
	}

	protected Pair<ArrayList<Types.ValueType>, ArrayList<Object>> addPairSchemaValue(
		Pair<ArrayList<Types.ValueType>, ArrayList<Object>> des,
		Pair<ArrayList<Types.ValueType>, ArrayList<Object>> src) {

		if(des == null)
			des = new ImmutablePair<>(new ArrayList<Types.ValueType>(), new ArrayList<Object>());
		if(src == null) {
			throw new RuntimeException("Src can't be null!");
		}

		des.getKey().addAll(src.getKey());
		des.getValue().addAll(src.getValue());
		return des;
	}

	protected Pair<ArrayList<Types.ValueType>, ArrayList<Object>> addPairSchemaValue(
		Pair<ArrayList<Types.ValueType>, ArrayList<Object>> des, ArrayList<?> src, Types.ValueType vt, int maxSize) {
		if(des == null)
			des = new ImmutablePair<>(new ArrayList<Types.ValueType>(), new ArrayList<Object>());

		int sizeOfSrc = src != null ? src.size() : 0;

		ArrayList<Types.ValueType> vts = new ArrayList<>();
		for(int i = 0; i < sizeOfSrc; i++)
			vts.add(vt);

		des.getKey().addAll(vts);
		if(src != null)
			des.getValue().addAll(src);
		if(maxSize > 0 && maxSize > sizeOfSrc) {
			for(int i = sizeOfSrc; i < maxSize; i++) {
				des.getKey().add(vt);
				switch(vt) {
					case INT32:
					case INT64:
					case FP32:
					case FP64:
						des.getValue().add(0);
						break;
					case STRING:
						des.getValue().add(null);
						break;
					case BOOLEAN:
						des.getValue().add(false);
						break;
				}
			}
		}
		return des;
	}
	protected Pair<ArrayList<Types.ValueType>, ArrayList<Object>> addPairSchemaValue(
		Pair<ArrayList<Types.ValueType>, ArrayList<Object>> des, ArrayList<?> src, Types.ValueType vt) {
		return addPairSchemaValue(des, src, vt, 0);
	}

	protected Integer addSchemaValue(HashMap<Integer, Pair<Types.ValueType, Object>> hashMap, Integer index, Types.ValueType valueType, Object value){
		if(value != null) {
			Pair<Types.ValueType, Object> pair = new ImmutablePair<>(valueType, value);
			hashMap.put(index, pair);
		}
		return ++index;
	}

	public String getJSON() {
		Gson gson = new Gson();//new GsonBuilder().disableHtmlEscaping().create();//new Gson();
		return gson.toJson(this);
	}

//	public String getXMLTPCH() throws JAXBException {
//		JAXBContext jc = (JAXBContext) JAXBContext.newInstance(LineItem.class);
//		Marshaller marshaller = jc.createMarshaller();
//		marshaller.setProperty(Marshaller.JAXB_FRAGMENT, true);
//	//	marshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);
//		JAXBElement<LineItem> rootElement = new JAXBElement<LineItem>(new QName(null,"l_lineitem"), LineItem.class,
//			(LineItem) this);
//
//		StringWriter sw = new StringWriter();
//
//		//Write XML to StringWriter
//		marshaller.marshal(rootElement, sw);
//
//		//Verify XML Content
//		String xmlContent = sw.toString();
//
//		return xmlContent;
//	}


	protected String getRandomString(int length) {
		String alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz123456789";
		StringBuilder salt = new StringBuilder();
		Random rnd = new Random();
		while(salt.length() < length) { // length of the random string.
			int index = (int) (rnd.nextFloat() * alphabet.length());
			salt.append(alphabet.charAt(index));
		}
		String saltStr = salt.toString();
		return saltStr;

	}
	public int getRandomNumber() {
		Random r = new Random();
		int low = 0;
		int high = 100000000;
		int result = r.nextInt(high - low) + low;
		return result;
	}


}
