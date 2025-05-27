import dk.aau.modelardb.core.DataPoint;
import dk.aau.modelardb.core.SegmentGenerator;
import dk.aau.modelardb.core.SegmentGroup;
import dk.aau.modelardb.core.TimeSeriesGroup;
import dk.aau.modelardb.core.models.ModelType;
import dk.aau.modelardb.core.models.ModelTypeFactory;
import dk.aau.modelardb.core.timeseries.TimeSeries;
import dk.aau.modelardb.core.timeseries.TimeSeriesParquet;
import dk.aau.modelardb.core.utility.SegmentFunction;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.parquet.ParquetReadOptions;
import org.apache.parquet.example.data.Group;
import org.apache.parquet.example.data.simple.SimpleGroup;
import org.apache.parquet.example.data.simple.convert.GroupRecordConverter;
import org.apache.parquet.hadoop.ParquetFileReader;
import org.apache.parquet.hadoop.ParquetWriter;
import org.apache.parquet.hadoop.api.WriteSupport;
import org.apache.parquet.hadoop.example.GroupWriteSupport;
import org.apache.parquet.hadoop.metadata.CompressionCodecName;
import org.apache.parquet.hadoop.util.HadoopInputFile;
import org.apache.parquet.io.ColumnIOFactory;
import org.apache.parquet.io.api.Binary;
import org.apache.parquet.schema.MessageType;
import org.apache.parquet.schema.PrimitiveType;
import org.apache.parquet.schema.Type;

import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Constructor;
import java.nio.ByteBuffer;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.sql.Timestamp;
import java.util.*;
import java.util.function.BooleanSupplier;
import java.util.function.Supplier;

class ModelarDBRunner {
  /** Instance Variables **/
  private static final int lengthBound = 10000; //Length bound is only used by the lossless models
  private static long totalModelTypeDataPointCounter = 0;
  private static long losslessModelTypeDataPointCounter = 0;



