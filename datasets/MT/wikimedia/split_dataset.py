# split of the example dataset from the notebook
# train 174443 ~96,2%
# test 4698 ~2,6%
# dev 2052 ~1,2%
# total 181193

import re


def split_parallel_datasets(
    german_file_path, english_file_path, german_output_paths, english_output_paths
):
    # Keywords to match for exact lines
    EXACT_KEYWORDS = [
        "References",
        "External links",
        "See also",
        "Life",
        "Literature",
        "Pictures",
        "Sources",
        "Links",
        "History",
        "Leben",
        "Geschichte",
        "+ Add translation",
    ]
    # Keywords to search for within lines
    CONTAINS_KEYWORDS = ["archived", "retrieved", "↑", "→", "http"]

    # Compile patterns for filtering
    exact_pattern = re.compile(
        r"^(" + r"|".join(map(re.escape, EXACT_KEYWORDS)) + r")$", re.IGNORECASE
    )
    contains_pattern = re.compile(
        r"|".join(map(re.escape, CONTAINS_KEYWORDS)), re.IGNORECASE
    )
    digit_pattern_two = re.compile(r"(\d{3,})")
    digit_pattern_five = re.compile(r"(\d{5,})")

    def filter_line(line: str):
        return (
            exact_pattern.match(line.strip())
            or contains_pattern.search(line)
            or len(digit_pattern_two.findall(line)) >= 4
            or len(digit_pattern_five.findall(line)) >= 1
        )

    filtered_lines = []
    with open(german_file_path, encoding="utf-8") as german_file, open(
        english_file_path, encoding="utf-8"
    ) as english_file:
        for german_line, english_line in zip(german_file, english_file):
            if not (filter_line(german_line) or filter_line(english_line)):
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
name = "wikimedia"
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
