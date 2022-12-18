## Machine Learning Recommendation System

In order to run this application the following packages will need to be installed:
*

Spotipy -> pip install spotipy

Tensorflow -> pip install tensorflow

Keras -> pip install keras

fastAPI -> pip install fastapi

sklearn -> pip install scikit-learn

# Running the Application

After downloading all of the packages we will first need to build our application with:

npm start

Then we will need to open a secondary or split terminal and initialise the fastAPI server with:

uvicorn src.ml:app

- (if application does not load in chrome use npm run build and then initialise fastapi)
- * some systems may require pip3 instead of pip
