import keras
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
#from keras_preprocessing import image
import numpy as np
import tensorflow as tf
from keras import backend as K
#from keras import backend.tensorflow_backend as K
from tensorflow.python.keras import backend as K

# Create a new TensorFlow graph and session
g1 = tf.Graph()
sess1 = tf.compat.v1.Session(graph=g1)#tf.Session(graph=g1)

# Set the graph and session as default for TensorFlow operations
with g1.as_default():
    #keras.backend.set_session(sess1)
    K.set_session(sess1)
    #tf.global_variables_initializer().run()
    #tf.compat.v1.global_variables_initializer().run()
    sess1.run(tf.compat.v1.global_variables_initializer())
    # Load ResNet50 model inside the session context
    model = ResNet50(weights='imagenet')
    

def predict(img_path):
    img = keras.utils.load_img(img_path, target_size=(224,224))
    x = keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    with sess1.as_default():
        with sess1.graph.as_default():
            preds = model.predict(x)
            predictions = decode_predictions(preds, top=1)[0]
    return(predictions)

