# Tackling systems' weaknesses

## Cascaded Model
### 1. Very Long Sentences (Fine-tuning or Update Pipeline)
First we want to try to fine-tune the ASR model on longer sentences.
Otherwise if this doesn't work out well we would fix it by using a better model as ASR model which can handle longer audio files (either Wav2Vec or Whisper).
For the translation we want to chunk the german text to translate it into English with our own machine translation model.

### 2. Noisy Input (Fine-Tuning add Preprocessing Step)
We want to add background noise to the audiofiles of the covost dataset and check the performance.
First we want to test how the performence improves when we fine-tune our ASR model on our noisy dataset.
Secondly we want to test different de-noisers with our noisy dataset and how they improve the performance on our cascaded model.

## Salmonn Model

### 3. Fix Accent Bias (Fine-tuning)
We can see that our finetuned salmon model under performs on the switzerland dialect.
#### BLEU Scores by Accent
| Accent       | Salmonn after Fine-tuning | Minimum Samples |
|--------------|---------------------------|----|
| Germany      | 31.124                    | 677 |
| Austria      | 36.686                    | 70 |
| Switzerland  | 26.189                    | 56 |

This bias we want to fix by fine-tuning on swiss data (we have approximately 3000 swiss speeches with aligned text).


### 4. Fix Out-of-domain shortcomings (In-context-learning)
We first need to attack our model with the Europarl dataset which is out-of-domain as we didn't include it in our training data.

Afterwards we want to try and fix it using in-context-learning

### Very Long Sentences
We essentially found out that SALMONN isn't supposed to handle audio sequences longer than 30s.
That's why we decided to instead focus on out-of-domain attacks.

### Noisy Input 
We already enhanced the performance of the SALMONN model with background noice on german speech by fine-tuning
on the german Covost dataset. We will also test the performance on salmonn again using the noisy input mentioned in the second point above.



