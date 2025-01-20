# Lab Report for Fourth Task

## Performance of both Speech Translation Models

These are the results of our previous trainings:

Salmonn after Fine-tuning: 30.34 BLEU score

Cascaded model (transformer(MT) + s2t_transformer(ASR)): 18.304 BLEU score

## Overview over Attacks and Results
All our attacks we did on both of our models likewise.

First we did a bias attack. We used the covost dataset for that, which we also trained and finetuned our models in the previous tasks. We used the available metrics like age, gender and accent, and calculated the corresponding BLEU Scores. Both models performed well for all the different metrics.

In our second attack we increased the sentence length by appending several sentences of the covost dataset together and build a new test dataset out of them. Both models performed very badly. For both models, the hypotheses is much shorted (regular sentence length) than the reference. The cascaded model shows repetitive output unrelated to the input data while the finetuned salmon only remembers very little of the input information and therefore the output sometimes seems to be related with the input but still makes no sense.

For the third attack we can provide only some test cases. We wanted to test how robust our models are to different types of noise. The finetuned Salmon has the ability to cope with the noise and even recognize the type of noise. So we already can see that our finetuned LLM has improved compared to the prior version regarding noisy input data. The cascaded model is very disturbed in all of the test cases. It always tries to interpret noise as spoken language and gives hallucinated output.

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

### BLEU Score for Very Long Sentences

| Salmonn after Fine-tuning| Cascaded Model |Samples |
|--------------------------|----------------|--------|
| 3.276                    |       0.0105   | 1352   |

#### Salmonn after Fine-tuning

As can be seen, the model performs very poorly on long sentences. When we look at the output of the model, a notable feature is that the length of hyp is much shorter than the length of ref. Moreover, hyp is not a summary or abbreviation of ref. It looks like the model only remembers a very small amount of information and then puts it together incorrectly. 

We also examined whether the poor performance was due to the lack of meaningful connections between the 10 sentences. However, even when using complete paragraphs from the Europarl dataset, the model continued to produce very short and unmeaningful sentences.

#### Cascaded Model

The cascaded model is performing even worse. The output is very repetitive and unrelated to the input data.

## Evaluating Model Robustness to Noise

Additionally, we wanted to qualitatively test how well the model handles noise.

|  Input  | Description | Output of raw Salmonn | Output of Salmonn after FT | Output of Cascaded Model |
|---------|-------------|-----------------------|----------------------------|--------------------------|
| audio-1 | Short, fuzzy vocals. | It's fun. | He says yes. |Welch pregnant.|
| audio-2 | The sound of TV in the Background. | (Part of the human voice was recognized.) | (Some nonsense words.) |(Part of the human voice was recognized.)|
| audio-3 | Someone says "It's ok." with the sound of TV in the Background. | He is okay. (Ignore TV sound) | He is okay.  (Ignore TV sound) |It's almost entirely interesting that you're there, especially partly, you can actually buy to a special or common parallel ^-Jeopardy Cyncensich. (The output is disturbed by noise and special characters are output.)|
| audio-4 | Friction Sound. | Sorry, audio cannot be recognized. (Because there is no voice) | Someone is writing with a pen on a ruler. (The model identifies the friction sound.) |The Foundation Foundation Foundation Foundation Foundation Foundation Foundations Institutes and studied at the University of Frankfurt. (Recognize the sound as human voice and the output is very repetitive)|
| audio-5 | Keyboard typing Sound. | Sorry, audio cannot be recognized. (Because there is no voice) | Typing. (Nice recognition) |The debate is a problem of developing countries. (Recognize the sound as human voice)|
| audio-6 | Rain Sound. | Sorry, audio cannot be recognized. (Because there is no voice) | Listen to this German speech and translate it into English. (Output the prompt) |He was taken off, and he was also working as a real estate adhesive. (Recognize the sound as human voice)|
| audio-7 | This is the audio we mentioned in 3rd part, the salmon model hallucinating. | Hallucination. (Very long paragraph about Religion) | Travel well! (Try to recognize the little bit of human voice but we cannot judge the correctness)|That's a good exercise.(Try to recognize the little bit of human voice but we cannot judge the correctness)|

It can be seen from the results that raw salmonn will give an "unrecognized" output when the human voice cannot be recognized, and hallucinations might occur when processing individual unvoiced audio. After fine-tuning, salmonn seems to have no hallucinations on the same input. Surprisingly, but inexplicably, salmonn can recognize sounds such as friction sound and typing sound after fine-tuning. We speculate that the model has a certain ability to perceive environmental sounds because of the contribution of the encoder (Whisper / BEATs). In stark contrast, the cascated model is almost always affected by noise.
