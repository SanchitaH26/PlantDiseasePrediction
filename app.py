from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow import keras
import numpy as np
from PIL import Image
import io
import re
from plant_disease_nlp import diagnose_disease, format_diagnosis
app = Flask(__name__)
CORS(app)
print("Loading model...")
model = keras.models.load_model('plant_disease_model.h5')
print("Model loaded successfully!")
CLASS_NAMES = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 
    'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]
IMG_SIZE=128
def preprocess_image(image):
    image = image.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(image)
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array
@app.route('/')
def home():
    return jsonify({
        "message": "Plant Disease Detection API",
        "endpoints": {
            "/predict-image": "POST - Upload image for disease detection",
            "/predict-text": "POST - Text-based symptom analysis"
        }
    })

@app.route('/predict-image',methods=['POST'])
def predict_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
        file=request.files['image']
        
        if file.filename=='':
            return jsonify({"error": "No image selected"}), 400
        image=Image.open(io.BytesIO(file.read()))
        if image.mode!='RGB':
            image=image.convert('RGB')
        processed_image=preprocess_image(image)
        predictions=model.predict(processed_image, verbose=0)
        predicted_class_idx=np.argmax(predictions[0])
        confidence=float(predictions[0][predicted_class_idx] * 100)
        predicted_class=CLASS_NAMES[predicted_class_idx]
        is_healthy='healthy' in predicted_class.lower()
        top_3_idx=np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions=[
            (CLASS_NAMES[i].replace('_', ' '), float(predictions[0][i] * 100))
            for i in top_3_idx
        ]
        disease_name=predicted_class.replace('_', ' ').title()
        response={
            "status":"HEALTHY" if is_healthy else "DISEASED",
            "disease":disease_name if not is_healthy else "No disease detected",
            "confidence":confidence,
            "predicted_class":predicted_class,
            "top_3_predictions":top_3_predictions
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict-text', methods=['POST'])
def predict_text():
    try:
        data = request.get_json()
        if not data or 'symptoms' not in data:
            return jsonify({"error": "No symptoms provided"}), 400
        symptoms = data['symptoms']
        if not symptoms.strip():
            return jsonify({"error": "Symptoms cannot be empty"}), 400
        diagnosis = diagnose_disease(symptoms)
        response = {
            "diagnosis": diagnosis,
            "formatted_output": format_diagnosis(diagnosis)
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })
if __name__ == '__main__':
    print("Plant Disease Detection API")
    print("Server starting on http://localhost:5000")
    print("Endpoints available:")
    print("  - POST /predict-image : Upload image for detection")
    print("  - POST /predict-text  : Text-based symptom analysis")
    app.run(debug=True, port=5000)