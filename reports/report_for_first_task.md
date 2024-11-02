# Lab Report for First Notebook
We organize our project on this https://github.com/JohannesWesch/SpeechTranslation github repo.    
We decided our model should translate from german to english.
We had problems getting good results after training with the Wikimedia and News-Commentary dataset. After much cleaning and optimizing of the first two datasets we also tried the ted talk 2020 dataset.
  We did this, because we were suggesting, that the similar conversational style of structure of the dataset, similar to the example ted talk 2010 dataset, is the reason why the trained model is performing much better. The more shallow and general talking is much easier to work with than the high density of fact based data of the first two models.
## First Try with Wikimedia Dataset
- First we want to focus on translation of knowledge based text.
- We want to use the Wikimedia dataset from OPUS. For more information on the dataset visit http://opus.lingfil.uu.se/LREC2012.txt. 
### Data Preprocessing
During the preprocessing of the Wikimedia dataset for training our model, we encountered various types of unwanted content that could degrade the quality of our model. To enhance the dataset's quality, we applied a series of filters to remove irrelevant or noisy data, ensuring that the training material consisted of clean and meaningful text suitable for translation tasks.

| **Issue**                                                                                                                                                 | **Resolution**                                                                                                                                                                                                                                 |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Presence of lines that are section headers or standalone keywords like "References", "External links", "See also", which do not contribute meaningful content for training.                       | Applied an exact match filter to remove any lines that exactly match a predefined list of such keywords, ignoring case sensitivity.                                                                                          |
| Lines containing links, citations, or navigational symbols such as "archived", "retrieved", "↑", "→", "http", introducing noise and irrelevant information into the dataset.                     | Implemented a contains filter to exclude any lines that contain these substrings anywhere within the text, regardless of their position, and without considering case sensitivity.                                         |
| Lines with excessive numerical data, such as multiple dates, reference numbers, or codes, which are not useful for training a translation model and could make the performance worse.             | Used regular expressions to filter out lines containing four or more occurrences of numbers with three or more digits, or any occurrence of numbers with five or more digits.                      |

## Second Try with News-Commentary Dataset
- On the second try we focus on a more cleaner set. The Wikimedia has a lot of syntax and headlines which make it hard to clean.
- See https://opus.nlpl.eu/News-Commentary/de&en/v16/News-Commentary for the dataset we used.
- First we removed rows with more than 20 words and empty lines.
- The results were hardly better than with the wikimedia dataset.
- Our thought was, that the contextual references in the dataset (similar to the wikimedia dataset) makes it difficult to get good performence in the test dataset. The context for each example must have been lerned at on point. Therefore we would require a huge dataset and a lot of training in order to get a good performence on a target.

## Third Try with Ted Talk 2020 Dataset
- With our final thoughts on the second try we decided to try a more conversational type of dataset without much contextual references and knowledge based information.
- We used the Ted Talk 2020 dataset for that.
- Our results have been much better with this set.
  - The BLEU score was 33.4.
  - And Rouge scores:
    - rouge1: 0.6543
    - rouge2: 0.4288
    - rougeL: 0.6332
  - The output of the hypothesis closely aligns with the reference upon review.

### Train a Model with mBART Architecture
Additionally we tried to train a transformer model with mBART and the Ted Talk 2020 dataset. Follow https://medium.com/@pablo_rf/fine-tuning-mbart-to-unseen-languages-c2fd55388ac5 for more information. And we also uploaded the jupiter notebook on github https://github.com/JohannesWesch/SpeechTranslation/blob/main/notebooks/ST_mBART.ipynb.
The architecture is based on the transformer architecture. In addition, a technique called denoised training is been used. Instead of directly translating a sentence, the model is trained to recover the correct version from a noisy version. This noisy version is created by introducing changes in the original sentence such as removing some blanks between tokens or changing random letters.

Our results were not as good as we hoped. After 5 epochs
- The final BLEU score  was 7.9.
- The ROUGE scores were
    - rouge1: 0.3851
    - rouge2: 0.1604
    - rougeL: 0.3541

## Challanges we stumbled upon
- Running Notebook on cluster.
- Finding a suitable dataset.
  - What criteria are crucial?
  - Cleaning the dataset in order to make it usable for our purpose.

### Contributors
Odin Göggerle, Zicheng Guo, Johannes Wesch
