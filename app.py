from flask import Flask, render_template, request, jsonify

from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array, to_categorical
from tensorflow import expand_dims

from sklearn.metrics import classification_report

import numpy as np
from io import BytesIO, StringIO
import os

from contextlib import redirect_stdout


app = Flask(__name__)

classes = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

(X_train, y_train), (X_test, y_test) = cifar10.load_data()


X_test = X_test.astype('float32')
X_test = X_test / 255.0

y_test = to_categorical(y_test, 10)

model = load_model("cifar10_cnn.h5")

# pred = model.predict(X_test)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]

    file_stream = BytesIO(file.read())

    # Process the image
    img = load_img(file_stream, target_size=(32,32))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = classes[np.argmax(prediction)]
    accuracy = np.max(prediction) * 100
    if accuracy > 20:
        return jsonify({
            "class": f"It is a {predicted_class}.",
            "accuracy": f"{accuracy:.2f}%"
        })
    
    else:
        return jsonify({
            "class": "I am not sure what this is.",
            "accuracy": f"{accuracy:.2f}%"
        })

@app.route("/evaluate-model", methods=["GET"])
def evaluate_model():
    pred = model.predict(X_test)
    y_pred = np.argmax(pred, axis=1)
    y_true = np.argmax(y_test, axis=1)

    # Generate classification report
    report = classification_report(y_true, y_pred)

    return jsonify({"report": report })

@app.route("/model-summary", methods=["GET"])
def model_summary():
    # Capture the model summary as a string
    summary_stream = StringIO()
    with redirect_stdout(summary_stream):
        model.summary()
    summary_string = summary_stream.getvalue()
    summary_stream.close()
    
    return jsonify({"summary": summary_string})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)