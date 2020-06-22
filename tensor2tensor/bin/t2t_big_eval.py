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

r"""Perform evaluation on trained T2T models using the Estimator API."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensor2tensor.bin import t2t_trainer          # pylint: disable=unused-import
from tensor2tensor.data_generators import problem  # pylint: disable=unused-import
from tensor2tensor.utils import trainer_lib
from tensor2tensor.utils import usr_dir
import tensorflow.compat.v1 as tf
from tensorflow.python.lib.io import file_io

import os
import pdb

flags = tf.flags
FLAGS = flags.FLAGS

flags.DEFINE_string("results_dir", "",
  "Where to write results")

def my_chkpt_iter(model_dir):
  with file_io.FileIO(os.path.join(model_dir, "checkpoint"), "r") as ckpt_file:
    contents = ckpt_file.read()
  specific_checkpoints = [
    f.split(" ")[1][1:-1]
    for f in contents.split("\n")
    if f.startswith('all_model_checkpoint_paths: "') and
      f.split("-")[-1][:-1] != "0"
  ]
  for ckpt in specific_checkpoints:
    yield os.path.join(model_dir, ckpt)
  # return specific_checkpoints

def main(_):
  tf.logging.set_verbosity(tf.logging.INFO)
  trainer_lib.set_random_seed(FLAGS.random_seed)
  usr_dir.import_usr_dir(FLAGS.t2t_usr_dir)

  hparams = trainer_lib.create_hparams(
      FLAGS.hparams_set, FLAGS.hparams, data_dir=FLAGS.data_dir,
      problem_name=FLAGS.problem)


  # Get the datasets needed
  many_datset_splits = [
    "extra_add_or_sub_big",
    "extra_add_sub_multiple_longer",
    "extra_div_big",
    "extra_mixed_longer",
    "extra_mul_big",
    "extra_mul_div_multiple_longer",
    "inter_add_or_sub",
    "inter_add_sub_multiple",
    "inter_div",
    "inter_mixed",
    "inter_mul",
    "inter_mul_div_multiple"
  ]
  many_dataset_kwargs = [{"dataset_split": ds} for ds in many_datset_splits]



  # make the function that returns data
  many_eval_input_fns = [hparams.problem.make_estimator_input_fn(
      tf.estimator.ModeKeys.EVAL, hparams, dataset_kwargs=dk)
      for dk in many_dataset_kwargs]








  config = t2t_trainer.create_run_config(hparams)

  # summary-hook in tf.estimator.EstimatorSpec requires
  # hparams.model_dir to be set.
  hparams.add_hparam("model_dir", config.model_dir)

  # set up "something" which will restore the
  # checkpoints and test against the datasets
  estimator = trainer_lib.create_estimator(
      FLAGS.model, hparams, config, use_tpu=FLAGS.use_tpu)

  ckpt_iter = my_chkpt_iter(hparams.model_dir)

  # run against the datasets for each checkpoint
  results_all_ckpts = []
  for ckpt_path in ckpt_iter:
    # run the model from the given ckpt using the input_fn to give data
    results = estimator.evaluate(
        many_eval_input_fns[0], steps=FLAGS.eval_steps, checkpoint_path=ckpt_path)
    results_all_ckpts.append(results)
    tf.logging.info(results)

  # forms a line of text from each category of data
  def build_line(items, labels=False):
    items = map(str, items)
    if labels:
      return "\t".join([i.split("/")[-1] for i in items]) + "\n"
    else:
      return "\t".join(items) + "\n"

  # pdb.set_trace()
  # write all the data
  # get the category_names
  category_names = results_all_ckpts[0].keys()
  results_dir = FLAGS.results_dir
  results_dir += "/eval-results-" + hparams.model_dir.split("/")[-1][len(FLAGS.model)+1:]
  with open(results_dir + "/eval_" + FLAGS.dataset_split + "_results.txt", "w") as results_file:
    results_file.write(build_line(category_names, labels=True))
    for r in results_all_ckpts:
      results_file.write(build_line([r[k] for k in category_names]))
  with open(results_dir + "/checklist", "a") as checklist_file:
    checklist_file.write(FLAGS.dataset_split + "\n")

if __name__ == "__main__":
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run()
