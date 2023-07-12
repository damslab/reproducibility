package at.tugraz.util;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class FileHandler {

	private BufferedWriter writer;

	public FileHandler(String fileName) throws IOException {
		writer = new BufferedWriter(new FileWriter(fileName));
	}

	public void write(String data) throws IOException {
		writer.write(data);
	}

	public void flush() throws IOException {
		this.writer.flush();
		this.writer.close();
	}
}
