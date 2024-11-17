
import raha
import pandas
import IPython.display
import sys

input = sys.argv[1]
name = sys.argv[2]
clean = sys.argv[3]
out = sys.argv[4]
if __name__ == '__main__':
    app_1 = raha.Detection()
    app_1.LABELING_BUDGET = 20
    app_1.STRATEGY_FILTERING = False

    dataset_dictionary = {
        "name": name,
        "path": input,
        "clean_path": clean
    }
    d = app_1.initialize_dataset(dataset_dictionary)
    d.dataframe.head()
    app_1.run_strategies(d)
    app_1.generate_features(d)
    app_1.build_clusters(d)

    while len(d.labeled_tuples) < app_1.LABELING_BUDGET:
        app_1.sample_tuple(d)
        app_1.label_with_ground_truth(d)
        d.labeled_tuples[d.sampled_tuple] = 1


    app_1.propagate_labels(d)
    app_1.predict_labels(d)
    app_1.store_results(d)
    app_2 = raha.Correction()
    app_2.LABELING_BUDGET = 20
    app_2.PRETRAINED_VALUE_BASED_MODELS_PATH = ""


    d = app_2.initialize_dataset(d)
    d.dataframe.head()

    app_2.initialize_models(d)
    for si in d.labeled_tuples:
        d.sampled_tuple = si
        print("si ",si)
        app_2.update_models(d)
        app_2.generate_features(d)
        app_2.predict_corrections(d)

    app_2.store_results(d)
    d.create_repaired_dataset(d.corrected_cells)
    d.repaired_dataframe.to_csv(out, sep=",", header=True, index=False, encoding="utf-8")