  /** Public Methods **/
  public static void run_compression(String[] args) throws Exception{
    var parquetFilePath = args[0];
    double[] errorBounds = extractErrorBounds(args);
    String[] selectedModels = extractSelectedModels(args);
    TimeZone.setDefault(TimeZone.getTimeZone("UTC"));

    //Determine number of columns and sampling interval
    var parquetFileReader = newParquetFileReader(parquetFilePath);
    var inputSchema = parquetFileReader.getFooter().getFileMetaData().getSchema().getColumns();
    var valueColumnCount = inputSchema.size();
    var samplingInterval = (int) determineSamplingInterval(parquetFileReader);
    parquetFileReader.close();

    //Setup handlers for calling private methods
    var consumeAllDataPoints = SegmentGenerator.class.getDeclaredMethod("consumeAllDataPoints");
    consumeAllDataPoints.setAccessible(true);
    var close = SegmentGenerator.class.getDeclaredMethod("close");
    close.setAccessible(true);

    //Ingest Parquet files using models and error bounds specified as command line arguments
    var tidGid = 0; //HACK: gid == tid when grouping is disabled
    var timestampColumnIndex = 0;
    var compressedSegments = new HashMap<Integer, ArrayList<ArrayList<SegmentGroup>>>();
    for (var valueColumnIndex = 1; valueColumnIndex < valueColumnCount; valueColumnIndex++) {

      var compressedSegmentsForColumn = new ArrayList<ArrayList<SegmentGroup>>();
      compressedSegments.put(valueColumnIndex, compressedSegmentsForColumn);
      for (double errorBound : errorBounds) {
        tidGid += 1;
        var compressedSegmentsForColumnAndErrorBound = new ArrayList<SegmentGroup>();
        var ts = new TimeSeriesParquet(parquetFilePath, tidGid, samplingInterval, timestampColumnIndex, valueColumnIndex);
        var tsg = new TimeSeriesGroup(tidGid, new TimeSeries[]{ts});
        tsg.initialize(); //Lazy initialization is required when running distributed
        tsg.hasNext();
        var sg = newSegmentGenerator(tsg, samplingInterval, errorBound, selectedModels, compressedSegmentsForColumnAndErrorBound);
        consumeAllDataPoints.invoke(sg);
        close.invoke(sg);
        //Print start and end time of ingested time series for debugging
        System.out.println("INFO: processed column " + (valueColumnIndex + 1)
                + "(" + new Timestamp(compressedSegmentsForColumnAndErrorBound.get(0).startTime) + " to "
                + new Timestamp(compressedSegmentsForColumnAndErrorBound.get(compressedSegmentsForColumnAndErrorBound.size() - 1).endTime) + ")"
                + " of " + valueColumnCount + " using error bound " + errorBound);
        if (ModelarDBRunner.losslessModelTypeDataPointCounter != 0) {
          float percentage = (float) (((double) ModelarDBRunner.losslessModelTypeDataPointCounter / ModelarDBRunner.totalModelTypeDataPointCounter) * 100.0);
          System.out.println("WARNING: lossless fallback model was used for " + percentage + "% (" +
                  ModelarDBRunner.losslessModelTypeDataPointCounter + "/" + ModelarDBRunner.totalModelTypeDataPointCounter+ ") of the data points");
        }
        compressedSegmentsForColumn.add(compressedSegmentsForColumnAndErrorBound);
      }

    }

    //Write the real data points (R), approximated data points, (E error bound), and models to Parquet files

    String subfolder = (selectedModels[0].contains("PMC"))? "pmc" :((selectedModels[0].contains("Gorilla"))? "gorilla" : "swing");
    StringBuilder outdir = new StringBuilder("data/compressed/");
    outdir.append(subfolder).append('/');
    outdir.append("error_bound_").append(errorBounds[0]).append('/');
    String data_name = parquetFilePath.split("/")[2];
    data_name = data_name.split("\\.")[0];    
    var parquetFilePathWithoutSuffix = outdir.append("partial_"+data_name);

    var parquetFilePathSegments = parquetFilePathWithoutSuffix + "_segments_" + subfolder+ ".parquet";
    var segmentsSchema = new MessageType("segments",
            new PrimitiveType(Type.Repetition.REQUIRED, PrimitiveType.PrimitiveTypeName.INT32, "gid" ),
            new PrimitiveType(Type.Repetition.REQUIRED, PrimitiveType.PrimitiveTypeName.INT64, "start_time"),
            new PrimitiveType(Type.Repetition.REQUIRED, PrimitiveType.PrimitiveTypeName.INT64, "end_time"),
            new PrimitiveType(Type.Repetition.REQUIRED, PrimitiveType.PrimitiveTypeName.INT32, "mtid" ),
            new PrimitiveType(Type.Repetition.REQUIRED, PrimitiveType.PrimitiveTypeName.BINARY, "model"),
            new PrimitiveType(Type.Repetition.REQUIRED, PrimitiveType.PrimitiveTypeName.BINARY, "gaps"));
    var parquetSegmentWriter = newParquetFileWriter(parquetFilePathSegments, segmentsSchema);

    var metdataSegmentWriter = new FileWriter(parquetFilePathWithoutSuffix + "_metadata_" + subfolder + ".txt");
    metdataSegmentWriter.write(samplingInterval + "\n");
    metdataSegmentWriter.write("\n"); //Add empty line to simplify parsing

    var allModelTypes = getAllModelTypes(selectedModels);
    for (var modelType : allModelTypes) {
      metdataSegmentWriter.write(modelType.mtid + " " + modelType.getClass().getName() + "\n");
    }
    metdataSegmentWriter.write("\n"); //Add empty line to simplify parsing

    var columns = new ArrayList<Type>();
    columns.add(new PrimitiveType(Type.Repetition.REQUIRED, PrimitiveType.PrimitiveTypeName.INT64, "datetime"));
    var columnValues = new ArrayList<Iterator<DataPoint>>();
    var offset = ByteBuffer.allocate(12).putInt(1).putInt(1).putInt(0).array(); //HACK: gid == tid when grouping is disabled
    for (var valueColumnIndex = 1; valueColumnIndex < valueColumnCount; valueColumnIndex++) {
      var compressedSegmentsForColumn = compressedSegments.get(valueColumnIndex);
      if ( ! compressedSegmentsForColumn.isEmpty()) { //Check if the column was skipped
        var columnName = inputSchema.get(valueColumnIndex).getPath()[0];
        columnName = columnName.replace(" ", "_");

        //Add the raw data points cast to float to match the precession of reconstructed data
        columns.add(new PrimitiveType(Type.Repetition.REQUIRED, PrimitiveType.PrimitiveTypeName.FLOAT, columnName + "-R"));
        var rts = new TimeSeriesParquet(parquetFilePath, -1, samplingInterval, timestampColumnIndex, valueColumnIndex); //Tid -1 should never appear
        rts.open(); //Lazy initialization is required when running distributed
        columnValues.add(rts);

        //Add each of the approximated columns where data points are reconstructed from models
        for (int i = 0; i < errorBounds.length; i++) {
          double errorBound = errorBounds[i];
          var columnNameWithErrorBound = columnName + "-E" + errorBound;
          columns.add(new PrimitiveType(Type.Repetition.REQUIRED, PrimitiveType.PrimitiveTypeName.FLOAT, columnNameWithErrorBound));
          var compressedSegmentsForColumnAndErrorBound = compressedSegmentsForColumn.get(i);
          columnValues.add(compressedSegmentsForColumnAndErrorBound.stream().map(sg ->
                  allModelTypes[sg.mtid - 1].get(sg.gid, sg.startTime, sg.endTime, samplingInterval, sg.model, offset)).flatMap(s -> s.grid()).iterator());

          //Dump all segments for this column and error bound as a reference to these are available
          metdataSegmentWriter.write(compressedSegmentsForColumnAndErrorBound.get(0).gid + " " + columnNameWithErrorBound + "\n");
          compressedSegmentsForColumnAndErrorBound.forEach(segmentGroup -> {
            var group = new SimpleGroup(segmentsSchema);
            group.add(0, segmentGroup.gid);
            group.add(1, segmentGroup.startTime);
            group.add(2, segmentGroup.endTime);
            group.add(3, segmentGroup.mtid);
            group.add(4, Binary.fromConstantByteArray(segmentGroup.model));
            group.add(5, Binary.fromConstantByteArray(segmentGroup.offsets));
            try {
              parquetSegmentWriter.write(group);
            } catch (IOException ioe) {
              error("Failed to write segments to Parquet ", ioe);
            }
          });
        }
      }
    }
    parquetSegmentWriter.close();
    metdataSegmentWriter.close();

    //Dump all data points
    var parquetFilePathDataPoints = parquetFilePathWithoutSuffix + "_points_" + subfolder + ".parquet";
    var dataPointsSchema = new MessageType("data_points", columns);
    var columnValuesSize = columnValues.size();
    var parquetDataPointWriter = newParquetFileWriter(parquetFilePathDataPoints, dataPointsSchema);
    var firstIterator = columnValues.get(0);
    while (columnValues.stream().allMatch(it -> it.hasNext())) { //All columns should contain the same number of values
      var group = new SimpleGroup(dataPointsSchema);
      var dp = firstIterator.next();
      group.add(0, dp.timestamp);
      group.add(1, dp.value);
      for (var index = 1; index < columnValuesSize; index++) {
        group.add(index + 1, columnValues.get(index).next().value);
      }
      parquetDataPointWriter.write(group);
    }
    parquetDataPointWriter.close();

  }




