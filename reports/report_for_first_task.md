# Lap Report for First Notebook

## Decisions we made
- First we want to focus on translation of knowladge based text.
- We want to use the Wikimedia dataset from OPUS. For more information on the dataset visit http://opus.lingfil.uu.se/LREC2012.txt. 
- Our model should translate from german to english.

## Data Preprocessing

During the preprocessing of the Wikimedia dataset for training our model, we encountered various types of unwanted content that could degrade the quality of our model. To enhance the dataset's quality, we applied a series of filters to remove irrelevant or noisy data, ensuring that the training material consisted of clean and meaningful text suitable for translation tasks.

| **Issue**                                                                                                                                                 | **Resolution**                                                                                                                                                                                                                                 |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Presence of lines that are section headers or standalone keywords like "References", "External links", "See also", which do not contribute meaningful content for training.                       | Applied an exact match filter to remove any lines that exactly match a predefined list of such keywords, ignoring case sensitivity.                                                                                          |
| Lines containing links, citations, or navigational symbols such as "archived", "retrieved", "↑", "→", "http", introducing noise and irrelevant information into the dataset.                     | Implemented a contains filter to exclude any lines that contain these substrings anywhere within the text, regardless of their position, and without considering case sensitivity.                                         |
| Lines with excessive numerical data, such as multiple dates, reference numbers, or codes, which are not useful for training a translation model and could make the performance worse.             | Used regular expressions to filter out lines containing four or more occurrences of numbers with three or more digits, or any occurrence of numbers with five or more digits.                      |


## Challanges we stumbled upon
- Running Notebook on cluster.
- Finding a suitable dataset.
  - Which critirias are decisive?
  - Cleaning the dataset in order to make it usable for our purpose.

### Contributors
Odin Göggerle, Zicheng Guo, Johannes Wesch
