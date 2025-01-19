import heapq
import os
import subprocess
from pathlib import Path
import pickle
import fairseq
import argparse
import numpy as np
import pandas as pd
import torch
import torchaudio
from fairseq import checkpoint_utils
from fairseq.examples.speech_to_text.data_utils import save_df_to_tsv, extract_fbank_features, create_zip, \
    get_zip_manifest
from fairseq.models.transformer import TransformerModel
from tqdm import tqdm
from torchaudio.datasets import COMMONVOICE

# If you got 'an undefined symbol' error, check your torch_version.
# my_torch_version == 2.1.0 and my_torchaudio_version == 2.1.0


ROOT_DIR = Path("../datasets/SpeechTranslation/de/")
test_data = COMMONVOICE(ROOT_DIR, tsv="filtered_test_modified_client_id.tsv") # len = 16188

ASR_INPUT_DEFAULT=""
ASR_ROOT_PATH="../../trainedModels/S2"
ASR_CHECKPOINT_PATH="../../trainedModels/S2/S2_checkpoint_best.pt"
ASR_OUTPUT_PATH="..//datasets/SpeechTranslation/de/"
MT_ROOT_PATH="../../trainedModels/S1/"
MT_CHECKPOINT_NAME="../../trainedModels/S1/S1_checkpoint_best.pt"
MT_OUTPUT_PATH="../datasets/SpeechTranslation/de/"

#TODO
#TEST_INPUT="/content/fairseq/examples/translation/sample_data/spm.tst.de-en.de"
#PRED_LOG="/content/fairseq/examples/translation/de-en.decode.log"



def preprocess_audio_files():
    # Define file path to store the features
    feature_root = ROOT_DIR / "fbank80"
    feature_root.mkdir(exist_ok=True)

    # Extract features of all audios in all data splits
    for dataset in [test_data]:
        print(f"Extracting log mel filter bank features of audio")
        for wav, sample_rate, metadata in tqdm(dataset):
            sample_id = f"{metadata['client_id']}"
            extract_fbank_features(
                wav, sample_rate, feature_root / f"{sample_id}.npy"
            )

    # Pack audio features into ZIP
    zip_path = ROOT_DIR / "fbank80.zip"
    print("ZIPing features...")
    create_zip(feature_root, zip_path)  # len = 628374

    print("Fetching audio manifest...")
    audio_paths, audio_lengths = get_zip_manifest(zip_path)

    with open(ROOT_DIR / 'audio_manifest.pkl', 'wb') as f:
        pickle.dump((audio_paths, audio_lengths), f)
    print("Saved as audio_manifest.pkl")

    with open(ROOT_DIR / 'audio_manifest.pkl', 'rb') as file:
        audio_paths, audio_lengths = pickle.load(file)

    MANIFEST_COLUMNS = ["id", "audio", "n_frames", "tgt_text", "speaker"]
    #for dataset, split_name in zip([train_data, dev_data, test_data],["train-clean", "dev-clean", "test-clean"]):
    for dataset, split_name in zip([test_data], ["test-clean"]):
        print(f"Fetching manifest from {split_name}...")
        manifest = {c: [] for c in MANIFEST_COLUMNS}
        for _, _, metadata in tqdm(dataset):
            try:
                sample_id = f"{metadata['client_id']}"
                manifest["id"].append(sample_id)
                manifest["audio"].append(audio_paths[sample_id])
                manifest["n_frames"].append(audio_lengths[sample_id])
                manifest["tgt_text"].append(metadata['sentence'])
                manifest["speaker"].append(metadata['client_id'])
            except KeyError as e:
                print(f'ERROR: couldn\'t load audio path for sample_id: {sample_id}')
            except ValueError as e:
                print(f'ERROR: regarding {sample_id}. {e}')

        save_df_to_tsv(pd.DataFrame.from_dict(manifest), ROOT_DIR / f"{split_name}.tsv")

    print("Preprocessing and transcription complete!")

def run_fairseq_transcription():
    # Construct the Fairseq generate command for transcription or translation



    command = [
        "fairseq-generate",
        "../../SpeechTranslation/datasets/SpeechTranslation/de/", # Path to the data directory (source or transcriptions)
        "--task", "speech_to_text",
        "--arch", "s2t_transformer_s",
        "--config-yaml", "../../SpeechTranslation/datasets/SpeechTranslation/de/config.yaml",
        "--path", "../../SpeechTranslation/datasets/SpeechTranslation/de/S2_checkpoint_best.pt",# Path to the model checkpoint
        "--gen-subset", "test-clean",  # Subset to generate (e.g., test set)
        "--remove-bpe",
        "--bpe", "sentencepiece",
        #"--temperature", "1.0",
        "--batch-size", "1",
        "--beam", "5",  # Beam size for beam search (higher = better)
        "--max-tokens", "50000",  # Maximum number of tokens per batch
        "--cpu",  # Run on CPU (use --cuda for GPU if available)
        "--scoring", "wer",
        "--results-path",
        ASR_OUTPUT_PATH,
    ]
    # Run the command and capture the output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    if result.returncode == 0:
        print("Generation completed successfully.")
        return result.stdout
    else:
        print("Error occurred during generation.")
        print(result.stderr)
        return None

