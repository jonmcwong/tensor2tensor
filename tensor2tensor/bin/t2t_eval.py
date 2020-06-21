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

flags.DEFINE_string("dataset_split", "",
  "The split used by the desired evaluation dataset")

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

  # set appropriate dataset-split, if flags.eval_use_test_set.
  if FLAGS.dataset_split:
    # if not FLAGS.eval_use_test_set: raise ValueError(
      # "dataset_split flag was passed even though eval_use_test_set is False.")
    dataset_split = FLAGS.dataset_split
  else:
    dataset_split = "test" if FLAGS.eval_use_test_set else None
  dataset_kwargs = {"dataset_split": dataset_split}
  eval_input_fn = hparams.problem.make_estimator_input_fn(
      tf.estimator.ModeKeys.EVAL, hparams, dataset_kwargs=dataset_kwargs)
  config = t2t_trainer.create_run_config(hparams)

  # summary-hook in tf.estimator.EstimatorSpec requires
  # hparams.model_dir to be set.
  hparams.add_hparam("model_dir", config.model_dir)

  estimator = trainer_lib.create_estimator(
      FLAGS.model, hparams, config, use_tpu=FLAGS.use_tpu)
  ckpt_iter1 = trainer_lib.next_checkpoint(
      hparams.model_dir, FLAGS.eval_timeout_mins
      )
  ckpt_iter2 = my_chkpt_iter(hparams.model_dir)

  # Chose a specific set of checkpoints if dataset_split provided
  ckpt_iter = ckpt_iter1 if not FLAGS.dataset_split else ckpt_iter2
  results_all_ckpts = []
  for ckpt_path in ckpt_iter:
    results = estimator.evaluate(
        eval_input_fn, steps=FLAGS.eval_steps, checkpoint_path=ckpt_path)
    results_all_ckpts.append(results)
    tf.logging.info(results)

  # forms a line of text from each category of data
  def build_line(items, labels=False):
    items = map(str, items)
    if labels:
      return "\t".join([i.split("/")[-1] for i in items]) + "\n"
    else:
      return "\t".join(items) + "\n"

  pdb.set_trace()
  # get the category_names
  category_names = results_all_ckpts[0].keys()
  results_dir = "eval-results-" + hparams.model_dir.split("/")[-1][len(FLAGS.model)+1:]
  with open(results_dir + "/eval_" + FLAGS.dataset_split + "_results.txt", "w") as results_file:
    results_file.write(build_line(category_names, labels=True))
    for r in results_all_ckpts:
      results_file.write(build_line([r[k] for k in category_names]))
  with open(results_dir + "/checklist", "a") as checklist_file:
    checklist_file.write(FLAGS.dataset_split + "\n")

if __name__ == "__main__":
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run()
