from intermine.webservice import Service
import pandas as pd

def get_protein_sequence(gene_name):
    if "CELE_" in gene_name:
        gene_name = gene_name.split("CELE_")[1]
    service = Service("http://im-dev1.wormbase.org/tools/wormmine/service")
    query = service.new_query("Gene")
    query.add_view(
        "symbol", "transcripts.CDSs.protein.primaryIdentifier",
        "transcripts.CDSs.protein.symbol",
        "transcripts.CDSs.protein.sequence.residues"
    )
    query.add_constraint("symbol", "=", gene_name, code="A")

    with open('1_fastas.txt', 'a') as f:
        for row in query.rows():
            f.write(">"+row["symbol"]+":"+row["transcripts.CDSs.protein.symbol"]+"\n"+row["transcripts.CDSs.protein.sequence.residues"]+"\n")

    for row in query.rows():
        print(row["symbol"], row["transcripts.CDSs.protein.primaryIdentifier"], \
              row["transcripts.CDSs.protein.symbol"], row["transcripts.CDSs.protein.sequence.residues"])

df = pd.read_excel('increased_genes.xlsx')
genes = df.genes.to_list()
for gene in genes:
    get_protein_sequence(gene)