  public static void main(String[] args) throws Exception {
    //Parse user-configuration
    if (args.length < 3) {
      System.out.println("usage: java -cp ModelarDB.jar ModelarDBRunner.java parquetFilePath errorBoundsInPercentages modelsToUse(C L G P A)");
      return;
    }
    ModelarDBRunner.run_compression(args);
  }

  /** Private Methods **/
  private static double[] extractErrorBounds(String[] args) {
    var errorBounds = new HashSet<Double>();
    for (int i = 1; i < args.length; i++) {
      try {
        errorBounds.add(Double.parseDouble(args[i]));
      } catch (NumberFormatException e) {
        //Ignore models used
      }
    }
    if (errorBounds.isEmpty()) {
      error("No error bounds were provided as command line arguments ", null);
    }
    return errorBounds.stream().mapToDouble(i -> i).toArray();
  }

  private static String[] extractSelectedModels(String[] args) {
    var selectedModels = new HashSet<String>();
    for (int i = 1; i < args.length; i++) {
      switch (args[i].toUpperCase()) {
        case "C" -> selectedModels.add("dk.aau.modelardb.core.models.PMC_MeanModelType");
        case "L" -> selectedModels.add("dk.aau.modelardb.core.models.SwingFilterModelType");
        case "G" -> selectedModels.add("dk.aau.modelardb.core.models.FacebookGorillaModelType");
        case "P" -> {
          selectedModels.add("dk.aau.modelardb.core.models.PMC_MeanModelType");
          selectedModels.add("dk.aau.modelardb.core.models.SwingFilterModelType");
        }
        case "A" -> {
          selectedModels.add("dk.aau.modelardb.core.models.PMC_MeanModelType");
          selectedModels.add("dk.aau.modelardb.core.models.SwingFilterModelType");
          selectedModels.add("dk.aau.modelardb.core.models.FacebookGorillaModelType");
        }
        default -> {
          try {
            Double.parseDouble(args[i]); //Ignore error bounds
          } catch (NumberFormatException e) {
            error("Unknown model type specified as a command line argument " + args[i], null);
          }
        }
      }
    }
    if (selectedModels.isEmpty()) {
      error("No model types were provided as command line arguments ", null);
    }
    return selectedModels.toArray(new String[selectedModels.size()]);
  }

