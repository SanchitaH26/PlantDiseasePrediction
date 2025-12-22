from flask import Flask, request, jsonify, session, redirect, send_from_directory
from flask_cors import CORS
from tensorflow import keras
from pymongo import MongoClient
import numpy as np
from PIL import Image
import io
import hashlib
import re
import speech_recognition as sr
import tempfile
import os
from pydub import AudioSegment
from plant_disease_nlp import diagnose_disease, format_diagnosis

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = "super-secret-key-change-this"
CORS(app, supports_credentials=True)

client = MongoClient("mongodb://localhost:27017/")
db = client["agribot_db"]
users = db["users"]
diseases_collection = db["diseases"]

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

IMG_SIZE = 128

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def preprocess_image(image):
    image = image.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(image)
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def initialize_diseases():
    if diseases_collection.count_documents({}) == 0:
        print("Initializing diseases database...")
        for class_name in CLASS_NAMES:
            parts = class_name.split('___')
            plant = parts[0].replace('_', ' ')
            disease = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
            
            is_healthy = 'healthy' in disease.lower()
            
            disease_doc = {
                "class_name": class_name,
                "plant": plant,
                "disease_name": disease,
                "is_healthy": is_healthy,
                "symptoms": f"Common symptoms of {disease} in {plant}",
                "cause": f"Typical causes of {disease}",
                "treatment": f"Standard treatment for {disease}",
                "prevention": f"Prevention methods for {disease}",
                "severity": "Medium" if not is_healthy else "None"
            }
            diseases_collection.insert_one(disease_doc)
        print(f"Initialized {len(CLASS_NAMES)} diseases in database")

initialize_diseases()

@app.route("/login.html")
def serve_login():
    return send_from_directory(".", "login.html")

@app.route("/index.html")
def serve_index():
    if "user" not in session:
        return redirect("/login.html")
    if session.get("role") == "admin":
        return redirect("/admin_dashboard.html")
    return send_from_directory(".", "index.html")

@app.route("/admin_dashboard.html")
def serve_admin():
    if "user" not in session or session.get("role") != "admin":
        return redirect("/login.html")
    return send_from_directory(".", "admin_dashboard.html")

@app.route("/")
def root():
    return send_from_directory(".", "login.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if users.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    users.insert_one({
        "username": username,
        "password": hash_password(password),
        "role": role
    })

    return jsonify({"message": "Registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    user = users.find_one({
        "username": username,
        "password": hash_password(password),
        "role": role
    })

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    session["user"] = username
    session["role"] = role

    return jsonify({"message": "Login successful", "role": role})

@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

@app.route("/check-auth")
def check_auth():
    if "user" in session:
        return jsonify({"authenticated": True, "role": session.get("role")})
    return jsonify({"authenticated": False}), 401

@app.route("/admin/diseases", methods=["GET"])
def get_all_diseases():
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    
    diseases = list(diseases_collection.find({}, {"_id": 0}))
    return jsonify({"diseases": diseases, "total": len(diseases)})

@app.route("/admin/diseases/<class_name>", methods=["GET"])
def get_disease(class_name):
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    
    disease = diseases_collection.find_one({"class_name": class_name}, {"_id": 0})
    if not disease:
        return jsonify({"error": "Disease not found"}), 404
    
    return jsonify(disease)

@app.route("/admin/diseases", methods=["POST"])
def add_disease():
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.json
    
    if diseases_collection.find_one({"class_name": data.get("class_name")}):
        return jsonify({"error": "Disease already exists"}), 400
    
    disease_doc = {
        "class_name": data.get("class_name"),
        "plant": data.get("plant"),
        "disease_name": data.get("disease_name"),
        "is_healthy": data.get("is_healthy", False),
        "symptoms": data.get("symptoms", ""),
        "cause": data.get("cause", ""),
        "treatment": data.get("treatment", ""),
        "prevention": data.get("prevention", ""),
        "severity": data.get("severity", "Medium")
    }
    
    diseases_collection.insert_one(disease_doc)
    return jsonify({"message": "Disease added successfully"})

