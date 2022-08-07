import pandas as pd

def get_significative_df(val=0.1):

    df = pd.read_excel('proteomics.xlsx')
    df.rename(columns = {'Abundance Ratio Adj. P-Value: (FZR-1, Sample) / (control, Sample)':'p_value',
                         "Abundance Ratio: (FZR-1, Sample) / (control, Sample)":'abundance_ratio'
                         }, inplace=True)
    df_sig = df[df["p_value"] < val]
    #filter out contaminants
    df_sig = df_sig[df_sig['Description'].str.contains("Caenorhabditis elegans")]
    return df_sig


def get_increased_genes(df):
    df = df[df["abundance_ratio"] >= 1]
    genes = [e.split("GN=")[1].split()[0] for e in df.Description.to_list()]
    new_df = df[["abundance_ratio", "p_value"]]
    new_df["genes"] = genes
    new_df["description"] = df["Description"]
    return new_df

def get_decreased_genes(df):
    df = df[df["abundance_ratio"] <= 1]
    genes = [e.split("GN=")[1].split()[0] for e in df.Description.to_list()]
    new_df = df[["abundance_ratio", "p_value"]]
    new_df["genes"] = genes
    new_df["description"] = df["Description"]
    return new_df

df = get_significative_df()
get_increased_genes(df).to_excel("increased_genes.xlsx", index=False)
get_decreased_genes(df).to_excel("decreased_genes.xlsx", index=False)