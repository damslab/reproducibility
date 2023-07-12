package at.tugraz.util;

public class Types {

	/**
	 * Value types (int, double, string, boolean, unknown).
	 */
	public enum ValueType {
		UINT8, // Used for parsing in UINT values from numpy.
		FP32, FP64, INT32, INT64, BOOLEAN, STRING, UNKNOWN;

		public boolean isNumeric() {
			return this == UINT8 || this == INT32 || this == INT64 || this == FP32 || this == FP64;
		}

		public boolean isUnknown() {
			return this == UNKNOWN;
		}

		public boolean isPseudoNumeric() {
			return isNumeric() || this == BOOLEAN;
		}

		public String toExternalString() {
			switch(this) {
				case FP32:
				case FP64:
					return "DOUBLE";
				case UINT8:
				case INT32:
				case INT64:
					return "INT";
				case BOOLEAN:
					return "BOOLEAN";
				default:
					return toString();
			}
		}
	}
}
