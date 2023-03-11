import tensorflow as tf


mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis = 1)
x_test = tf.keras.utils.normalize(x_test, axis = 1)

# Uncomment if creating a new model
model = tf.keras.models.Sequential() 
model.add(tf.keras.layers.Flatten(input_shape= (28,28)))
model.add(tf.keras.layers.Dense(128, activation= 'relu'))
model.add(tf.keras.layers.Dense(128, activation= 'relu'))
model.add(tf.keras.layers.Dense(10, activation= 'softmax'))

model.compile(optimizer= 'adam', loss= 'sparse_categorical_crossentropy', metrics= ['accuracy'])

model.fit(x_train, y_train, epochs= 8)

model.save('App/recog_model')


model = tf.keras.models.load_model('App/recog_model')

loss, accuracy = model.evaluate(x_test, y_test)

print(loss)
print(accuracy)