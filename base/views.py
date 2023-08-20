from django.shortcuts import render
from django.http import JsonResponse
from codingex.settings import BASE_DIR
import os        
import pandas as pd
import json 

def get_unique_values(request):
    file_path_1 = os.path.join(BASE_DIR, r'codingex/coding_exercise/9606_abund.txt')
    df_1 = pd.read_csv(file_path_1, sep='\t', header=None)
    df2 = df_1[[2,3]].drop_duplicates().reset_index()
    unique_values = len(df2)
    
    #B1 question# 
    file_path = os.path.join(BASE_DIR, r'codingex/coding_exercise/9606_gn_dom.txt')
    df = pd.read_csv(file_path, sep='\t', header=None)
    
    #replaced column names (first row is column names)
    new_header = df.iloc[0].to_list()
    df = df[1:]
    df.columns = new_header

    #new dataframe with only relevant columns
    df1 = df[['#Gn','Domain']]

    #finding highest average occurrence
    domain_counts = df1.groupby('Domain')['#Gn'].count().reset_index()
    domain_counts.rename(columns={'#Gn':'Occurrences'}, inplace=True)
    total_gene_products = len(df1['#Gn'].unique())
    domain_counts['Average Occurrence'] = domain_counts['Occurrences'] / total_gene_products
    highest_average_domain = domain_counts['Domain'][domain_counts['Average Occurrence'].idxmax()]
    highest_average_occurrence = domain_counts['Average Occurrence'].max()

    # send data / context to template 
    context = {
        'unique_values':unique_values,
        'highest_average_domain':highest_average_domain,
        'highest_average_occurrence':highest_average_occurrence,
    }
    return render(request, 'index.html', context)

def get_mean_std(request): 

    file_path = os.path.join(BASE_DIR, r'codingex/coding_exercise/9606_abund.txt')
    df = pd.read_csv(file_path, sep='\t', header=None)

        # -2 and sort_values to remove >#Taxid Ensembl_protein Gn Mean-copy-number< *and* >#Taxid Paxid GN Mean<
    mean_std_raw = pd.DataFrame(df, columns=[2, 3]).sort_values(by=3)[:-2]

        # Convert 3rd column ( Mean-copy-number ) to float 
    mean_std_raw = mean_std_raw.astype({2:'string', 3:'float64'})

        # Create two new columns "mean" and "standard deviation", reset_index to save gene names
    mean_std_sorted = mean_std_raw.groupby(2).agg(["mean", "std"]).reset_index()
        # Convert and display as json 
    out_2 = mean_std_sorted.to_json(orient='records')
    ajax_json_a2 = json.loads(out_2)

    return JsonResponse({'out_a2':ajax_json_a2})

def get_percentile_rank(request):

    file_path = os.path.join(BASE_DIR, r'codingex/coding_exercise/9606_abund.txt')
    df = pd.read_csv(file_path, sep='\t', header=None)
    df1 = df[[1,2,3]]

        # Have to sort data so 
        # >#Taxid Ensembl_protein Gn Mean-copy-number< 
        # *and* 
        # >#Taxid Paxid GN Mean<
        # go to the bottom of the list 
        # and remove them ( cleaning data )
    df1 = df1.sort_values(by=3)[:-2]
    df1 = df1.astype({1:'string', 2:'string', 3:'float64'}).drop_duplicates().reset_index()
    # df1 = df1.drop_duplicates().reset_index()
    df1['percentile'] = df1[3].rank(pct=True)
    df1.drop(index=df1.index[0], axis=0, inplace=True)
    print(df1)

    out_3 = df1.to_json(orient='records')
    ajax_json_a3 = json.loads(out_3)

    return JsonResponse({'out_a3':ajax_json_a3[:-2]})
