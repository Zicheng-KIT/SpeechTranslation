# Report For Second Task
## Key Aspects
* dataset information 
  * Corpus: Commomvoice_de_v19.0
  * Size: train (740h) / dev (48h) / test (47h) 
* model architecture: s2t_transformer_s
* performance on testset
  * WER score of 14.8% 
  * over 90% word-level accuracy 

## Train with s2t_transformer

We use `Commomvoice_de_v19.0` as the dataset. The training set has 600,000 mp3 files, and the validation set and test set have 20,000 each. All target sentences have punctuation marks. The dataset has a small amount of noise interference and has diversity in pronunciation.

We use the s2t_transformer model provided by fairseq and follow the steps in the demonstration notebook to train.

### Result
After about 35,000 updates, the model achieved really good results：

| Epoche | Training Loss | Validation Loss | WER Score |
|--------|--------------|----------------|-----------|
|   1    |   11.022      |   9.638       |   102.07    |
|   2    |   8.941       |   8.595       |   107.75    |
|   3    |   7.799       |   6.604       |   100.90    |
|   4    |   5.594       |   4.375       |   53.24     |
|   5    |   4.335       |   3.734       |   36.60     |
|  ...  |  ...  |  ...  |  ...  |
|   26    |   2.783       |   2.765       |   15.24    |
|   27    |   2.772       |   2.762       |   15.10    |
|   28    |   2.760       |   2.753       |   14.71    |
|   29    |   2.749       |   2.752       |   14.70    |
|   **30**    |   **2.740**      |   **2.742**       |   **14.78**    |

The model performs very well on the validation set, with over 90% word-level accuracy and low perplexity (about 1.7), indicating that the model has achieved high prediction quality. A WER score of 14.8% indicates that the error between the transcript result and the reference text is relatively small, especially in real scenarios with certain noise interference or accent diversity.

### Problems encountered:
1. The dataset is too large and it is difficult to preprocess within the limited time of bwcluster. It must be processed in batches.
2. Some audio files in the dataset have background sound, such as another person speaking. For example, there is a very simple sentence "Worüber sprechen wir?", and our model predicts "In einem Pfadfinderinneninneninneninneninneninneninneninneninneninneninneninneninnen spielen sie im vierten und auf."

## Combine ASR and MT models
* For evaluation of our stacked approach we used the test training set from [covost version 2](https://github.com/facebookresearch/covost)  containing german voice clips and english transcription.
* It is based on Common Voice 4.
* The size of the test part of the dataset is 13511 lines.
* Pipeline: We first transcribed the german voice clips into german text with our s2t_transformer from the section above. Then we translated the transcription with our MT model from the first task.
* We calculated the BLEU score of 18.304 over 1000 sentences.
  
| Our Translation                     |  Reference Translation |
|------------------------------------------|--------------------------------------|
| Downy is known for his respectless humor.| Downey is known for his disrespectfully sharp humor.      |
| The point is marked by a smoke signal. | The dropping point is marked with a smoke signal.|
| Majuro is the capital of the Marshall Islands.| Majuro is the capital of Marshall Islands.|
| On stage, among the authors themselves, also Aquile Sandrock. | Besides the author himself, Adele Sandrock was also standing on the stage. |
| The European community then escaped Roy Jenkins's president of the European Commission to the summit. | The European community sent Roy Jenkins, the former president of the European Commission, to the summit. |
## Finetuing Wav2Vec2
For the finetuning we followed [this](https://huggingface.co/blog/fine-tune-wav2vec2-english) blog article.  Initially, we attempted to fine-tune the Wav2Vec2-XLS-R-1B and Wav2Vec2-XLS-R-300M models. However, both proved too large for our resources, so we opted to fine-tune the Wav2Vec2-base model, which has 90 million parameters.

The primary challenge we encountered was the `grad_norm` vanishing and eventually becoming NaN, causing the loss to drop to zero during training. While we have not pinpointed the exact cause of this issue, adjusting the batch size to 32 (using `per_device_train_batch_size`=16 and `gradient_accumulation_steps`=2) helped mitigate the problem.

We conducted the training with 50,000 samples and a learning rate of 1e-4, which yielded the following results:

| Epoche | Training Loss | Evaluation Loss | WER Score |
|--------|---------------|-----------------|-----------|
| 1      | 1.6148        | 0.9654         | 0.7512    |
| 2      | 1.4453        | 0.7582         | 0.6618    |
| 3      | 1.388         | 0.7118         | 0.6425    |
| 4      | 1.3523        | 0.7147         | 0.6316    |
| 5      | 1.4234        | 0.6897         | 0.6099    |
| 6      | 1.3275        | 0.6786         | 0.5990    |
| 7      | 1.3476        | 0.6406         | 0.5640    |
| 8      | 1.3123        | 0.6104         | 0.5592    |

Since the training approach from the notebook produced pretty good results, we decided not to fine-tune this model further. Additionally, the Wav2Vec fine-tuning model struggles with punctuation because the original model was trained on data that lacked punctuation. For the fine-tuning of Wav2Vec there are finetuned models out there (see [here](https://huggingface.co/oliverguhr/wav2vec2-base-german-cv9)), and their work indicates that significant computational resources are required. Given the tight time frame, it was challenging to accommodate additional training.

To see some examples here are couple of transcripts of our model (Our) in direct comparison to the one from [HuggingFace](https://huggingface.co/oliverguhr/wav2vec2-base-german-cv9) (HF):

| HF Transcript                              | Our Transcript                                 |
|------------------------------------------|--------------------------------------|
| war die integration erfolgreich          | war die intikration erfolgreich      |
| las uns noch paprica in den salatschnipseln | las ist noch pabrika in densalatschnitze |
| mückenstiche solte man nicht aufkratzen  | möckenstiche solte mar nicht aufkrasen |
| ist diese leitung sicher                 | ist die eleit musiche                |
| die raten verlasen dach senkende schife  | die raten verlasen ach sengendeschöfben |
