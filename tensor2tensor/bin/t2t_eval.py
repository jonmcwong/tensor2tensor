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
flags.DEFINE_string("results_dir", "", "Where to write results")
flags.DEFINE_string("which_checkpoints", "all", "all, last or NUM")
print(FLAGS.results_dir)
FLAGS.task_direction = FLAGS.task_direction.upper()
# pdb.set_trace()

def chkpt_condition(f, contents):
  if FLAGS.which_checkpoints == "all":
    return True
  elif FLAGS.which_checkpoints == "last":
    return f.split("-")[:-1] == contents.split("\n")[0].split("-")[:-1]
  elif FLAGS.which_checkpoints.isnumeric():
    return FLAGS.which_checkpoints == f.split("-")[:-1]
  else:
    raise ValueError("which_checkpoints must be 'all', 'last' or a number. It is currently", FLAGS.which_checkpoints)

def my_chkpt_iter(model_dir):
  with file_io.FileIO(os.path.join(model_dir, "checkpoint"), "r") as ckpt_file:
    contents = ckpt_file.read()
  specific_checkpoints = [
    f.split(" ")[1][1:-1]
    for f in contents.split("\n")
    if f.startswith('all_model_checkpoint_paths: "') and
      chkpt_condition(f, contents)
  ]
  for ckpt in specific_checkpoints:
    yield os.path.join(model_dir, ckpt)
  # return specific_checkpoints

def main(_):
  if FLAGS.results_dir:
    print("\n\n\n\n\nresults_dir = {}\n\n\n\n\n".format(FLAGS.results_dir))
    print(FLAGS.results_dir and FLAGS.results_dir[:5] == "gs://")
  tf.logging.set_verbosity(tf.logging.INFO)
  trainer_lib.set_random_seed(FLAGS.random_seed)
  usr_dir.import_usr_dir(FLAGS.t2t_usr_dir)

  hparams = trainer_lib.create_hparams(
      FLAGS.hparams_set, FLAGS.hparams, data_dir=FLAGS.data_dir,
      problem_name=FLAGS.problem)

  if FLAGS.task_direction == problem.TaskDirections.NORMAL:
    dataset_split = "test" if FLAGS.eval_use_test_set else None
  elif FLAGS.task_direction == problem.TaskDirections.Q12:
    dataset_split = FLAGS.dataset_split
  elif FLAGS.task_direction == problem.TaskDirections.Q8:
    dataset_split = FLAGS.dataset_split
  elif FLAGS.task_direction == problem.TaskDirections.INTERPOLATE:
    dataset_split = FLAGS.dataset_split
  elif FLAGS.task_direction == problem.TaskDirections.EXTRAPOLATE:
    dataset_split = FLAGS.dataset_split
  else:
    raise ValueError("Found unknown task_direction which is ", FLAGS.task_direction)
  # pdb.set_trace()
  dataset_kwargs = {"dataset_split": dataset_split}
  eval_input_fn = hparams.problem.make_estimator_input_fn(
      tf.estimator.ModeKeys.EVAL, hparams, dataset_kwargs=dataset_kwargs)
  config = t2t_trainer.create_run_config(hparams)

  # summary-hook in tf.estimator.EstimatorSpec requires
  # hparams.model_dir to be set.
  hparams.add_hparam("model_dir", config.model_dir)

  estimator = trainer_lib.create_estimator(
      FLAGS.model, hparams, config, use_tpu=FLAGS.use_tpu)


  if FLAGS.task_direction == problem.TaskDirections.NORMAL:
    ckpt_iter = trainer_lib.next_checkpoint(
      hparams.model_dir, FLAGS.eval_timeout_mins
      )
  elif FLAGS.task_direction == problem.TaskDirections.Q12:
    ckpt_iter = my_chkpt_iter(hparams.model_dir)
  elif FLAGS.task_direction == problem.TaskDirections.Q8:
    ckpt_iter = my_chkpt_iter(hparams.model_dir)
  elif FLAGS.task_direction == problem.TaskDirections.INTERPOLATE:
    ckpt_iter = my_chkpt_iter(hparams.model_dir)
  elif FLAGS.task_direction == problem.TaskDirections.EXTRAPOLATE:
    ckpt_iter = my_chkpt_iter(hparams.model_dir)
  else:
    raise ValueError("Found unknown task_direction which is ", FLAGS.task_direction)


  # Chose a specific set of checkpoints if dataset_split provided
  if FLAGS.results_dir:
    results_dir = FLAGS.results_dir
  else:
    raise ValueError("results_dir not defined")
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

  # pdb.set_trace()
  
  # get the category_names
  category_names = results_all_ckpts[0].keys()
  # Write to bucket
  with file_io.FileIO(
    results_dir + "/eval_" + FLAGS.dataset_split + "_results.txt", "w"
  ) as results_file:
    results_file.write(build_line(category_names, labels=True))
    for r in results_all_ckpts:
      results_file.write(build_line([r[k] for k in category_names]))
  with file_io.FileIO(results_dir + "/checklist", "w") as checklist_file:
    checklist_file.write(FLAGS.dataset_split + "\n")


if __name__ == "__main__":
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run()
