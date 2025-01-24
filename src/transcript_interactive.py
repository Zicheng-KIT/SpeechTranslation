import subprocess

# Configuration
MODEL_CHECKPOINT = "/PraktikumSprachübersetzung/trainedModels/S2/S2_checkpoint_best.pt"
TSV_FILE = "/PraktikumSprachübersetzung/Noise/file_paths.txt"  # Path to your .txt file
OUTPUT_FILE = "/PraktikumSprachübersetzung/Noise/output.txt"  # Path to your .txt file

SPM_MODEL = "PraktikumSprachübersetzung/trainedModels/S2/spm_unigram50000.model"

def run_inference(tsv_file, model_checkpoint, spm_model):
    """
    Run fairseq-interactive for transcription.
    """
    cmd = [
        "fairseq-interactive",
        "/PraktikumSprachübersetzung/Noise",
        "--task", "speech_to_text",
        "--path", model_checkpoint,
        "--nbest", "1",
        "--config-yaml", "/PraktikumSprachübersetzung/trainedModels/S2/config.yaml",
        "--bpe", "sentencepiece",
        "--batch-size", "1",
        "--input", TSV_FILE,
        "--max-source-positions", "60000",
        "--max-tokens", "6000000",
        "--sentencepiece-model", spm_model,
    ]

    # Run the command and capture output
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print("Error during inference:")
        print(stderr)
        return

    # Parse predictions
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:
        for line in stdout.split("\n"):
            if line.startswith("D-"):
                _, _, transcription = line.split("\t")
                out_file.write(transcription + '\n')
                print("Transcription:", transcription)

if __name__ == "__main__":
    run_inference(TSV_FILE, MODEL_CHECKPOINT, SPM_MODEL)