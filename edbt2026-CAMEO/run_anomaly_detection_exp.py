from anomaly_detection import anomaly_detection_exp

if __name__ == "__main__":
    compressors = 'vw'
    data_path = "data/UCR_data"
    error_bound = 0.001
    anomaly_detection_exp.compress_and_detect_anomaly(compressors, data_path, error_bound)