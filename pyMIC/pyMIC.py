from __future__ import print_function
import os
import sys
from joblib import Parallel, delayed
import multiprocessing

def processInput(i,gene_exp_file,cutoff=100):
    #carefull about cutoff this could cause a bug
    #command = "java -jar MINE.jar "+gene_exp_file+" "+str(i)+" notify=500 >/dev/null"
    command = "java -jar MINE.jar "+gene_exp_file+" "+str(i)  
    os.system(command)
    os.system("rm "+gene_exp_file+",mv="+str(i)+",cv=0.0,B=n^0.6,Status.txt")
    os.system("mv "+gene_exp_file+",mv="+str(i)+",cv=0.0,B=n^0.6,Results.csv mycsv"+str(i)+".csv")
    top_genes = os.popen("cat mycsv"+str(i)+".csv | cut -d ',' -f2").read().split('\n')[1:cutoff] # get the top cutoff genes correlated with the TF
    os.system("rm mycsv"+str(i)+".csv")
    return top_genes


def some_vs_rest(tf_list_file,gene_exp_file,ncores=4,cutoff=100):

    tf_list = os.popen("cat "+tf_list_file+" | cut -d '\t' -f1").read().split('\n')
    if(gene_exp_file.split(".")[1] == "txt"):
        gene_list = os.popen("cat "+gene_exp_file+" | cut -d '\t' -f1").read().split('\n')
    elif(gene_exp_file.split(".")[1] == "csv"):
        gene_list = os.popen("cat "+gene_exp_file+" | cut -d ',' -f1").read().split('\n')
    else:
        print("File type error")
        sys.exit(0)


    valid_TF = []
    TF_index = []
    for tf in tf_list:
        try:
            TF_index.append(gene_list.index(tf))
            valid_TF.append(tf)
        except ValueError:
            pass



    inputs = TF_index # Test with only 10 TFs
    valid_TF = valid_TF
    print(str(len(valid_TF))+" number of TFs will be compared with"+str(len(gene_list))+" number of genes for assiciations")

    num_cores = ncores #multiprocessing.cpu_count()     
    results = Parallel(n_jobs=num_cores)(delayed(processInput)(i,gene_exp_file,cutoff) for i in inputs)
    return results,valid_TF



if __name__=='__main__':

    #file names
    tf_list_file = "test_gene_list.txt"
    gene_exp_file = "Spellman.csv"
    rf = open("TF_genes.csv", "w")

    results,valid_TF = some_vs_rest(tf_list_file,gene_exp_file,4,100)

    for i in range(len(valid_TF)):
        rf.write(valid_TF[i])
        for j in range(len(valid_TF)):
            rf.write("\t"+str(len(set(results[i]).intersection(set(results[j])))))
        rf.write("\n")

