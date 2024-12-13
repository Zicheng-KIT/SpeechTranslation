# Report For Third Task

## Without Fine-Tuning SALMONN
### Results
- We observed that the model seems to habe a tendency to output religious speech if the input contains just a very short sequence of background voice besides the intended speech. In that case the model interprets the short sequence of speech in the background and generates a long transcription from it. #TODO
- 
| Filtering Criteria              | Number of Samples | BLEU Score        |
|---------------------------------|-------------------|-------------------|
| Unfiltered                      | 3001              | 18.33             |
| No Chinese                      | 2199              | 24.34             |
| No Chinese & <= 75 chars        | 1546              | 27.08             |

## Fine-Tuning SALMONN For German to English Speech Translation
- #TODO
- We had problems by trainin
- We trained for 5 epochs each took 2.50h for training and validation.
- We changed hyperparamters for
  - #TODO 
  - temperatur: 0.7 reduce the posibility of chinese and german output.
  - top_p: 0.8 reduce the posibility of chinese and german output.
  - repetition_penalty: 1.2 to reduce the probability of repeating output like "there is a a a a a".
  
- We changed the runner.py so we can train from the last epoch again.
  - We modify the 'save_chekpoint' function in order to save all parameters. 
  - We add the function 'load_checkpoint'.
  - With that we are able to reload the checkpoint.
- We had to change the parameter 'num_workers' to 0 in the config.yaml. Otherwise we had an error while restart training (while preparing training data). 
## Comparison

- After fine tuning we had improvements:
  - there is no german and chinese output anymore.
  - there is no illegal output anymore.
    - That  
### BLUE Score Comparison
| Filtering Criteria              |  Number of Samples | BLEU Score       |
|---------------------------------|-------------------|-------------------|
| Without finetuning               | 3100              | 18.33             |
| After finetuning               | 3100                | 29.46             |

### Output Comparison Examples
TODO

