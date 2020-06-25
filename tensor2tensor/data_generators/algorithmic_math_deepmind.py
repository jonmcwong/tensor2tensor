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
import pdb
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

  # @property
  # def task_direction(self):
  #   return problem.TaskDirections.Q12
  
  @property
  def dataset_splits(self):
    if self.task_direction == problem.TaskDirections.NORMAL:
      return [{
          "split": problem.DatasetSplit.TRAIN,
          "shards": 128,
      }, {
          "split": problem.DatasetSplit.EVAL,
          "shards": 1,
      }]
    elif self.task_direction == problem.TaskDirections.EASY:
      return [{
          "split": "train_easy",
          "shards": 64,
      }]
    elif self.task_direction == problem.TaskDirections.EASY_MEDIUM:
      return [{
          "split": "train_easy_medium",
          "shards": 64,
      }]
    elif self.task_direction == problem.TaskDirections.INTERPOLATE:
      return [{
          "split": "single_inter",
          "shards": 1,
      }]
    elif self.task_direction == problem.TaskDirections.EXTRAPOLATE:
      return [{
          "split": "single_extra",
          "shards": 1,
      }]
    elif self.task_direction == problem.TaskDirections.Q8:
      return [{
      #     "split": "train_easy_add_or_sub", "shards": 1,
      # }, {
      #     "split": "train_medium_add_or_sub", "shards": 1,
      # }, {
      #     "split": "train_hard_add_or_sub", "shards": 1,
      # }, {
      #     "split": "extra_add_or_sub_big", "shards": 1,
      # }, {
      #     "split": "train_easy_mul", "shards": 1,
      # }, {
      #     "split": "train_medium_mul", "shards": 1,
      # }, {
      #     "split": "train_hard_mul", "shards": 1,
      # }, {
      #     "split": "extra_mul_big", "shards": 1,
      # }, {
          "split": "train_easy_add_sub_multiple", "shards": 1,
      }, {
          "split": "train_medium_add_sub_multiple", "shards": 1,
      }, {
          "split": "train_hard_add_sub_multiple", "shards": 1,
      }, {
          "split": "extra_add_sub_multiple_longer", "shards": 1,
      }]
    elif self.task_direction == problem.TaskDirections.Q12:
      return [{
          "split": "extra_add_or_sub_big", "shards": 1,
      }, {
          "split": "extra_add_sub_multiple_longer", "shards": 1,
      }, {
          "split": "extra_div_big", "shards": 1,
      }, {
          "split": "extra_mixed_longer", "shards": 1,
      }, {
          "split": "extra_mul_big", "shards": 1,
      }, {
          "split": "extra_mul_div_multiple_longer", "shards": 1,
      }, {
          "split": "inter_add_or_sub", "shards": 1,
      }, {
          "split": "inter_add_sub_multiple", "shards": 1,
      }, {
          "split": "inter_div", "shards": 1,
      }, {
          "split": "inter_mixed", "shards": 1,
      }, {
          "split": "inter_mul", "shards": 1,
      }, {
          "split": "inter_mul_div_multiple", "shards": 1,
      }]
    else:
      raise ValueError("Found unknown task_direction which is ", self.task_direction)




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
        return dataset_split[:5] + "polate/arithmetic__" + dataset_split[6:] + ".txt"
      elif dataset_split[:5] == "train":
        items = dataset_split.split("_")
        return  items[0] + "-" + items[1] + "/arithmetic__" + "_".join(items[2:]) + ".txt"
      else:
        raise ValueError(dataset_split)

    split_names = [p["split"] for p in self.dataset_splits]


    train_dirs = ["mathematics_dataset-v1.0/train-easy", "mathematics_dataset-v1.0/train-medium", "mathematics_dataset-v1.0/train-hard"]
    eval_dirs = ["mathematics_dataset-v1.0/interpolate", "mathematics_dataset-v1.0/extrapolate"]
    if self.task_direction == problem.TaskDirections.NORMAL:
      dirs = eval_dirs
      # Create the list of directories with data files.
      if dataset_split == problem.DatasetSplit.TRAIN:
        dirs = train_dirs
    elif self.task_direction == problem.TaskDirections.EASY:
      dirs = train_dirs[0:1]
    elif self.task_direction == problem.TaskDirections.EASY_MEDIUM:
      dirs = train_dirs[0:2]
    elif self.task_direction == problem.TaskDirections.INTERPOLATE:
      dirs = eval_dirs[0:1]
    elif self.task_direction == problem.TaskDirections.EXTRAPOLATE:
      dirs = eval_dirs[1:2]
    elif self.task_direction == problem.TaskDirections.Q12:
        dirs = ["mathematics_dataset-v1.0/" + expand_split(dataset_split)]
    elif self.task_direction == problem.TaskDirections.Q8:
        dirs = ["mathematics_dataset-v1.0/" + expand_split(dataset_split)]
    else:
      raise ValueError("Found unknown task_direction which is ", self.task_direction)

    dirs = [os.path.join(tmp_dir, d) for d in dirs]
    # pdb.set_trace()
    # Iterate over directories and files generating examples.
    for d in dirs:
      if self.task_direction == problem.TaskDirections.NORMAL:
        files = tf.gfile.Glob(d + "/*.txt")
      elif self.task_direction == problem.TaskDirections.Q12:
        files = [d]
      elif self.task_direction == problem.TaskDirections.Q8:
        files = [d]
      else:
        raise ValueError("Found unknown task_direction which is ", self.task_direction)

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
