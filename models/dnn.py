import tensorflow as tf
import tensorflow.keras as keras

import data.data as data

def create_model(train_data, train_target, val_data, val_target, params):
    num_output_classes = data.Dataset.config.num_classes
    input_shape = train_data[0].shape

    model = keras.Sequential()

    model.add(keras.layers.InputLayer(input_shape=input_shape, name='input'))
    model.add(keras.layers.BatchNormalization())

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(params['size_first_layer'], activation='relu'))
    if params['has_batch_norm']:
        model.add(keras.layers.BatchNormalization())
    if params['size_second_layer'] > 0:
        model.add(keras.layers.Dense(params['size_second_layer'], activation='relu'))
    model.add(keras.layers.Dropout(params['dropout']))
    model.add(keras.layers.Dense(num_output_classes, activation='softmax'))

    # Create the checkpoint callback
    checkpoint_filepath = 'tmp/checkpoint'
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=True,
        monitor='val_accuracy',
        mode='max',
        save_best_only=True)

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics='accuracy')
    history = model.fit(train_data, train_target, validation_data=(val_data, val_target), epochs=params['num_epochs'],
                        batch_size=params['batch_size'], callbacks=[checkpoint_callback])

    # Load the best performing checkpoint into the model
    model.load_weights(checkpoint_filepath)

    return history, model
