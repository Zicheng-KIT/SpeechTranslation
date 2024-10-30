# split of the example dataset from the notebook
# train 174443 ~96,2%
# test 4698 ~2,6%
# dev 2052 ~1,2%
# total 181193

import re


def split_parallel_datasets(file_path_de, file_path_en, output_dict_de, output_dict_en):
    """
    Split parallel German-English datasets into train, test, and dev sets based on specified percentages,
    and filter out datapoints that contain any of the specified keywords in either language.

    :param file_path_de: Path to the German dataset file.
    :param file_path_en: Path to the English dataset file.
    :param output_dict_de: Dictionary with keys 'train', 'test', 'dev' and corresponding output file paths for German.
    :param output_dict_en: Dictionary with keys 'train', 'test', 'dev' and corresponding output file paths for English.
    """

    PERCENTAGES = {"train": 96, "test": 2, "dev": 2}
    KEYWORDS = [
        "archived",
        "retrieved",
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
    ]

    # Compile a pattern for keywords to filter lines
    pattern = re.compile(
        r"|".join(re.escape(keyword) for keyword in KEYWORDS), re.IGNORECASE
    )

    with open(file_path_de, "r", encoding="utf-8") as f_de, open(
        file_path_en, "r", encoding="utf-8"
    ) as f_en:
        lines_de = f_de.readlines()
        lines_en = f_en.readlines()

    print(f"Original Dataset size: {len(lines_de)}")

    assert len(lines_de) == len(
        lines_en
    ), "German and English datasets must have the same number of lines."

    filtered_lines_de, filtered_lines_en = [], []
    for line_de, line_en in zip(lines_de, lines_en):
        if not (pattern.match(line_de.strip()) or pattern.match(line_en.strip())):
            filtered_lines_de.append(line_de)
            filtered_lines_en.append(line_en)

    print(f"Filtereds Dataset size: {len(filtered_lines_de)}")

    # Split filtered lines into train, test, and dev
    total_samples = len(filtered_lines_de)
    train_idx = int(total_samples * (PERCENTAGES["train"] / 100))
    test_idx = train_idx + int(total_samples * (PERCENTAGES["test"] / 100))

    train_lines_de, test_lines_de, dev_lines_de = (
        filtered_lines_de[:train_idx],
        filtered_lines_de[train_idx:test_idx],
        filtered_lines_de[test_idx:],
    )
    train_lines_en, test_lines_en, dev_lines_en = (
        filtered_lines_en[:train_idx],
        filtered_lines_en[train_idx:test_idx],
        filtered_lines_en[test_idx:],
    )

    # Write the splits to corresponding output files for German and English
    with open(output_dict_de["train"], "w", encoding="utf-8") as f:
        f.writelines(train_lines_de)
    with open(output_dict_de["test"], "w", encoding="utf-8") as f:
        f.writelines(test_lines_de)
    with open(output_dict_de["dev"], "w", encoding="utf-8") as f:
        f.writelines(dev_lines_de)

    with open(output_dict_en["train"], "w", encoding="utf-8") as f:
        f.writelines(train_lines_en)
    with open(output_dict_en["test"], "w", encoding="utf-8") as f:
        f.writelines(test_lines_en)
    with open(output_dict_en["dev"], "w", encoding="utf-8") as f:
        f.writelines(dev_lines_en)

    print(
        f"Dataset split completed with {len(train_lines_de)} train, {len(test_lines_de)} test, and {len(dev_lines_de)} dev samples for German and English datasets."
    )


file_path = "./datasets/de-en.txt"
split_path = "/sample_data"
file_path_de = f"{file_path}/wikimedia.de-en.de"
file_path_en = f"{file_path}/wikimedia.de-en.en"

output_dict_de = {
    "train": f"{file_path}{split_path}/train.wikimedia.de-en.de",
    "test": f"{file_path}{split_path}/tst.wikimedia.de-en.de",
    "dev": f"{file_path}{split_path}/dev.wikimedia.de-en.de",
}

output_dict_en = {
    "train": f"{file_path}{split_path}/train.wikimedia.de-en.en",
    "test": f"{file_path}{split_path}/tst.wikimedia.de-en.en",
    "dev": f"{file_path}{split_path}/dev.wikimedia.de-en.en",
}

split_parallel_datasets(file_path_de, file_path_en, output_dict_de, output_dict_en)
