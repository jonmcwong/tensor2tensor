# coding=utf-8
# Copyright 2020 The Tensor2Tensor Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""Data generators for the DeepMind Mathematics Dataset.

See https://github.com/deepmind/mathematics_dataset for the original repository.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tarfile

from tensor2tensor.data_generators import generator_utils
from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_problems
from tensor2tensor.utils import registry
from tensor2tensor.utils import metrics


import tensorflow.compat.v1 as tf


_URL = "https://storage.cloud.google.com/mathematics-dataset/mathematics_dataset-v1.0.tar.gz"


@registry.register_problem
class AlgorithmicMathDeepmindAll(text_problems.Text2TextProblem):
  """DeepMind Mathematics Problem, v1.0, all data."""

  @property
  def vocab_type(self):
    return text_problems.VocabType.CHARACTER

  @property
  def dataset_splits(self):
    return [{
        "split": problem.DatasetSplit.TRAIN,
        "shards": 128,
    }, {
        "split": problem.DatasetSplit.EVAL,
        "shards": 1,
    }]

  @property
  def dataset_special_splits(self):
    return [{
        "split": "train_easy_add_or_sub",
        "shards": 1,
    }, {
        "split": "train_medium_add_or_sub",
        "shards": 1,
    }, {
        "split": "train_hard_add_or_sub",
        "shards": 1,
    }, {
        "split": "extra_add_or_sub",
        "shards": 1,
    }, {
        "split": "train_easy_mul",
        "shards": 1,
    }, {
        "split": "train_medium_mul",
        "shards": 1,
    }, {
        "split": "train_hard_mul",
        "shards": 1,
    }, {
        "split": "extra_mul",
        "shards": 1,
    }]

  # @property
  # def dataset_special_splits(self):
  #   return [{
  #       "split": "extra_add_or_sub_big",
  #       "shards": 1,
  #   }, {
  #       "split": "extra_add_sub_multiple_longer",
  #       "shards": 1,
  #   }, {
  #       "split": "extra_div_big",
  #       "shards": 1,
  #   }, {
  #       "split": "extra_mixed_longer",
  #       "shards": 1,
  #   }, {
  #       "split": "extra_mul_big",
  #       "shards": 1,
  #   }, {
  #       "split": "extra_mul_div_multiple_longer",
  #       "shards": 1,
  #   }, {
  #       "split": "inter_add_or_sub",
  #       "shards": 1,
  #   }, {
  #       "split": "inter_add_sub_multiple",
  #       "shards": 1,
  #   }, {
  #       "split": "inter_div",
  #       "shards": 1,
  #   }, {
  #       "split": "inter_mixed",
  #       "shards": 1,
  #   }, {
  #       "split": "inter_mul",
  #       "shards": 1,
  #   }, {
  #       "split": "inter_mul_div_multiple",
  #       "shards": 1,
  #   }]

  # What evaluation metrics to use with this problem.
  def eval_metrics(self):
    return [metrics.Metrics.ACC, metrics.Metrics.ACC_TOP5,
            metrics.Metrics.ACC_PER_SEQ]

  @property
  def is_generate_per_split(self):
    return True

  def generate_samples(self, data_dir, tmp_dir, dataset_split):
    """Downloads and extracts the dataset and generates examples.

    Args:
      data_dir: The base directory where data and vocab files are stored.
      tmp_dir: temp directory to download and extract the dataset.
      dataset_split: split of the data-set.

    Yields:
      The data examples.
    """
    # # Create directories if needed.
    # if not tf.gfile.Exists(tmp_dir):
    #   tf.gfile.MakeDirs(tmp_dir)
    # if not tf.gfile.Exists(data_dir):
    #   tf.gfile.MakeDirs(data_dir)

    # # Download and extract the data.
    # filename = os.path.basename(_URL)
    # path = generator_utils.maybe_download(tmp_dir, filename, _URL)
    # print("PATH: ", path)
    # tarfile.open(path, "r:gz").extractall(tmp_dir)

    def expand_split(dataset_split):
      if dataset_split[:5] == "inter" or dataset_split[:5] == "extra":
        return dataset_split[:5] + "polate/arithmetic__" + dataset_split[6:]
      elif dataset_split[:5] == "train"
        items = dataset_split.split("_")
        return  items[0] + "-" + items[1] + "/arithmetic__" + "_".join(items[2:])

    # Create the list of directories with data files.
    train_dirs = ["mathematics_dataset-v1.0/train-easy", "mathematics_dataset-v1.0/train-medium", "mathematics_dataset-v1.0/train-hard"]
    eval_dirs = ["mathematics_dataset-v1.0/interpolate", "mathematics_dataset-v1.0/extrapolate"]
    dirs = eval_dirs

    specific_files = False
    if dataset_split == problem.DatasetSplit.TRAIN:
      dirs = train_dirs
    elif "easy-medium" in data_dir:
      print("Found easy-medium data_dir")
      dirs = train_dirs[0:2]
    elif "easy" in data_dir:
      print("Found easy data_dir")
      dirs = train_dirs[0:1]
    elif dataset_split in [p["split"] for p in self.dataset_special_splits]:
      # this only happens if not training and specific_files
      # load file specified by dataset_split
      specific_files = True
      dirs = ["mathematics_dataset-v1.0/" + expand_split(dataset_split)]
    dirs = [os.path.join(tmp_dir, d) for d in dirs]

    # Iterate over directories and files generating examples.
    for d in dirs:
      if specific_files:
        files = tf.gfile.Glob(d + ".txt") # specific files already have the full name provided
      else:
        files = tf.gfile.Glob(d + "/*.txt")
      for fname in files:
        # In each text file, the first line is the input, the next the answer,
        # and so on until the end of the file.
        cur_input = None
        with tf.gfile.Open(fname, "rb") as f:
          for line in f:
            if cur_input is None:
              # cur_input = line.strip()
              cur_input = str(line)
            else:
              yield {"inputs": cur_input, "targets": str(line)}
              # yield {"inputs": cur_input, "targets": line.strip()}
              cur_input = None
