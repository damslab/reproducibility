package at.tugraz.util;

import org.apache.log4j.PropertyConfigurator;

import java.io.File;
import java.io.IOException;
import java.util.BitSet;
import java.util.Properties;

public abstract class GenerateData {

	protected static long datasetNRows;
	protected static long[] sampleNRows;
	protected static String inDataPath;
	protected static String outDataPath;

	protected static String dataFileName;
	protected static String sampleRawFileName;
	protected static String sampleFrameFileName;
	protected static String schemaFileName;
	protected static String schemaMapFileName;

	protected static FileHandler dataFileHandler;
	protected static FileHandler dataFileHandlerCSV;
	protected static FileHandler sampleRawFileHandler;
	protected static FileHandler sampleFrameFileHandler;
	protected static FileHandler schemaFileHandler;
	protected static FileHandler schemaMapFileHandler;

	protected static BitSet bs;
	protected static int totalColCount;
	protected static String datasetName;
	protected static String format;

	protected static String objectToString(Object in, Types.ValueType vt) {
		return (in != null) ? in.toString() : "NULL";
	}

	protected static void mainGenerateData(String[] args, String dataset) throws IOException {
		Properties prop = new Properties();
		PropertyConfigurator.configure(prop);
		prop.setProperty("log4j.appender.WORKLOG.File", "log4j.properties");
		PropertyConfigurator.configure("log4j.properties");

		inDataPath = args[0];
		outDataPath = args[1];
		String[] tmpList = args[2].split(",");

		sampleNRows = new long[tmpList.length];
		for(int i = 0; i < tmpList.length; i++)
			sampleNRows[i] = Integer.parseInt(tmpList[i]);

	}


	protected static void createDataFile(String dataset, String format) throws IOException {
		createDataPath(dataset, format);
		dataFileName = outDataPath +"/"+ dataset+"-"+format+"/" + dataset + "-"+format+".dat";
		dataFileHandler = new FileHandler(dataFileName);
	}

	protected static void createDataPath(String dataset, String format) throws IOException {
		File directory;
		if(format !=null)
			directory = new File(outDataPath+"/"+ dataset + "-"+format+"/");
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
