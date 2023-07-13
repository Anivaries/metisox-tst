from django.shortcuts import render
from django.http import JsonResponse
from codingex.settings import BASE_DIR
import os        
import pandas as pd
import json 

def read_file(request):
    file_path_1 = os.path.join(BASE_DIR, r'codingex/coding_exercise/9606_abund.txt')
    df_1 = pd.read_csv(file_path_1, sep='\t', header=None)

    unique_values_copy = df_1[3].nunique()
    unique_values_gene = df_1[2].nunique()
    # send data / context to template 
    context = {
        'unique_values_c':unique_values_copy,
        'unique_values_g':unique_values_gene,
    }
    return render(request, 'index.html', context)

def ajax_a3(request):

    file_path = os.path.join(BASE_DIR, r'codingex/coding_exercise/9606_abund.txt')
    df = pd.read_csv(file_path, sep='\t', header=None)
    df['percent_rank']=df[3].rank(pct=True)
        # Have to sort data so >#Taxid Ensembl_protein Gn Mean-copy-number< *and* >#Taxid Paxid GN Mean<
        # go to the bottom of the list 
    percentile_rank = df.sort_values(by=['percent_rank'])
    perc_drop_dupl = percentile_rank.drop_duplicates()
    out_3 = perc_drop_dupl.to_json(orient='records')
    ajax_json_a3 = json.loads(out_3)
        # -2 to remove >#Taxid Ensembl_protein Gn Mean-copy-number< *and* >#Taxid Paxid GN Mean<
    return JsonResponse({'out_a3':ajax_json_a3[:-2]})
    

def ajax_a2(request): 

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