@app.route("/admin/diseases/<class_name>", methods=["PUT"])
def update_disease(class_name):
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.json
    
    update_data = {}
    if "plant" in data:
        update_data["plant"] = data["plant"]
    if "disease_name" in data:
        update_data["disease_name"] = data["disease_name"]
    if "is_healthy" in data:
        update_data["is_healthy"] = data["is_healthy"]
    if "symptoms" in data:
        update_data["symptoms"] = data["symptoms"]
    if "cause" in data:
        update_data["cause"] = data["cause"]
    if "treatment" in data:
        update_data["treatment"] = data["treatment"]
    if "prevention" in data:
        update_data["prevention"] = data["prevention"]
    if "severity" in data:
        update_data["severity"] = data["severity"]
    
    result = diseases_collection.update_one(
        {"class_name": class_name},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        return jsonify({"error": "Disease not found"}), 404
    
    return jsonify({"message": "Disease updated successfully"})

@app.route("/admin/diseases/<class_name>", methods=["DELETE"])
def delete_disease(class_name):
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    
    result = diseases_collection.delete_one({"class_name": class_name})
    
    if result.deleted_count == 0:
        return jsonify({"error": "Disease not found"}), 404
    
    return jsonify({"message": "Disease deleted successfully"})

@app.route("/admin/stats", methods=["GET"])
def get_admin_stats():
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    
    total_diseases = diseases_collection.count_documents({})
    healthy_count = diseases_collection.count_documents({"is_healthy": True})
    diseased_count = diseases_collection.count_documents({"is_healthy": False})
    
    
    pipeline = [
        {"$group": {"_id": "$plant", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    plant_distribution = list(diseases_collection.aggregate(pipeline))
    
    return jsonify({
        "total_diseases": total_diseases,
        "healthy_count": healthy_count,
        "diseased_count": diseased_count,
        "plant_distribution": plant_distribution
    })

@app.route('/predict-image', methods=['POST'])
def predict_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        image = Image.open(io.BytesIO(file.read()))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx] * 100)
        predicted_class = CLASS_NAMES[predicted_class_idx]
        is_healthy = 'healthy' in predicted_class.lower()
        
        top_3_idx = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = [
            (CLASS_NAMES[i].replace('_', ' '), float(predictions[0][i] * 100))
            for i in top_3_idx
        ]
        
        disease_name = predicted_class.replace('_', ' ').title()
        
        response = {
            "status": "HEALTHY" if is_healthy else "DISEASED",
            "disease": disease_name if not is_healthy else "No disease detected",
            "confidence": confidence,
            "predicted_class": predicted_class,
            "top_3_predictions": top_3_predictions
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

@app.route('/predict-voice', methods=['POST', 'OPTIONS'])
def predict_voice():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({"error": "No audio file selected"}), 400
        
        print("[Voice] Received audio file")
        
        recognizer = sr.Recognizer()
        audio_data = audio_file.read()
        
        temp_webm_path = tempfile.mktemp(suffix='.webm')
        temp_wav_path = tempfile.mktemp(suffix='.wav')
        
        try:
            with open(temp_webm_path, 'wb') as f:
                f.write(audio_data)
            
            print(f"[Voice] Saved WebM audio to {temp_webm_path}")
            
            try:
                audio_segment = AudioSegment.from_file(temp_webm_path, format="webm")
                audio_segment = audio_segment.set_frame_rate(16000).set_channels(1)
                audio_segment.export(temp_wav_path, format="wav")
                print("[Voice] Converted WebM to WAV successfully")
            except Exception as conv_error:
                print(f"[Voice] Conversion error: {conv_error}")
                raise Exception("Could not convert audio format. Please try again.")
            
            with sr.AudioFile(temp_wav_path) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.record(source)
            
            print("[Voice] Audio loaded successfully")
            
            recognized_text = None
            detected_language = None
            
            languages_to_try = [
                ('en-IN', 'en'),
                ('hi-IN', 'hi'),
                ('kn-IN', 'kn'),
                ('te-IN', 'te'),
                ('ta-IN', 'ta'),
                ('ml-IN', 'ml'),
                ('mr-IN', 'mr'),
                ('gu-IN', 'gu'),
                ('bn-IN', 'bn'),
                ('pa-IN', 'pa'),
            ]
            
            for lang_code, lang_short in languages_to_try:
                try:
                    text = recognizer.recognize_google(audio, language=lang_code)
                    if text:
                        recognized_text = text
                        detected_language = lang_short
                        print(f"[Voice Recognition] Success: {lang_short} - '{text}'")
                        break
                except sr.UnknownValueError:
                    print(f"[Voice] Could not understand audio in {lang_code}")
                    continue
                except sr.RequestError as e:
                    print(f"[Voice] API Error with {lang_code}: {e}")
                    continue
        
        finally:
            try:
                if os.path.exists(temp_webm_path):
                    os.remove(temp_webm_path)
                    print(f"[Voice] Cleaned up WebM file")
            except Exception as e:
                print(f"[Voice] Could not delete WebM: {e}")
            
            try:
                if os.path.exists(temp_wav_path):
                    os.remove(temp_wav_path)
                    print(f"[Voice] Cleaned up WAV file")
            except Exception as e:
                print(f"[Voice] Could not delete WAV: {e}")
        
        if not recognized_text:
            print("[Voice] No speech recognized in any language")
            return jsonify({
                "error": "Could not understand audio. Please speak clearly and try again.",
                "supported_languages": [lang[1] for lang in languages_to_try]
            }), 400
        
        print(f"[Voice] Processing diagnosis for: '{recognized_text}'")
        
        diagnosis = diagnose_disease(recognized_text)
        
        print(f"[Voice] Diagnosis completed: {diagnosis is not None}")
        
        response = {
            "recognized_text": recognized_text,
            "detected_language": detected_language,
            "diagnosis": diagnosis,
            "formatted_output": format_diagnosis(diagnosis) if diagnosis else None
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"[Voice] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)