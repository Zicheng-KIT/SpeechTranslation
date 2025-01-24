# Tackling systems' weaknesses

## Cascaded Model
### Very Long Sentences
Fix by using a better model as ASR model which can handle longer audio files (either Wav2Vec or Whisper)
Then chunk the german text to translate it into English with our own machine translation model

### Noisy Input
Fix with Audio Enhancement Module


## Salmon Model
### Noisy Input 
Fix by Fine Tuning
 - Use example we have already

### Fix Accent Bias
We can see that our finetuned salmon model under performs on the switzerland dialect.
#### BLEU Scores by Accent
| Accent       | Salmonn after Fine-tuning | Minimum Samples |
|--------------|---------------------------|----|
| Germany      | 31.124                    | 677 |
| Austria      | 36.686                    | 70 |
| Switzerland  | 26.189                    | 56 |

This bias we want to fix by fine-tuning on swiss data.

### Very Long Sentences
We essentially found out that SALMONN isn't supposed to handle audio sequences longer than 30s.
That's why we decided to instead focus on out-of-domain attacks.

### Out-of-domain attack
We want to attack and fix the modal using the Europarl dataset



