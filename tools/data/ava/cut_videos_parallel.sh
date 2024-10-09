#!/usr/bin/env bash

set -e

IN_DATA_DIR="../../../data/ava/videos"
OUT_DATA_DIR="../../../data/ava/videos_15min"

if [[ ! -d "${OUT_DATA_DIR}" ]]; then
  echo "${OUT_DATA_DIR} does not exist. Creating";
  mkdir -p ${OUT_DATA_DIR}
fi

python cut_videos_parallel.py -s ${IN_DATA_DIR} -o ${OUT_DATA_DIR}
