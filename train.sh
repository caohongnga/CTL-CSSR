#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail


bash ./asr_ctl.sh --stage 10 --stop_stage 10 --asr_args "--max_epoch 10 --freeze_param encoder decoder.decoders"

bash ./asr_ctl.sh --stage 10 --stop_stage 10 --asr_args "--max_epoch 20 --freeze_param encoder"

bash ./asr_ctl.sh --stage 10 --asr_args "--max_epoch 80"
