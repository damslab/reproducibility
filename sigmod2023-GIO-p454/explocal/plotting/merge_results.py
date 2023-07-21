import pandas as pd
import numpy as np
import scipy.stats as stats
import re


class merge_results(object):

    def atoi(self, text):
        return int(text) if text.isdigit() else text

    def natural_keys(self, text):    
        return [ self.atoi(c) for c in re.split(r'(\d+)', text) ]    
    
    def calc_mean(self, list, ratio=1):    
        mean = np.mean(list)  
        std = np.std(list)
        normal_list = []
        nz=[]
        for l in list:
            if std == 0:
                break
            z = (l-mean)/std            
            if z <1 and z>=-1 :
                normal_list.append(l)
            nz.append(z)
        if len(normal_list) == 0:        
            avg_value = min(list)         
        else:        
            avg_value = np.mean(normal_list)
        return avg_value/ratio  
    
    def merge_results1(self, fieldName, ratio, header,datasets, parallels, projections, examples, path):
    
        data = pd.read_csv( path, sep=',')   
        df_final = pd.DataFrame(columns = header)    
        for dataset in datasets:
                for parallel in parallels:
                    for projection in projections:
                        for example in examples:
                            df_tmp =  data.loc[(data['dataset']==dataset) &
                                            (data[fieldName]==projection) &
                                            (data["example_nrows"]==example) &
                                            (data["parallel"]==parallel)
                                            ]                        
                            list_times = np.array(df_tmp['time'].tolist())                         
                            
                            if len(list_times) > 0 :
                                time = self.calc_mean(list=list_times, ratio=ratio)    
                                record= [dataset,projection,example,f'{time:.2f}',f'{parallel}'.lower()]
                                df_final.loc[len(df_final)] = record
    
        return df_final  

    def merge_results2(self, fieldName, ratio,header, baselines, datasets, parallels, projections,path):
        
        data = pd.read_csv( path, sep=',')   
        df_final = pd.DataFrame(columns = header)    
        for dataset in datasets:
            for baseline in baselines:
                for parallel in parallels:
                    for projection in projections:
                            df_tmp =  data.loc[(data['dataset']==dataset) &
                                            (data['baseline']==baseline) &
                                            (data[fieldName]==projection) &                                          
                                            (data["parallel"]==parallel)
                                            ]                        
                            list_times = np.array(df_tmp['time'].tolist())                         
                            
                            if len(list_times) > 0 :
                                time = self.calc_mean(list=list_times, ratio=ratio)    
                                record= [baseline,dataset,projection,f'{time:.2f}',f'{parallel}'.lower()]
                                df_final.loc[len(df_final)] = record
    
        return df_final 


    def merge_results5(self, header, baselines, datasets, parallels, path):
        
        data = pd.read_csv( path, sep=',')   
        df_final = pd.DataFrame(columns = header)    
        for dataset in datasets:
            for baseline in baselines:
                for parallel in parallels:
                            df_tmp =  data.loc[(data['dataset']==dataset) &
                                            (data['baseline']==baseline) &                                       
                                            (data["parallel"]==parallel)
                                            ]                        
                            list_times = np.array(df_tmp['time'].tolist())                         
                            
                            if len(list_times) > 0 :
                                time = self.calc_mean(list=list_times)    
                                record= [baseline,dataset,f'{time/1000:.2f}',f'{parallel}'.lower()]
                                df_final.loc[len(df_final)] = record
    
        return df_final 
    
    def merge_results6(self, header, baselines, datasets, parallels, path, examples, ratio):
        
        data = pd.read_csv( path, sep=',')         
        df_final = pd.DataFrame(columns = header)  

        for dataset in datasets:
            for baseline in baselines:
                for example in examples:
                    for parallel in parallels:
                                df_tmp =  data.loc[(data['dataset']==dataset) &
                                                (data['baseline']==baseline) &                                       
                                                (data["parallel"]==parallel) & 
                                                (data["example_nrows"]==example)
                                                ]                                                    
                                list_times = np.array(df_tmp['time'].tolist())                         
                                
                                if len(list_times) > 0 :                                    
                                    time = self.calc_mean(list=list_times)    
                                    record= [baseline,dataset,example,f'{time/ratio:.2f}',f'{parallel}'.lower()]
                                    df_final.loc[len(df_final)] = record
    
        return df_final 
    
    def merge_results7(self, header, baselines, datasets, parallels, path, examples, ratio, fields):
        
        data = pd.read_csv( path, sep=',')         
        df_final = pd.DataFrame(columns = header)  

        for dataset in datasets:
            for baseline in baselines:
                for example in examples:
                    for field in fields:
                        for parallel in parallels:
                                    df_tmp =  data.loc[(data['dataset']==dataset) &
                                                    (data['baseline']==baseline) &                                       
                                                    (data["parallel"]==parallel) & 
                                                    (data["example_nrows"]==example) &
                                                    (data["field"]==field)
                                                    ]                                                    
                                    list_times = np.array(df_tmp['time'].tolist())                         
                                    
                                    if len(list_times) > 0 :                                    
                                        time = self.calc_mean(list=list_times)    
                                        record= [baseline,dataset,field,example,f'{time/ratio:.2f}',f'{parallel}'.lower()]
                                        df_final.loc[len(df_final)] = record
    
        return df_final 
    
