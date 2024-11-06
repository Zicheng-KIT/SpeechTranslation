# Lab Report for First Notebook
We organize our project on this https://github.com/JohannesWesch/SpeechTranslation github repo.    
We tried using Transformer and mBART to train a translation task from German to English on Cluster.
We tried several datasets, dividing each dataset into a training set, a test set, and a validation set with a ratio of 96:2:2. 
The datasets were also cleaned, for example using Bicleaner or applying some regular expressions.
See below for details.

## First Try with Wikimedia Dataset using plain Transformer
First we want to focus on translation of knowledge based text.
We use the Wikimedia dataset from OPUS. For more information on the dataset visit http://opus.lingfil.uu.se/LREC2012.txt. 
### Trouble: Data Preprocessing
During the preprocessing of the Wikimedia dataset for training our model, we encountered various types of unwanted content that could degrade the quality of our model. To enhance the dataset's quality, we applied a series of filters to remove irrelevant or noisy data, ensuring that the training material consisted of clean and meaningful text suitable for translation tasks.

| **Issue**                                                                                                                                                 | **Resolution**                                                                                                                                                                                                                                 |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Presence of lines that are section headers or standalone keywords like "References", "External links", "See also", which do not contribute meaningful content for training.                       | Applied an exact match filter to remove any lines that exactly match a predefined list of such keywords, ignoring case sensitivity.                                                                                          |
| Lines containing links, citations, or navigational symbols such as "archived", "retrieved", "↑", "→", "http", introducing noise and irrelevant information into the dataset.                     | Implemented a contains filter to exclude any lines that contain these substrings anywhere within the text, regardless of their position, and without considering case sensitivity.                                         |
| Lines with excessive numerical data, such as multiple dates, reference numbers, or codes, which are not useful for training a translation model and could make the performance worse.             | Used regular expressions to filter out lines containing four or more occurrences of numbers with three or more digits, or any occurrence of numbers with five or more digits.                      |

### Result
Bad performance, BLEU score 1.5 after 30 epochs.

## Second Try with News-Commentary Dataset using plain Transformer
On the second try we focus on a more cleaner set. The Wikimedia has a lot of syntax and headlines which make it hard to clean. 
- See https://opus.nlpl.eu/News-Commentary/de&en/v16/News-Commentary for the dataset we used.
- We removed rows with more than 20 words and empty lines.
- Our thought was, that the contextual references in the dataset (similar to the wikimedia dataset) makes it difficult to get good performence in the test dataset. The context for each example must have been lerned at on point. Therefore we would require a huge dataset and a lot of training in order to get a good performence on a target.
### Result
The results were hardly better than with the wikimedia dataset, BLEU score 3.x after 30 epochs.

## STOP and Think
Why were the first two results so bad?
- We were planning to use a more conversational type of dataset.
  - Because we were suggesting, that the similar conversational style of structure of the dataset, similar to the example ted talk 2010 dataset, is the reason why the trained model is performing much better. The more shallow and general talking is much easier to work with than the high density of fact based data of the first two models.
- We seek better ways to clean data. What criteria are crucial?
  - We are grateful that you suggested Bicleaner-AI.
- We were planning to use mBART.
  - Try more complex models to see if they can bring surprises.

## Third Try with Ted Talk 2020 Dataset using plain Transformer
We decided to try a more conversational type of dataset without much contextual references and knowledge based information. We used the Ted Talk 2020 dataset for that.
### Result
- Our results have been much better with this set.
  - The BLEU score was 33.4 with loss 3.318.
  - And Rouge scores:
    - rouge1: 0.6543
    - rouge2: 0.4288
    - rougeL: 0.6332
  - The output of the hypothesis closely aligns with the reference upon review.

## Fourth Try: Train a Model with mBART Architecture
Additionally we tried to train a transformer model with mBART and the Ted Talk 2020 dataset. Follow https://medium.com/@pablo_rf/fine-tuning-mbart-to-unseen-languages-c2fd55388ac5 for more information. 
The architecture is based on the transformer architecture. In addition, a technique called denoised training is been used. Instead of directly translating a sentence, the model is trained to recover the correct version from a noisy version. This noisy version is created by introducing changes in the original sentence such as removing some blanks between tokens or changing random letters.
### Trouble: Setting Hyperparameters
During training, we found that the loss was fluctuating. Even after training for a long time, there are no good results. We set a smaller learning rate and other hyperparameters, and finally we achieved good results.
### Result
There should be further improvement with continued training, but we estimate that the improvement will not be that significant.

| Epochs | Loss | BLEU |
|----|----|----|
| 20 | 5.097 | 20.0 |
| 30 | 4.755 | 22.7 |
| 40 | 4.526 | 24.6 |
| 50 | 4.358 | 26.1 |
| 60 | 4.226 | 26.5 |
| 70 | 4.177 | 27.2 |
| 80 | 4.022 | 27.6 |
| 90 | 3.939 | 27.8 |
| 100 | 3.864 | 28.1 |

## Fifth Try: News-Commentary Dataset cleaned by Bicleaner with mBART
We use Bicleaner for data cleaning and select only rows with a confidence rate greater than 0.9 as the dataset.
### Result
| Epochs | Loss | BLEU |
|----|----|----|
| 10 | 5.883 | 7.3 |

We don't have time to do more for now because the cluster is not always accessible.  
We'll try to train more epochs later.
