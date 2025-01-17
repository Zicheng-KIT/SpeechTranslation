# Lab Report for Fourth Task

## Performance of both Speech Translation Models

These are the results of our previous trainings:

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

The BLEU scores across gender, accent, and age groups demonstrate that both the Salmonn end-to-end model and the cascaded speech translation model maintain relatively consistent performance without significant variations. This indicates that neither model shows any apparent bias against specific demographics or linguistic features, supporting their fairness and robustness in diverse scenarios.


## Attack on Input Length (Covost Dataset)

We want to test the model's ability to handle very long sentences. Ten sentences were randomly selected from the covost test set and concatenated together, and the corresponding audio files were also concatenated. Blanks were added between the audio files so that there is no overlap between the audios.

#### BLEU Score for Very Long Sentences

| Salmonn after Fine-tuning| Cascaded Model |Samples |
|--------------------------|----------------|--------|
| 3.276                    |                | 1352   |

As can be seen, the model performs very poorly on long sentences. When we look at the output of the model, a notable feature is that the length of hyp is much shorter than the length of ref. Moreover, hyp is not a summary or abbreviation of ref. It looks like the model only remembers a very small amount of information and then puts it together incorrectly. 

We also examined whether the poor performance was due to the lack of meaningful connections between the 10 sentences. However, even when using complete paragraphs from the Europarl dataset, the model continued to produce very short and unmeaningful sentences.


## Evaluating Model Robustness to Noise

Additionally, we wanted to qualitatively test how well the model handles noise.

|  Input  | Description | Output of raw Salmonn | Output of Salmonn after FT | Output of Cascaded Model |
|---------|-------------|-----------------------|----------------------------|--------------------------|
| audio-1 | Short, fuzzy vocals. | It's fun. | He says yes. ||
| audio-2 | The sound of TV in the Background. | (Correctly identified the human voice on TV.) | (Correctly identified the human voice on TV.) ||
| audio-3 | Someone says "It's ok." with the sound of TV in the Background. | He is okay. (Ignore TV sound) | He is okay.  (Ignore TV sound) ||
| audio-4 | Friction Sound. | Sorry, audio cannot be recognized. (Because there is no voice) | Someone is writing with a pen on a ruler. (The model identifies the friction sound.) ||
| audio-5 | Keyboard typing Sound. | Sorry, audio cannot be recognized. (Because there is no voice) | Typing. (Nice recognition) ||
| audio-6 | Rain Sound. | Sorry, audio cannot be recognized. (Because there is no voice) | Listen to this German speech and translate it into English. (Output the prompt) ||
| audio-7 | This is the audio we mentioned in 3rd part, the model hallucinating. | Hallucination. (Very long paragraph about Religion) | Travel well! (Try to recognize the little bit of human voice)||

It can be seen from the results that raw salmonn will give an "unrecognized" output when the human voice cannot be recognized, and hallucinations might occur when processing individual unvoiced audio. After fine-tuning, salmonn seems to have no hallucinations on the same input. Surprisingly, but inexplicably, salmonn can recognize sounds such as friction sound and typing sound after fine-tuning. We speculate that the model has a certain ability to perceive environmental sounds because of the contribution of the encoder (Whisper / BEATs).
