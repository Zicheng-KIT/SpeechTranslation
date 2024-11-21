import fairseq
import argparse
import torch

from fairseq.models.transformer import TransformerModel


ASR_INPUT_DEFAULT=""

ASR_CHECKPOINT_PATH="/checkpoints/"
ASR_CHECKPOINT_NAME="#TODOS2_checkpoint_best.pt"

MT_CHECKPOINT_PATH="/checkpoints/"
MT_CHECKPOINT_NAME="/home/roger/Studium/PraktikumSprachübersetzung/SpeechTranslation/fairseq/examples/translation/checkpoints/checkpoint_best.pt"
MT_META_FILE_FOLDER="/home/roger/Studium/PraktikumSprachübersetzung/SpeechTranslation/fairseq/examples/translation"
#TODO
#TEST_INPUT="/content/fairseq/examples/translation/sample_data/spm.tst.de-en.de"
#PRED_LOG="/content/fairseq/examples/translation/de-en.decode.log"

# RUN with
# python3 de_en_translation.py --source source.txt --output translated.txt


def translate(model, source_file, output_file):
    # Read source sentences
    with open(source_file, 'r') as f:
        src_lines = f.readlines()

    # Translate each line
    translations = []
    for line in src_lines:
        # Strip newline and extra spaces
        line = line.strip()
        # Translate using the model
        translated = model.translate(line)
        translations.append(translated)

    # Write translations to the output file
    with open(output_file, 'w') as f:
        for translation in translations:
            f.write(translation + '\n')

def main():
    # Command-line arguments parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, required=True, help="Path to the source text file to translate")
    parser.add_argument('--output', type=str, required=True, help="Path to save the translated output")
    args = parser.parse_args()

    # Load the model
    translation_model = TransformerModel.from_pretrained(
        MT_META_FILE_FOLDER,
        checkpoint_file=MT_CHECKPOINT_NAME,
        data_name_or_path=MT_META_FILE_FOLDER + '/data-bin/iwslt14.de-en',
        bpe='sentencepiece',  # or 'fastbpe' or 'sentencepiece' depending on the BPE used
        sentencepiece_model=MT_META_FILE_FOLDER+ '/bpe.model',
        tokenizer='moses',  # or use 'space' or other tokenizers if needed
        src_lang='de',
        tgt_lang='en'
    )

    # Perform translation
    translate(translation_model, args.source, args.output)

    print(f"Translation complete. Translated text saved to {args.output}")

if __name__ == "__main__":
    main()


