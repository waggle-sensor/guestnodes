# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
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
# ==============================================================================
"""Interface for data parsers.

Data parser parses input data and returns a dictionary of numpy arrays
keyed by the entries in standard_fields.py. Since the parser parses records
to numpy arrays (materialized tensors) directly, it is used to read data for
evaluation/visualization; to parse the data during training, DataDecoder should
be used.
"""
from abc import ABCMeta
from abc import abstractmethod


class DataToNumpyParser(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def parse(self, input_data):
    """Parses input and returns a numpy array or a dictionary of numpy arrays.

    Args:
      input_data: an input data

    Returns:
      A numpy array or a dictionary of numpy arrays or None, if input
      cannot be parsed.
    """
    pass
