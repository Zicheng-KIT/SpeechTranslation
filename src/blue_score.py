import sacrebleu

# Load the hypothesis and reference files
with open('../datasets/SpeechTranslation/de/translation.txt', 'r') as f:
    hypothesis = f.readlines()

with open('../datasets/SpeechTranslation/de/covost_de_en_translation_ref.tsv', 'r') as f:
    reference = f.readlines()

# Calculate BLEU score
bleu = sacrebleu.corpus_bleu(hypothesis, [reference])

# Print the BLEU score
print(f"BLEU score: {bleu.score}")
