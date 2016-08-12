import pyMIC

"""
Keep the input files in the same directory to run this test
"""

tf_list_file = "test_gene_list.txt"
gene_exp_file = "Spellman.csv"
rf = open("TF_genes.csv", "w")

results,valid_TF = some_vs_rest(tf_list_file,gene_exp_file,4,100)

for i in range(len(valid_TF)):
    rf.write(valid_TF[i])
    for j in range(len(valid_TF)):
        rf.write("\t"+str(len(set(results[i]).intersection(set(results[j])))))
    rf.write("\n")
