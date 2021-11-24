Using TensorFlow backend.
Loading data... 
The train data size is that 
(20258, 19, 341)
(20258, 341)
X_train, y_train,shape
(20258, 19, 341)
(20258, 341)

Data Loaded. Compiling...

train.py:51: UserWarning: The `input_dim` and `input_length` arguments in recurrent layers are deprecated. Use `input_shape` instead.
  return_sequences=True))
train.py:51: UserWarning: Update your `LSTM` call to the Keras 2 API: `LSTM(units=64, return_sequences=True, input_shape=(19, 341))`
  return_sequences=True))
W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE3 instructions, but these are available on your machine and could speed up CPU computations.
W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.1 instructions, but these are available on your machine and could speed up CPU computations.
W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.2 instructions, but these are available on your machine and could speed up CPU computations.
W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX instructions, but these are available on your machine and could speed up CPU computations.
W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX2 instructions, but these are available on your machine and could speed up CPU computations.
W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use AVX512F instructions, but these are available on your machine and could speed up CPU computations.
W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use FMA instructions, but these are available on your machine and could speed up CPU computations.
train.py:65: UserWarning: Update your `Dense` call to the Keras 2 API: `Dense(units=341, activation="softmax")`
  output_dim=layers['output'],activation='softmax'))
Compilation Time :  0.0114541053772
Training...
Train on 19245 samples, validate on 1013 samples
Epoch 1/10
19245/19245 [==============================] - 27s - loss: 2.2438 - acc: 0.4062 - val_loss: 3.9367 - val_acc: 0.1066
Epoch 2/10
19245/19245 [==============================] - 28s - loss: 1.7689 - acc: 0.4896 - val_loss: 3.7269 - val_acc: 0.0030
Epoch 3/10
19245/19245 [==============================] - 29s - loss: 1.6343 - acc: 0.5166 - val_loss: 3.9401 - val_acc: 0.0039
Epoch 4/10
19245/19245 [==============================] - 30s - loss: 1.5131 - acc: 0.5497 - val_loss: 4.1313 - val_acc: 0.0020
Epoch 5/10
19245/19245 [==============================] - 27s - loss: 1.4119 - acc: 0.5795 - val_loss: 4.7000 - val_acc: 0.0888
Epoch 6/10
19245/19245 [==============================] - 24s - loss: 1.3081 - acc: 0.6159 - val_loss: 3.9640 - val_acc: 0.0977
Epoch 7/10
19245/19245 [==============================] - 25s - loss: 1.2367 - acc: 0.6314 - val_loss: 4.0659 - val_acc: 0.0967
Epoch 8/10
19245/19245 [==============================] - 24s - loss: 1.1850 - acc: 0.6422 - val_loss: 4.0118 - val_acc: 0.1915
Epoch 9/10
19245/19245 [==============================] - 25s - loss: 1.1345 - acc: 0.6566 - val_loss: 4.2684 - val_acc: 0.1017
Epoch 10/10
19245/19245 [==============================] - 25s - loss: 1.0869 - acc: 0.6676 - val_loss: 4.1716 - val_acc: 0.1816
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
lstm_1 (LSTM)                (None, 19, 64)            103936    
_________________________________________________________________
dropout_1 (Dropout)          (None, 19, 64)            0         
_________________________________________________________________
lstm_2 (LSTM)                (None, 19, 256)           328704    
_________________________________________________________________
dropout_2 (Dropout)          (None, 19, 256)           0         
_________________________________________________________________
lstm_3 (LSTM)                (None, 100)               142800    
_________________________________________________________________
dropout_3 (Dropout)          (None, 100)               0         
_________________________________________________________________
dense_1 (Dense)              (None, 341)               34441     
=================================================================
Total params: 609,881.0
Trainable params: 609,881.0
Non-trainable params: 0.0
_________________________________________________________________
Done Training...