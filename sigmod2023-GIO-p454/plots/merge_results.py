import pandas as pd
import sys
import os
import string
import numpy as np
import scipy.stats as stats
import re


class merge_results(object):

    def atoi(self, text):
        return int(text) if text.isdigit() else text

    def natural_keys(self, text):    
        return [ self.atoi(c) for c in re.split(r'(\d+)', text) ]

    def calc_mean_(self, list):
    
        mean = np.mean(list)
    
        std = np.std(list)
        normal_list = []
        nz=[]
        for l in list:
            if std == 0:
                break;
            z = (l-mean)/std
            if z <=0.5:
                normal_list.append(l)
            nz.append(z)
        if len(normal_list) == 0:
            avg_value = min(list)         
        else:
            avg_value = np.mean(normal_list)
        return avg_value  
    
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


    def merge_results5(self, header, baselines, datasets, parallels,path):
        
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
    
if __name__ == "__main__":
    root_path = '../results/'
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
                                  f'{root_path}/Experiment21d_times.dat',
                                  f'{root_path}/Experiment2e_times.dat',
                                  f'{root_path}/Experiment2f_times.dat',
                                  f'{root_path}/Experiment2g_times.dat'] 

    exp3_early = [f'{root_path}/Experiment3a_times.dat',
                  f'{root_path}/Experiment3b_times.dat'] 

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
    exp5_headers=["baseline","dataset","field","time","parallel"]       
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


    for path in exp1_micor_bench_identification:
        exp_df = mr.merge_results1(fieldName="query", ratio=1,header=exp1_2_headers, datasets=datasets, parallels=parallel, projections=Q, examples=examples10k, path=path)
        fname = path.split("/")
        exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)  

    for path in exp2_identification_1k_10k:
        exp_df = mr.merge_results1(fieldName="query", ratio=1,header=exp1_2_headers, datasets=datasets, parallels=parallel, projections=Q, examples=examples10k, path=path)
        fname = path.split("/")
        exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)       

    # for path in exp2_results:
    #     exp_df = merge_results2(fieldName="query", ratio=1,header=exp2_headers, baselines=base_lines, datasets=datasets, parallels=parallel, projections=Q, path=path)
    #     fname = path.split("/")
    #     exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)  

    
    # for path in exp3_results:
    #     exp_df = merge_results1(fieldName="field", ratio=1,header=exp3_headers, datasets=datasets, parallels=parallel, projections=F, examples=examples, path=path)
    #     fname = path.split("/")
    #     exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)   

    # for path in exp4_results:
    #     print(path)
    #     exp_df = merge_results2(fieldName="field", ratio=1,header=exp4_headers, baselines=base_lines, datasets=datasets, parallels=parallel, projections=F, path=path)
    #     fname = path.split("/")
    #     exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)  


    # for path in exp5a_results:
    #     exp_df = merge_results5(header=exp5a_headers, baselines=base_lines, datasets=datasets, parallels=parallel, path=path)
    #     fname = path.split("/")
    #     exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)   

    # for path in exp5b_results:
    #     exp_df = merge_results5(header=exp5b_headers, baselines=base_lines, datasets=datasets, parallels=parallel, path=path)
    #     fname = path.split("/")
    #     exp_df.to_csv(f'{mearged_path}/{fname[len(fname)-1]}', index=False)          
    

