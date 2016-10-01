import keras
from keras.layers import Dropout, LSTM, Dense, Activation
from keras.models import Sequential
from keras.regularizers import l2
from commons import *


__author__ = 'Sogo'
__version__ = '0.5'
# Attributes: id, time, user, serial, value, ip, type, user2
# Types: D, L, V, C, T, H / user1 + user2

if __name__ == "__main__":
    print("Operating regression_test.py file.")

    number_of_time_stamps = 50
    # Set general LSTM Data from keras
    data = get_data_list_on_folder(folder='./ips/sk-jung-gu', complete_set=False)
    (X_train, y_train), (X_test, y_test) = train_test_split(data, fold_size=0.1, time_steps=number_of_time_stamps)

    """
        model.output_shape == (None, 32)
        - Input shape   : 3D tensor (nb_samples, timesteps, input_dim)
        - Output shape  : return_sequences 2D tensor is (nb_samples, output_dim)
        - Note: https://keras.io/layers/recurrent/
    """
    in_out_neurons = 6
    hidden_neurons = 64
    batch_size = 32
    in_shape = X_train.shape    # (# of samples, timesteps, output_dim)
    in_shape = (batch_size, in_shape[1], in_shape[2]) # (batch_size, timesteps, output_dim)

    model_lstm = Sequential()

    model_lstm.add(LSTM(output_dim=hidden_neurons, batch_input_shape=in_shape, return_sequences=False))
    model_lstm.add(Dropout(0.1))
    # model_lstm.add(Dense(hidden_neurons, W_regularizer=l2(0.06)))
    model_lstm.add(Dense(input_dim=hidden_neurons, output_dim=in_out_neurons)) # None batches means any size of batch is able to process.
    model_lstm.add(Activation("softmax"))
    model_lstm.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=['accuracy']) # sparse_categorical_crossentropy(https://keras.io/objectives/), metrics=['accuracy']
    model_lstm.fit(X_train, y_train, batch_size=batch_size, nb_epoch=3, verbose=2, validation_split=0.05)

    predicted = model_lstm.predict(X_test)
    print(np.sqrt((predicted - y_test) ** 2).mean(axis=0)).mean() # Printing RMSE

else:
    print("Operaing 'main' from other file. (This is regression_test.py)")