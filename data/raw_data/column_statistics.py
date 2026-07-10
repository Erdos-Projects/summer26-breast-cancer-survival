import pandas as pd

# Load the dataset
df = pd.read_csv('brca_metabric_clinical_data.tsv', sep='\t')
total = len(df)

# Build the statistics dataframe
stats = pd.DataFrame({
    'Column': df.columns,
    'Data Type': df.dtypes.astype(str).values,
    'Non-null Entries': df.notna().sum().values,
    'Missing Entries': df.isna().sum().values,
    'Completeness (%)': (df.notna().sum().values / total * 100).round(2)
})

# Format completeness with % sign
stats['Completeness (%)'] = stats['Completeness (%)'].apply(lambda x: f'{x}%')

# Convert to markdown and save
md_header = f'## METABRIC Dataset — Column Statistics\n\n**Total rows:** {total}\n\n'
md_table = stats.to_markdown(index=False)

with open('metabric_column_statistics.md', 'w') as f:
    f.write(md_header + md_table)

print(f'Saved metabric_column_statistics.md ({len(stats)} columns)')
