# Lab Report for Fourth Task

## Performance of both Speech Translation Models

Salmonn after Fine-tuning: 30.34 BLEU score

Cascaded model (transformer(MT) + s2t_transformer(ASR)): 18.304 BLEU score

## Results of Attacks

## Bias Attack (Covost Dataset)

#### BLEU Scores by Gender
| Gender  | Salmonn after Fine-tuning | Cascaded Model | Minimum Samples |
|---------|---------------------------|----------------|---------|
| Male    | 31.257                    | 20.355         | 1014    |
| Female  | 31.702                    | 20.095         | 136     |

#### BLEU Scores by Accent
| Accent       | Salmonn after Fine-tuning | Cascaded Model | Minimum Samples |
|--------------|---------------------------|----------------|---------|
| Germany      | 31.124                    | 20.981         | 677     |
| Austria      | 36.686                    | 23.943         | 70      |
| Switzerland  | 26.189                    | 21.240         | 56      |

#### BLEU Scores by Age
| Age Group   | Salmonn after Fine-tuning | Cascaded Model | Minimum Samples |
|-------------|---------------------------|----------------|---------|
| Teens       | 29.242                    | 22.056         | 162     |
| Twenties    | 28.918                    | 18.386         | 335     |
| Thirties    | 32.542                    | 20.810         | 247     |
| Forties     | No data available         | No data available | N/A   |
| Fifties     | 33.334                    | 22.557         | 175     |
| Sixties     | 34.757                    | 19.365         | 49      |
| Seventies   | 28.753                    | 20.909         | 42      |


## Attack on Input Length (Covost Dataset)

We want to test the model's ability to handle very long sentences without out-of-domain. Ten sentences were randomly selected from the covost test set and concatenated together, and the corresponding audio files were also concatenated. Blanks were added between the audio files so that there is no overlap between the audios.

#### BLEU Score for Very Long Sentences

| Salmonn after Fine-tuning| Cascaded Model |Samples |
|--------------------------|----------------|--------|
| 3.2761658879360285       |                | 1352   |

As can be seen, the model performs very poorly on long sentences. When we look at the output of the model, a notable feature is that the length of hyp is much shorter than the length of ref. Moreover, hyp is not a summary or abbreviation of ref. It looks like the model only remembers a very small amount of information and then puts it together incorrectly. Considering that our sentences are randomly selected, we use the entire meaningful passage, but the model still gets the wrong result.


## Background Noise

