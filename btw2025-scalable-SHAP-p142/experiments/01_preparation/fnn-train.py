#-------------------------------------------------------------
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
#-------------------------------------------------------------

#!/usr/bin/env python
# coding: utf-8

# In[63]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import shap

from joblib import dump


# In[41]:


X = pd.read_csv("../data/adult/Adult_X.csv", header=None).values
y = pd.read_csv("../data/adult/Adult_y.csv", header=None).values - 1


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=7
)


def create_model(input_size, hidden_size, output_size, drop_out):
    model = Sequential()
    model.add(Input(shape=(input_size,)))
    model.add(Dense(hidden_size, input_shape=(input_size,), activation='relu'))
    model.add(Dropout(drop_out))
    model.add(Dense(output_size, activation='sigmoid'))
    return model

#train
# Configuration
batch_size = 64
learning_rate = 0.003
epochs = 30
hidden_size = 128
drop_out = 0.35

input_size = X_train.shape[1]
output_size = 1  # Binary classification

#setup 
model = create_model(input_size, hidden_size, output_size, drop_out)
optimizer = SGD(learning_rate=learning_rate)
model.compile(optimizer=optimizer, loss='mse', metrics=['accuracy'])

# Training
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))




# In[56]:
model.evaluate(X_test, y_test)


# In[64]:
dump(model, "../data/adult/ffn.joblib")