  private static void error(String msg, Throwable reason) {
    if (reason == null) {
      System.out.println("\nERROR: " + msg);
    } else {
      System.out.println("\nERROR: " + msg + " " + reason);
    }
    System.exit(1);
  }

  private static ParquetFileReader newParquetFileReader(String parquetFilePath) throws IOException {
    var path = new Path(parquetFilePath);
    var iff = HadoopInputFile.fromPath(path, new Configuration());
    var pro = ParquetReadOptions.builder().build();
    return new ParquetFileReader(iff, pro);
  }

  private static long determineSamplingInterval(ParquetFileReader parquetFileReader) throws IOException {
    //Initialize record reader
    var readStore = parquetFileReader.readNextRowGroup();
    var schema = new MessageType("schema", parquetFileReader.getFooter().getFileMetaData().getSchema().getFields().get(0));
    var grc = new GroupRecordConverter(schema);
    var columnIO = new ColumnIOFactory().getColumnIO(schema);
    var recordReader = columnIO.getRecordReader(readStore, grc);
    var rowIndex = 1;
    var rowCount = readStore.getRowCount();

    //Check if timestamps are formatted as expected
    var previousTimestamp = recordReader.read().getLong(0, 0) / 1000;
    var year = new Timestamp(previousTimestamp).getYear() + 1900;
    if (year < 1980 || 2100 < year) {
      error("Timestamps seems to be malformed " + new Timestamp(previousTimestamp) , null);
    }

    //Read all rows and ensure time series is ordered
    var samplingIntervalCounter = new HashMap<Long, Integer>();
    while (rowIndex != rowCount) {
      var currentTimestamp = recordReader.read().getLong(0, 0) / 1000;
      var samplingInterval = currentTimestamp - previousTimestamp;
      samplingIntervalCounter.merge(samplingInterval, 1, Integer::sum);

      //Check if time series is ordered
      if (currentTimestamp < previousTimestamp) {
        error("The timestamps are not ordered as " + new Timestamp(currentTimestamp) + " < " + new Timestamp(previousTimestamp), null);
      }
      previousTimestamp = currentTimestamp;
      rowIndex++;
    }

    //Select SI based on majority
    return Collections.max(samplingIntervalCounter.entrySet(), Comparator.comparingInt(Map.Entry::getValue)).getKey();
  }

