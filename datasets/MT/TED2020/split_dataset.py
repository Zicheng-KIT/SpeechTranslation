# split of the example dataset from the notebook
# train 174443 ~96,2%
# test 4698 ~2,6%
# dev 2052 ~1,2%
# total 181193

import re


def split_parallel_datasets(
    german_file_path, english_file_path, german_output_paths, english_output_paths
):
    brackets_pattern = re.compile(r"\(.*?\)")


    filtered_lines = []
    with open(german_file_path, encoding="utf-8") as german_file, open(
        english_file_path, encoding="utf-8"
    ) as english_file:
        for german_line, english_line in zip(german_file, english_file):
            if (
                german_line.strip()
                and english_line.strip()
                and not brackets_pattern.search(english_line)
                and not brackets_pattern.search(german_line)
                and len(german_line.split()) <= 20
            ):
                filtered_lines.append((german_line, english_line))

    print(f"Filtered Dataset size: {len(filtered_lines)}")

    total_samples = len(filtered_lines)
    train_end = int(total_samples * 0.96)
    test_end = int(total_samples * 0.98)
    splits = {
        "train": filtered_lines[:train_end],
        "test": filtered_lines[train_end:test_end],
        "dev": filtered_lines[test_end:],
    }

    # Write each split to the corresponding output files
    for split_name, split_data in splits.items():
        with open(
            german_output_paths[split_name], "w", encoding="utf-8"
        ) as german_output, open(
            english_output_paths[split_name], "w", encoding="utf-8"
        ) as english_output:
            for german_line, english_line in split_data:
                german_output.write(german_line)
                english_output.write(english_line)


# Define file paths
name = "TED2020"
base_path = f"./datasets/{name}"
output_folder = "/sample_data"
german_file_path = f"{base_path}/{name}.de-en.de"
english_file_path = f"{base_path}/{name}.de-en.en"

german_output_paths = {
    key: f"{base_path}{output_folder}/{split}.de-en.de"
    for key, split in {"train": "train", "test": "tst", "dev": "dev"}.items()
}
english_output_paths = {
    key: f"{base_path}{output_folder}/{split}.de-en.en"
    for key, split in {"train": "train", "test": "tst", "dev": "dev"}.items()
}

split_parallel_datasets(
    german_file_path, english_file_path, german_output_paths, english_output_paths
)
