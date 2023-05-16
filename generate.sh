#!/bin/bash

DATABIN=data-bin
CKPTS=checkpoints

LANGUAGE=$1
TYPE=$2

CHECKPOINT_DIR="${CKPTS}/${LANGUAGE}-models"
PRED="${CKPTS}/${LANGUAGE}-predictions/test"

mkdir -p "${CKPTS}/${LANGUAGE}-predictions"

if [[ "${TYPE}" == "dev" ]]; then
    TYPE=valid
    PRED="${CKPTS}/${LANGUAGE}-predictions/dev"
fi

MODEL="checkpoint_best.pt"
echo "... generating with model ${MODEL} ..."

fairseq-generate \
    "${DATABIN}/${LANGUAGE}" \
    --gen-subset "${TYPE}" \
    --source-lang "${LANGUAGE}.input" \
    --target-lang "${LANGUAGE}.output" \
    --path "${CHECKPOINT_DIR}/${MODEL}" \
    --beam 1 \
    > "${PRED}-${MODEL}.txt"


# Reformat the predictions to the shared task data format

if [[ "${TYPE}" == "valid" ]]; then
    TYPE=dev
fi
