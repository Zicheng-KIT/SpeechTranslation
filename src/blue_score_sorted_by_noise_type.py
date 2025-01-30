# Reload the TSV file
import pandas as pd
import sacrebleu

df = pd.read_csv("/LanguageTranslationPraktikum/output_manifest_translated.tsv", sep="\t")

# Compute BLEU scores using sacrebleu
bleu_scores_sacrebleu = {}

for noise, group in df.groupby("noise_type"):
    references = [group["translation"].dropna().tolist()]  # sacrebleu expects a list of reference lists
    hypotheses = group["generated_translation"].dropna().tolist()  # List of hypothesis sentences

    # Compute corpus-level BLEU score
    if hypotheses:  # Ensure there are hypotheses to compare
        bleu = sacrebleu.corpus_bleu(hypotheses, references).score
        bleu_scores_sacrebleu[noise] = bleu

# Display BLEU scores per noise type
bleu_scores_sacrebleu
