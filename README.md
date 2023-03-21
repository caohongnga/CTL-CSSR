# Cyclic Transfer Learning for Mandarin-English Code-Switching Speech Recognition

By Cao Hong Nga, Duc-Quang Vu, Huong Hoang Luong, Chien-Lin Huang, Jia-Ching Wang,
## Overview
We implement Cyclic Transfer Learning (CTL) on SEAME Mandarin-English Code-switching Speech Corpus. Our code is available at https://github.com/caohongnga/CTL-CSSR.

The figure below shows CTL approach.
<p align="center">
  <img width="300" alt="fig_method" src="https://github.com/caohongnga/CTL-CSSR/blob/main/CTL.png">
</p>


## Running the code
We use ESPnet, a speech processing toolkit (https://github.com/espnet/espnet) for our experiment.

You can download the model at https://drive.google.com/drive/folders/1LGcoLITArM3DeGnEnwMB913G14Vi6v_c?usp=sharing.
## The code details
In this code, you can infer your testing sets or re-run CTL method as in the submitted paper. The code includes:
- Configuration for acoustic model: conf/train_asr_transformer.yaml
- Configuration for language model: conf/train_lm_transformer.yaml
- File to run the model: asr_ctl.sh
- Bye Pair Encoding (BPE) for target model: data/cs_token_list/bpe_unigram4004/bpe.model
- Languge model file for inference: exp/lm_transformer/valid.acc.ave.pth
- Acoustic model file for inference: exp/asr_target_cycle4/valid.acc.ave.pth and exp/asr_target_cycle4/config.yaml
- The number of BPEs for the multilingual automatic speech recognition task (ML-ASR task) and the target task (CSSR) are 5000, 4004, respectively.
- We fine-tune our model by changing the number of BPE tokens of the ML-ASR task to 5503 at the iteration 3. The MER for all test set (dev_man+ dev_sge) is 17.8%, respectively. The model is at exp/asr_fine_tuning/valid.acc.ave.pth. 
### Training
- Training Language Model
The configuration for language model is at
~~~
bash ./asr_ctl.sh --stage 6 --stop_stage 8 --lm_train_text "your LM training set" --lm_dev_text "your LM validation set" --lm_test_text "your LM test set"
~~~
- Training Acoustic Model
Training IPA-CSSR at iteration 1
~~~
bash ./asr_ctl.sh --stage 9 --stop_stage 10 --train_set "your training set" --valid_set "your validation set" 
~~~
After transferring the parameters, we apply three-stage optimization as follows:
- Stage 1 (from epoch 1 to epoch 10): We freeze all the parameters received from the previous model, and fine-tune the remaining parameters (only the fully connected layers).
- Stage 2 (from epoch 11 to epoch 20): We lock the subsampling and the encoder layers, then train the other layers.
- Stage 3 (from epoch 21): We unlock all the layers and fine-tune the entire model.
Training:
~~~
bash ./train.sh 
~~~

### Inference
- Inference multiple sets
~~~
bash ./asr_ctl_target.sh --stage 11 --test_sets "<list of your test sets>"
~~~
- Inference an audio file
~~~
>>> import soundfile
>>> speech2text = Speech2Text("<asr_config.yml>", "<asr.pth>")  #speech2text = Speech2Text("asr_target_cycle4/config.yaml, "asr_target_cycle4/valid.acc.ave.pth")
>>> audio, rate = soundfile.read("speech.wav")
>>> speech2text(audio)
        --> [(text, token, token_int, hypothesis object), ...]
~~~

### Dataset
We use SEAME Mandarin-English Code-switching Speech Corpus for the Task 1 (IPA-CSSR) and the target task (CSSR). The corpus is available at https://catalog.ldc.upenn.edu/LDC2015S04.

For multilingual pre-training, we utilize the TEDLIUM-2 English speech recognition corpus (https://www.openslr.org/19/) and the AISHELL-1 Mandarin Speech Corpus (https://www.openslr.org/33/).

For language model training, we use SEAME and part IV of the National Speech Corpus (NSC) (https://www.imda.gov.sg/programme-listing/digital-services-lab/national-speech-corpus)






