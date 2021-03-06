# -------------------------------------------------------------
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# -------------------------------------------------------------

import getopt
import os
import sys

from systemds.context import SystemDSContext
from systemds.examples.tutorials.mnist import DataManager
from systemds.matrix import Matrix
from systemds.operator.algorithm import multiLogReg, multiLogRegPredict

d = DataManager()

with SystemDSContext() as sds:
    # Train Data
    X = Matrix(sds, d.get_train_data().reshape((60000, 28*28)))
    X.write("data/mnist_features.data").compute()
    Y = Matrix(sds, d.get_train_labels().reshape((60000, 1))) + 1
    Y.to_one_hot(10).write("data/mnist_labels.data").compute()
    X_t = Matrix(sds, d.get_test_data().reshape((10000, 28*28)))
    X_t.write("data/mnist_test_features.data").compute()
    Y_t = Matrix(sds, d.get_test_labels().reshape((10000, 1))) +1
    Y_t.to_one_hot(10).write("data/mnist_test_labels.data").compute()