  private static SegmentGenerator newSegmentGenerator(TimeSeriesGroup tsg, int samplingInterval, double errorBound,
                                                      String[] selectedModels, ArrayList<SegmentGroup> compressedSegmentsForColumnAndErrorBound) {
    //Construct the model types
    var fallbackModelType = ModelTypeFactory.getFallbackModelType((float) errorBound, ModelarDBRunner.lengthBound);
    Supplier<ModelType[]> modelTypeInitializer = newModelTypeSupplier(selectedModels, errorBound);

    //Construct segment consume methods
    var consumeTemporary = new SegmentFunction() {
      public void emit(int gid, long startTime, long endTime, int mtid, byte[] model, byte[] gaps) {
        //Purposely empty
      }
    };

    ModelarDBRunner.totalModelTypeDataPointCounter = 0;
    ModelarDBRunner.losslessModelTypeDataPointCounter = 0;
    var consumeFinalized = new SegmentFunction() {
      public void emit(int gid, long startTime, long endTime, int mtid, byte[] model, byte[] gaps) {
        ModelarDBRunner.totalModelTypeDataPointCounter += ((endTime - startTime) / samplingInterval) + 1;
        if (mtid == 1) {
          ModelarDBRunner.losslessModelTypeDataPointCounter += ((endTime - startTime) / samplingInterval) + 1;
        }
        compressedSegmentsForColumnAndErrorBound.add(new SegmentGroup(gid, startTime, endTime, mtid, model, gaps));
      }
    };

    var isTerminated = new BooleanSupplier() {
      public boolean getAsBoolean() {
        return false;
      }
    };

    //Construct segment generator
    try {
      var constructor = (Constructor<SegmentGenerator>) SegmentGenerator.class.getDeclaredConstructors()[0];
      constructor.setAccessible(true);
      return constructor.newInstance(tsg, modelTypeInitializer, fallbackModelType, null, 0, 0.0F, consumeTemporary, consumeFinalized);
    } catch (Exception e) {
      Throwable reason = e;
      while (reason.getCause() != null) {
        reason = reason.getCause();
      }
      error("Unable to construct SegmentGenerator due to ", reason);
    }
    return null; //Required by javac
  }

  private static Supplier<ModelType[]> newModelTypeSupplier(String[] selectedModels, double errorBound) {
    var mtids = new int[] {2, 3, 4}; //The lossless fallback model type has mtid one per definition
    return () -> ModelTypeFactory.getModelTypes(selectedModels, mtids, (float) errorBound, ModelarDBRunner.lengthBound);
  }

  private static ModelType[] getAllModelTypes(String[] selectedModels) {
    int errorBound = 0; //Only used for decompression
    var userModelTypes = newModelTypeSupplier(selectedModels, errorBound).get();
    var modelTypes = new ModelType[userModelTypes.length + 1];
    modelTypes[0] = ModelTypeFactory.getFallbackModelType(errorBound, ModelarDBRunner.lengthBound);
    for (var index = 1; index < modelTypes.length; index++) {
      modelTypes[index] = userModelTypes[index - 1];
    }
    return modelTypes;
  }

  private static ParquetWriter<Group> newParquetFileWriter(String parquetFilePath, MessageType schema) throws IOException {
    var path = new Path(parquetFilePath);

    FileSystem fileSystem = path.getFileSystem(new Configuration());
    fileSystem.setWriteChecksum(false);
    if (fileSystem.exists(path)){
      if (fileSystem.delete(path, false)) {
        System.out.println("File deleted successfully!");
      } else {
        System.out.println("Delete operation failed.");
      }
    }

    var parquetWriterBuilder = new ParquetWriter.Builder(path) {
      @Override
      protected ParquetWriter.Builder self() {
        return this;
      }

      @Override
      protected WriteSupport getWriteSupport(Configuration conf) {
        GroupWriteSupport.setSchema(schema, conf);
        return new GroupWriteSupport();
      }
    };
    parquetWriterBuilder.withCompressionCodec(CompressionCodecName.SNAPPY);
    return parquetWriterBuilder.build();
  }
}