import sacrebleu

# Load the hypothesis and reference files
with open('/home/roger/Studium/PraktikumSprachübersetzung/SpeechTranslation/datasets/SpeechTranslation/de/translation.txt', 'r') as f:
    hypothesis = f.readlines()

with open('/home/roger/Studium/PraktikumSprachübersetzung/SpeechTranslation/datasets/SpeechTranslation/de/ref.txt', 'r') as f:
    reference = f.readlines()

# Calculate BLEU score
bleu = sacrebleu.corpus_bleu(hypothesis, [reference])

# Print the BLEU score
print(f"BLEU score: {bleu.score}")