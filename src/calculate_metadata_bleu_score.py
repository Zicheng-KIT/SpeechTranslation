import sacrebleu
import csv

# Path to the TSV file
tsv_file_path = 'updated_covost_v2_with_hypothesis_column.tsv'

# Metadata filters
valid_genders = ['male', 'female']
valid_accents = ['germany', 'austria', 'switzerland']
valid_ages = ['teens', 'twenties', 'thirties', 'forties', 'fifties', 'sixties', 'seventies']

# Initialize dictionaries for storing references and hypotheses by metadata
metadata_categories = {
    'gender': valid_genders,
    'accent': valid_accents,
    'age': valid_ages
}
references_by_metadata = {key: {value: [] for value in values} for key, values in metadata_categories.items()}
hypotheses_by_metadata = {key: {value: [] for value in values} for key, values in metadata_categories.items()}

# Read the TSV file
with open(tsv_file_path, 'r', encoding='utf-8') as tsv_file:
    reader = csv.DictReader(tsv_file, delimiter='\t')
    
    for row in reader:
        text = row.get('translation', '').strip()
        hypothesis = row.get('hypothesis', '').strip()
        gender = row.get('gender', '').strip().lower()
        accent = row.get('accent', '').strip().lower()
        age = row.get('age', '').strip().lower()
        
        if hypothesis:
            
            # Store unfiltered hypothesis and reference for each metadata category
            if gender in valid_genders:
                references_by_metadata['gender'][gender].append(text)
                hypotheses_by_metadata['gender'][gender].append(hypothesis)
            if accent in valid_accents:
                references_by_metadata['accent'][accent].append(text)
                hypotheses_by_metadata['accent'][accent].append(hypothesis)
            if age in valid_ages:
                references_by_metadata['age'][age].append(text)
                hypotheses_by_metadata['age'][age].append(hypothesis)

# Calculate and print BLEU scores for each metadata category
for category, values in metadata_categories.items():
    print(f"\nBLEU scores by {category}:")
    for value in values:
        references = references_by_metadata[category][value]
        hypotheses = hypotheses_by_metadata[category][value]
        if references and hypotheses:
            bleu = sacrebleu.corpus_bleu(hypotheses, [references])
            print(f"{value.capitalize()}: {bleu.score} (Samples: {len(references)})")
        else:
            print(f"{value.capitalize()}: No data available")