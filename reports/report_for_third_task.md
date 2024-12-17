# Report For Third Task

## Without Fine-Tuning SALMONN
### Results
- We observed that the model seems to have a tendency to output religious speech if the input contains just a very short sequence of background voice besides the intended speech. In that case the model interprets the short sequence of speech in the background and generates a long transcription from it.
  - See the third example in the subsection Example Output.
- Also the output contained german and chinese sentences. The transcription/translation was in good quality, but not in english. 

| Filtering Criteria              | Number of Samples | BLEU Score        |
|---------------------------------|-------------------|-------------------|
| Unfiltered                      | 3001              | 18.33             |
| No Chinese                      | 2199              | 24.34             |
| No Chinese & <= 75 chars        | 1546              | 27.08             |

### Example Output
| Reference                                                 | Hypotheses                                                                                                                                                       |
|-----------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Better the sparrow in his hand than the dove on the roof. | [TO REMOVE]                                                                                                                                                      |
| It's showdown time in Gstaad.                             | It comes to a showdown. It comes to a showdown. It comes to a showdown. ..                                                                                       |
| The matter has a catch though.                            | Zechariah was the father of John the Baptist. John the Baptist was the son of Zechariah and Elizabeth. Elizabeth was .. 'continues in the same way a lot longer' |
| My favourite color is black, she said.                    | Meine Lieblingsfarbe ist schwarz, sie sagte.                                                                                                                     |
|                        | 我最喜欢的颜色是黑色，她说。 |


## Fine-Tuning SALMONN For German to English Speech Translation

- We trained for 5 epochs each took 2.50h for training and validation.
- We changed following hyperparameters:
  - temperature: 0.7
    - Control the randomness of the model's responses.
    - In our case reduce extreme random output like in the third example in the last section.
  - top_p: 0.8 
    - Control randomness by limiting the set of words from which the model can choose the next word.
    - In our case reduce the possibility of chinese and german output.
  - repetition_penalty: 1.2
    - In order to reduce the probability of repeating output like "there is a a a a a".
- We changed the runner.py so that we can resume training from the last epoch.
  - We modified the 'save_checkpoint' function in order to save all parameters. 
  - We added the function 'load_checkpoint'.
  - With these two changes we are able to reload the checkpoint.
- We had to change the parameter 'num_workers' to 0 in the config.yaml. Otherwise, we had an error while resuming training (during the preparation of training data). 

## Comparison

- After fine-tuning we had improvements:
  - there is no german and chinese output and no empty lines anymore.
  - there is no illegal output anymore.
    - For example sentences in the output which had no reference to the input data at all.

### BLUE Score Comparison

| Filtering Criteria              |  Number of Samples | BLEU Score       |
|---------------------------------|-------------------|-------------------|
| Without finetuning               | 3001              | 18.33             |
| After finetuning               | 9300                | 30.34             |

**Number of Samples** we used for calculating the BLEU Score.
