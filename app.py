# Predicting a new image using our CNN model
import numpy as np
#from keras.preprocessing import image
from keras.utils import load_img, img_to_array
import tensorflow as tf
import cv2
import os
from mtcnn_cv2 import MTCNN
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import streamlit as st
from lime import lime_image



model = tf.keras.models.load_model(r"dmg_car-weights-CNN.h5")
explainer = lime_image.LimeImageExplainer()
#
def predict_image(img, model, threshold):
    # Load and preprocess the image
    img = load_img(img, target_size=model.input_shape[1:4])
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Make predictions using the model
    prediction = model.predict(img_array)[0][0]
    
    # Check if the prediction is above the threshold
    if prediction >= threshold:
        result = 'good'
    else:
        result = 'damaged'
     # Generate an explanation of the prediction using LIME
    expl = explainer.explain_instance(img_array[0], model.predict, top_labels=2, hide_color=0, num_samples=1000)
    explanation = '\n'.join([f'{round(x[1]*100, 2)}% {x[0]}' for x in expl.as_list()])

    
    
    # Return the result
    return result,explanation




#
st.title('Car Damage Predictor')
st.markdown('Upload an image of a car to see if it is damaged or not.')
st.sidebar.title('Settings')
threshold = st.sidebar.slider('Threshold', 0.0, 1.0, 0.7 , 0.5, 0.01)
def main():
  uploaded_file = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])
  if uploaded_file is not None:
        st.image(uploaded_file, caption='Input image', use_column_width=True)
        if st.button('Predict'):
            progress_bar = st.progress(0)
            result,explanation= predict_image(uploaded_file, model, threshold)
            progress_bar.progress(100)
            st.write('Prediction:', result)
            st.write('Explanation:', explanation)

if __name__ == "__main__":
    main()