def extract_hyp():
    # Define the paths to log and output directories
    pred_log = ASR_OUTPUT_PATH + '/generate-test-clean.txt'
    pred_output_dir = ASR_OUTPUT_PATH  # Replace with your output directory

    # Ensure the output directory exists
    os.makedirs(pred_output_dir, exist_ok=True)

    # Output file paths
    hyp_file = os.path.join(pred_output_dir, 'hyp.txt')
    ref_file = os.path.join(pred_output_dir, 'ref.txt')

    # Function to process the lines in the log file
    def process_log_file(log_file, output_file, line_prefix, column_index):
        with open(log_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in tqdm(infile):
                if line.startswith(line_prefix):
                    # Remove the prefix (e.g., "D-" or "T-")
                    line = line[len(line_prefix):]
                    # Split by tab and select the relevant column (index starts at 0)
                    parts = line.split('\t')
                    if len(parts) > column_index:
                        # Clean up the part (remove " ##" and write to output file)
                        cleaned_line = parts[column_index].replace(' ##', '').strip()
                        outfile.write(cleaned_line + '\n')

    # Process the log file for hypothesis lines (starting with 'D')
    process_log_file(pred_log, hyp_file, 'D', 2)  # 'D' prefix and 3rd column (index 2)

    # Process the log file for reference lines (starting with 'T')
    process_log_file(pred_log, ref_file, 'T', 1)  # 'T' prefix and 2nd column (index 1)

    # Display the first few lines of the hypothesis file (equivalent to `head hyp.txt`)
    with open(hyp_file, 'r') as file:
        print("First few lines of hyp.txt:")
        for i, line in enumerate(file):
            if i >= 10:  # Only print the first 10 lines
                break
            print(line.strip())


def extract_and_sort_hypothesis(input_filename, output_filename):
    # Open the input file for reading
    with open(input_filename, 'r') as input_file:
        # Create a heap (priority queue) to keep track of the lines sorted by their ID
        hypothesis_lines = []

        # Read the file line by line to avoid loading the entire file into memory
        for line in input_file:
            if line.startswith('D-'):  # Only process hypothesis lines
                # Split the line into ID and hypothesis sentence
                parts = line.split('\t')
                if len(parts) > 1:
                    # Extract the hypothesis sentence (the part after the first tab)
                    hypothesis = parts[2].strip()
                    # Push the (ID, hypothesis) pair into the heap, sorting by the ID
                    heapq.heappush(hypothesis_lines, (parts[0], hypothesis))

    # Write sorted hypothesis lines to the output file
    with open(output_filename, 'w') as output_file:
        while hypothesis_lines:
            _, hypothesis = heapq.heappop(hypothesis_lines)  # Get the sorted hypothesis
            output_file.write(f"{hypothesis}\n")

    print(f"Extracted and sorted hypothesis lines saved to {output_filename}")

def translate(model, source_file, output_file):
    # Read source sentences
    with open(source_file, 'r') as f:
        src_lines = f.readlines()

    # Translate each line
    print("Translate each line")
    # Write translations to the output file
    with open(output_file, 'w') as f:
        translations = []
        for line in tqdm(src_lines):
            # Strip newline and extra spaces
            line = line.strip()
            # Translate using the model
            translated = model.translate(line)
            f.write(translated + '\n')

def main():
    # Command-line arguments parsing
    #preprocess_audio_files()
    #return
    #run_fairseq_transcription()
    #return

    #extract_hyp()
    #pred_log = ASR_OUTPUT_PATH + '/generate-test-clean.txt'
    #hyp_file = os.path.join(ASR_OUTPUT_PATH, 'hyp.txt')
    #extract_and_sort_hypothesis(pred_log, hyp_file)

    # Load the model
    translation_model = TransformerModel.from_pretrained(
        MT_ROOT_PATH,
        checkpoint_file=MT_CHECKPOINT_NAME,
        data_name_or_path=MT_ROOT_PATH + '/data-bin/iwslt14.de-en',
        bpe='sentencepiece',  # or 'fastbpe' or 'sentencepiece' depending on the BPE used
        sentencepiece_model=MT_ROOT_PATH + '/bpe.model',
        tokenizer='moses',  # or use 'space' or other tokenizers if needed
        src_lang='de',
        tgt_lang='en'
    )

    # Perform translation
    translate(translation_model, ASR_OUTPUT_PATH + 'hyp.txt', MT_OUTPUT_PATH + 'translation.txt')

    print(f"Translation complete. Translated text saved to {MT_OUTPUT_PATH + 'translation.txt'}")

if __name__ == "__main__":
    main()


