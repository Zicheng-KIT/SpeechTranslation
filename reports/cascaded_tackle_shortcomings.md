  
# Noisy Input
## Performance on our Noisy Dataset
We randomly added background noise from https://www.kaggle.com/datasets/chrisfilo/demand to the audiofiles of the covost dataset.
We then added the column 'noise_type' to the covost manifest file depending on which randomly selected type of noise is included in the corresponding audio file. 
With this new dataset we now can calculate BLUE Score for each type of noise and see how it affects our model.

| Noise Type     | BLEU Score for ASR | BLUE Score for Translation |
|---------------|--------------------|--------|
| **DKITCHEN_48k**  | 5.529              |2.528   |
| **DLIVING_48k**  | 5.586              | 0.574  |
| **DWASHING_48k**  | 23.281             |4.225   |
| **NFIELD_48k**  | 13.597             |5.596   |
| **NPARK_48k**  | 9.471              |3.461   |
| **NRIVER_48k**  | 4.371              |0.511   |
| **OHALLWAY_48k**  | 14.318             |5.848   |
| **OMEETING_48k**  | 3.734              | 1.608  |
| **OOFFICE_48k**  | 16.034             |1.741   |
| **PCAFETER_48k**  | 1.994              |2.397   |
| **PRESTO_48k**  | 1.670              | 1.013  |
| **PSTATION_48k**  | 3.097              |1.633   |
| **SCAFE_48k**  | 3.650              |0.879 |
| **SPSQUARE_48k**  | 13.131             | 2.718 |
| **STRAFFIC_48k**  | 11.799             | 4.281  |
| **TBUS_48k**  | 6.367              | 2.224  |
| **TCAR_48k**  | 21.317             | 4.564  |
| **TMETRO_48k**  | 15.300             | 6.646  |

## Tackle Noise with Filter
After attacking our model with this noisy dataset we deside which categories of noise we want to tackle and which filter we are using.

# Very long Sentences
## Finetune our ASR Model
| Long Sentences Count    | Cascaded approach using original ASR Model | Cascaded approach using finetuned ASR Model|
|---------------|--------------------|--------|
| 200  | 0.01             |3.975   |
