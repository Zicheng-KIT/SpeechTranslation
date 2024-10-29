# split of the example dataset from the notebook
# train 174443 ~96,2%
# test 4698 ~2,6%
# dev 2052 ~1,2%
# total 181193

import random

def split_dataset(file_path, output_dict, percentages):
    """
    Split a dataset into train, test, and dev sets based on specified percentages.
    
    :param file_path: Path to the original dataset file.
    :param output_dict: Dictionary with keys 'train', 'test', 'dev' and corresponding output file paths.
    :param percentages: Dictionary with keys 'train', 'test', 'dev' and corresponding percentages (summing up to 100).
    """

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_samples = len(lines)
    train_idx = int(total_samples * (percentages['train'] / 100))
    test_idx = train_idx + int(total_samples * (percentages['test'] / 100))
    
    train_lines = lines[:train_idx]
    test_lines = lines[train_idx:test_idx]
    dev_lines = lines[test_idx:]
    
    with open(output_dict['train'], 'w', encoding='utf-8') as f:
        f.writelines(train_lines)
    with open(output_dict['test'], 'w', encoding='utf-8') as f:
        f.writelines(test_lines)
    with open(output_dict['dev'], 'w', encoding='utf-8') as f:
        f.writelines(dev_lines)
    
    print(f"Dataset split completed with {len(train_lines)} train, {len(test_lines)} test, and {len(dev_lines)} dev samples for {file_path}.")

file_path = './datasets/de-en.txt'
percentages = {
    'train': 96,
    'test': 2,
    'dev': 2
}

files = {
    'de': 'wikimedia.de-en.de',
    'en': 'wikimedia.de-en.en'
}

for lang, filename in files.items():
    input_file = f"{file_path}/{filename}"
    output_dict = {
        'train': f"{file_path}/train.{filename}",
        'test': f"{file_path}/test.{filename}",
        'dev': f"{file_path}/dev.{filename}"
    }
    split_dataset(input_file, output_dict, percentages)