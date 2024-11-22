## Train from Scratch

## Combine ASR and MT models

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

Since the training approach from the notebook produced fairly good results, we decided not to fine-tune this model further. Others have already explored this extensively (see [here](https://huggingface.co/oliverguhr/wav2vec2-base-german-cv9)), and their work indicates that significant computational resources are required. Given the tight time frame, it was challenging to accommodate additional training.

To see some examples here are couple of transcripts of our model (Our) in direct comparison to the one from [HuggingFace](https://huggingface.co/oliverguhr/wav2vec2-base-german-cv9) (HF):

| HF Transcript                              | Our Transcript                                 |
|------------------------------------------|--------------------------------------|
| war die integration erfolgreich          | war die intikration erfolgreich      |
| las uns noch paprica in den salatschnipseln | las ist noch pabrika in densalatschnitze |
| mückenstiche solte man nicht aufkratzen  | möckenstiche solte mar nicht aufkrasen |
| ist diese leitung sicher                 | ist die eleit musiche                |
| die raten verlasen dach senkende schife  | die raten verlasen ach sengendeschöfben |