if __name__ == "__main__":
    root_path = '../../results'
    mearged_path = 'results/'

    exp1_micor_bench_identification = [f'{root_path}/Experiment1a_times.dat',
                                       f'{root_path}/Experiment1b_times.dat',
                                       f'{root_path}/Experiment1c_times.dat',
                                       f'{root_path}/Experiment1d_times.dat',
                                       f'{root_path}/Experiment1e_times.dat',
                                       f'{root_path}/Experiment1f_times.dat',
                                       f'{root_path}/Experiment1g_times.dat'] 
    
    exp2_identification_1k_10k = [f'{root_path}/Experiment2a_times.dat',
                                  f'{root_path}/Experiment2b_times.dat',
                                  f'{root_path}/Experiment2c_times.dat',
                                  f'{root_path}/Experiment2d_times.dat',
                                  f'{root_path}/Experiment2e_times.dat',
                                  f'{root_path}/Experiment2f_times.dat',
                                  f'{root_path}/Experiment2g_times.dat'] 

    exp3_early_a = f'{root_path}/Experiment3a_times.dat'
    exp3_early_b = f'{root_path}/Experiment3b_times.dat'

    exp4_micro_bench = [f'{root_path}/Experiment4a_times.dat',
                        f'{root_path}/Experiment4b_times.dat',
                        f'{root_path}/Experiment4c_times.dat',
                        f'{root_path}/Experiment4d_times.dat',
                        f'{root_path}/Experiment4e_times.dat',
                        f'{root_path}/Experiment4f_times.dat',
                        f'{root_path}/Experiment4g_times.dat'] 

    exp5a_systematic = [f'{root_path}/Experiment5aa_times.dat',
                        f'{root_path}/Experiment5ab_times.dat',
                        f'{root_path}/Experiment5ac_times.dat',
                        f'{root_path}/Experiment5ad_times.dat',
                        f'{root_path}/Experiment5ae_times.dat',
                        f'{root_path}/Experiment5af_times.dat',
                        f'{root_path}/Experiment5ag_times.dat',
                        f'{root_path}/Experiment5ah_times.dat',
                        f'{root_path}/Experiment5ai_times.dat',
                        f'{root_path}/Experiment5aj_times.dat',
                        f'{root_path}/Experiment5ak_times.dat',
                        f'{root_path}/Experiment5al_times.dat']
    
    exp5b_systematic = [f'{root_path}/Experiment5a_times.dat',
                        f'{root_path}/Experiment5b_times.dat',
                        f'{root_path}/Experiment5c_times.dat',
                        f'{root_path}/Experiment5d_times.dat',
                        f'{root_path}/Experiment5e_times.dat',
                        f'{root_path}/Experiment5f_times.dat',
                        f'{root_path}/Experiment5g_times.dat',
                        f'{root_path}/Experiment5h_times.dat',
                        f'{root_path}/Experiment5i_times.dat',
                        f'{root_path}/Experiment5j_times.dat',
                        f'{root_path}/Experiment5k_times.dat',
                        f'{root_path}/Experiment5l_times.dat']

    exp6_end_to_end = [f'{root_path}/Experiment6a_times.dat',
                       f'{root_path}/Experiment6b_times.dat']  

    exp4_results = [f'{root_path}/Experiment4l_times.dat']                   
                                           
    exp1_2_headers=["dataset","query","example_nrows","time","parallel"]
    exp3_headers=["baseline","dataset","example_nrows","time","parallel"]   
    exp4_headers=["baseline","dataset","query","time","parallel"]
    exp5a_headers=["dataset","field","example_nrows","time","parallel"] 
    exp5b_headers=["baseline","dataset","field","time","parallel"]       
    exp6_headers=["baseline","dataset","time","parallel"]  

    datasets=["aminer-author-json",
              "aminer-paper-json",
              "yelp-json",
              "yelp-csv",
              "aminer-author",
              "aminer-paper",
              "message-hl7",
              "autolead-xml",
              "susy-libsvm",
              "ReWasteF-csv",
              "mnist8m-libsvm",
              "higgs-csv",
              "queen-mm"]

    base_lines=["GIO",
                "SystemDS+JACKSON", 
                "SystemDS+GSON", 
                "SystemDS+JSON4J", 
                "RapidJSON", 
                "SystemDS+CSV",
                "Python", 
                "SystemDS+aminer-author", 
                "SystemDS+aminer-paper", 
                "SystemDS", 
                "SystemDS+Jackson",
                "SystemDS+LibSVM",
                "SystemDS+MM",
                "SystemDS+message-hl7"]  

    Q = ["Q1", "Q2", "Q3", "Q4", "Q5"]                     
    F = [f'F{n}' for n in range(0,33)]
    examples=[200,300,400,500,600,700,800,900,1000]
    examples10k=[1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
    parallel=[True, False]   

    mr = merge_results()

    #*********** exp1_micor_bench_identification ************
    for path in exp1_micor_bench_identification:
        exp_df = mr.merge_results1(fieldName="query", ratio=1,header=exp1_2_headers, datasets=datasets, parallels=parallel, projections=Q, examples=examples, path=path)
        fname = path.split("/")
        exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)  

    #*********** exp2_identification_1k_10k ************
    df_tbl3 = pd.DataFrame(index = examples10k, 
                        columns = ["Rows", "aminer-author-json-Q1", "aminer-author-json-Q2", "aminer-author-json-Q3", "aminer-author-json-Q4",
                                   "aminer-paper-json-Q1", "aminer-paper-json-Q2", "aminer-paper-json-Q3", "aminer-paper-json-Q4",
                                   "yelp-json-Q1", "yelp-json-Q2", "yelp-json-Q3", "yelp-json-Q4", "yelp-json-Q5",
                                   "aminer-author-Q1", "aminer-author-Q2", "aminer-author-Q3", "aminer-author-Q4",
                                   "aminer-paper-Q1", "aminer-paper-Q2", "aminer-paper-Q3", "aminer-paper-Q4",
                                   "yelp-csv-Q1", "yelp-csv-Q2",
                                   "message-hl7-Q1", "message-hl7-Q2"])
    
    df_tbl3["Rows"] = ["1K", "2K", "3K", "4K", "5K", "6K", "7K", "8K", "9K", "10K"]

    df_tbl3.set_index("Rows")
    for path in exp2_identification_1k_10k:
        exp_df = mr.merge_results1(fieldName="query", ratio=1000,header=exp1_2_headers, datasets=datasets, parallels=parallel, projections=Q, examples=examples10k, path=path)
        fname = path.split("/")
        if len(exp_df) > 0 :
             qs = exp_df["query"].unique()
             dataset_name = exp_df["dataset"].unique()
             nr = exp_df["example_nrows"].unique() 
             for q in qs:
                  for dn in dataset_name:
                       for n in nr:
                            value = exp_df.loc[(exp_df['dataset'] == dn) & (exp_df['example_nrows'] == n) & (exp_df['query'] == q)]["time"].item()
                            ck = f"{dn}-{q}"
                            df_tbl3.at[n,ck] = value
                           
    df_tbl3.rename(columns = {'aminer-author-json-Q1':'Q1'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-author-json-Q2':'Q2'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-author-json-Q3':'Q3'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-author-json-Q4':'Q4'}, inplace = True)

    df_tbl3.rename(columns = {'aminer-paper-json-Q1':'Q5'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-paper-json-Q2':'Q6'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-paper-json-Q3':'Q7'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-paper-json-Q4':'Q8'}, inplace = True)

    df_tbl3.rename(columns = {'yelp-json-Q1':'Q9'}, inplace = True)     
    df_tbl3.rename(columns = {'yelp-json-Q2':'Q10'}, inplace = True)
    df_tbl3.rename(columns = {'yelp-json-Q3':'Q11'}, inplace = True)
    df_tbl3.rename(columns = {'yelp-json-Q4':'Q12'}, inplace = True)
    df_tbl3.rename(columns = {'yelp-json-Q5':'Q13'}, inplace = True)

    df_tbl3.rename(columns = {'aminer-author-Q1':'Q14'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-author-Q2':'Q15'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-author-Q3':'Q16'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-author-Q4':'Q17'}, inplace = True)

    df_tbl3.rename(columns = {'aminer-paper-Q1':'Q18'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-paper-Q2':'Q19'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-paper-Q3':'Q20'}, inplace = True)
    df_tbl3.rename(columns = {'aminer-paper-Q4':'Q21'}, inplace = True)

    df_tbl3.rename(columns = {'yelp-csv-Q1':'Q22'}, inplace = True)
    df_tbl3.rename(columns = {'yelp-csv-Q2':'Q23'}, inplace = True)

    df_tbl3.rename(columns = {'message-hl7-Q1':'Q24'}, inplace = True)
    df_tbl3.rename(columns = {'message-hl7-Q2':'Q25'}, inplace = True)

   
    df_tbl3.to_csv(f'{mearged_path}/exp2_identification_1k_10k.dat', index=False)   

    
    #*********** exp3_early ************    
    exp3_headers_a = ["baseline","dataset","example_nrows","time","parallel"]
    exp3_headers_b = ["baseline","dataset","field","example_nrows","time","parallel"]

    exp_df_a = mr.merge_results6(ratio=1,header=exp3_headers_a, baselines=["GIO", "OLDGIO"], datasets=["mm-col"], parallels=parallel, path=exp3_early_a, examples=[100,200,300,400,500,600,700,800,900,1000])
    fname = exp3_early_a.split("/")
    exp_df_a.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)  
  
    exp_df_b = mr.merge_results7(ratio=1,header=exp3_headers_b, baselines=["GIO", "OLDGIO"], datasets=["mm-row"], parallels=parallel, path=exp3_early_b, examples=[200], fields=F)
    fname = exp3_early_b.split("/")
    exp_df_b.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)  
    
    #*********** exp4_micro_bench ************  
    for path in exp4_micro_bench:             
        exp_df = mr.merge_results2(fieldName="query", ratio=1,header=exp4_headers, datasets=datasets,baselines=base_lines, parallels=parallel, projections=Q, path=path)
        fname = path.split("/")
        exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)   

    #*********** exp5_systematic ************    
    for path in exp5a_systematic:  
        exp_df = mr.merge_results1(fieldName="field", ratio=1,header=exp5a_headers, datasets=datasets, parallels=parallel, projections=F, examples=examples, path=path)              
        fname = path.split("/")
        exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)  

    for path in exp5b_systematic:
        exp_df = mr.merge_results2(fieldName="field", ratio=1,header=exp5b_headers, baselines=base_lines, datasets=datasets, parallels=parallel, projections=F, path=path)
        fname = path.split("/")
        exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)  

    # for path in exp5a_results:
    #     exp_df = merge_results5(header=exp5a_headers, baselines=base_lines, datasets=datasets, parallels=parallel, path=path)
    #     fname = path.split("/")
    #     exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)   

    # for path in exp5b_results:
    #     exp_df = merge_results5(header=exp5b_headers, baselines=base_lines, datasets=datasets, parallels=parallel, path=path)
    #     fname = path.split("/")
    #     exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)          
    

