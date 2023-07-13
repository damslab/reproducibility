package at.tugraz.util;

import java.io.File;
import java.io.IOException;

public abstract class GenerateData {

	protected static String inDataPath;
	protected static String outDataPath;
	protected static String dataFileName;
	protected static FileHandler dataFileHandler;
	protected static String format;

	protected static String objectToString(Object in, Types.ValueType vt) {
		return (in != null) ? in.toString() : "NULL";
	}

	protected static void mainGenerateData(String[] args, String dataset) throws IOException {
		inDataPath = args[0];
		outDataPath = args[1];
	}


	protected static void createDataFile(String dataset, String format) throws IOException {
		createDataPath(dataset, format);
		dataFileName = outDataPath +"/"+ dataset + "-"+format+".dat";
		dataFileHandler = new FileHandler(dataFileName);
	}

	protected static void createDataPath(String dataset, String format) throws IOException {
		File directory;
		if(format !=null)
			directory = new File(outDataPath+"/");
		else
			directory = new File(outDataPath+"/"+ dataset +"/");
		if(!directory.exists()) {
			directory.mkdir();
		}
	}
	protected static void flushFileHandlers() throws IOException {
		dataFileHandler.flush();
	}
}
