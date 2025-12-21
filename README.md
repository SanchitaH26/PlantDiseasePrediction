# Plant Disease Detection System

An AI-powered multilingual platform for early plant disease detection using **deep learning** and **natural language processing**.  
Supports **13 languages**, including **12 major Indian languages**, enabling farmers to diagnose plant diseases through **image uploads** or **symptom descriptions** in their native language.

---

## Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Supported Diseases](#-supported-diseases)
- [Supported Languages](#-supported-languages)
- [Model Performance](#-model-performance)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)

---

# Features

## Dual Detection System

### **Image-based Detection**
- Upload plant leaf images  
- CNN-based disease classification (**92–95% accuracy**)

### **Text-based Diagnosis**
- Describe symptoms in any supported language  
- NLP-based disease diagnosis (**75–82% accuracy**)

---

## Multilingual Support

- **13 Languages:**  
  English + Hindi, Kannada, Telugu, Tamil, Malayalam, Marathi, Gujarati, Bengali, Punjabi, Odia, Urdu, Assamese  
- **Automatic Language Detection:** Unicode script-based 
- **Real-time Translation:** Deep Translator API  
- **Localized Output:** Disease name, cause & treatment in user's own language  

---

## User-Friendly Interface

- Drag-and-drop image upload  
- Clean multilingual diagnosis interface  
- Lightweight frontend (HTML/CSS/JS)  

---

# Tech Stack

## Backend
- Flask (Python 3.8+)
- TensorFlow 2.x, Keras
- Deep Translator  
- Pillow, NumPy  
- Flask-CORS  

## Frontend
- HTML5  
- CSS3  
- JavaScript  

## Machine Learning
- Custom CNN model  
- Dataset: **PlantVillage** (54k images)  
- Image size: **128×128 RGB**  
- Normalization: Scale `[0,1]`  
- Train/Validation: **80/20 split**

## NLP & Translation
- Unicode-based language detection  
- Deep Translator for multilingual support  
- Regex-based symptom extraction  

---

# Installation

## **Prerequisites**
- Python 3.8+
- pip
- 4GB RAM recommended
- Internet connection (for translation API)

---

## **Step 1 — Clone Repository**

```bash
git clone https://github.com/yourusername/plant-disease-detection.git
cd plant-disease-detection
```
## **Step 2 — Install Dependencies**
```bash
pip install -r requirements.txt
```

## **requirements.txt**
``` bash
flask==2.3.0
flask-cors==4.0.0
tensorflow==2.13.0
numpy==1.24.3
pillow==10.0.0
deep-translator==1.11.4
```
---

## **Step 3 — Add Model File**

**Place your trained model file:**

plant_disease_model.h5

in the project root directory.

## **Step 4 — Run Backend Server**
python app.py

Server runs at:

http://localhost:5000

## **Step 5 — Run Frontend**
python -m http.server 8000

Open:

http://localhost:8000

# Usage
## **Image-based Detection**

Open Image Upload tab

Upload a plant leaf image (JPG/PNG)

Click Analyze Image

View predicted disease & confidence score

## **Text-based Diagnosis**

Open Describe Symptoms tab

Enter symptoms in any language

Click Diagnose Disease

Receive diagnosis in the same language

## **Example Inputs:**

English: brown circular spots on leaf

Hindi: टमाटर की पत्तियों पर भूरे धब्बे

Kannada: ಟೊಮಾಟೊ ಎಲೆಯಲ್ಲಿ ಕಂದು ಕಲೆಗಳು


# Supported Diseases

Tomato Early Blight,Tomato Late Blight,Tomato Leaf Mold,Tomato Mosaic Virus,Tomato Yellow Leaf Curl Virus,Pepper Bacterial Spot,Potato Late Blight,Potato Early Blight,Healthy Leaf Detection

# Supported Languages

Kannada,English,Hindi,Tamil,Telugu,Malayalam,Marathi,Gujarati,Bengali,Punjabi,Odia,Urdu,Assamese

# Model Performance
Detection Mode	Accuracy
CNN Image-Based	92–95%

# Screenshots
## **Home Interface**

<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/0ea8a854-5a69-45ad-b605-84d7fa44995f" />


## **Image-Based Detection**

<img width="618" height="668" alt="image" src="https://github.com/user-attachments/assets/e40fdd4b-e28b-4d5f-842e-e85b7c1cef51" />


## **Text-Based Diagnosis**

<img width="618" height="668" alt="image" src="https://github.com/user-attachments/assets/dca6b246-e052-450b-a3c0-a8b3c674d3b0" />

## **Multilingual text based analysis**

<img width="584" height="668" alt="image" src="https://github.com/user-attachments/assets/c0770e29-19a7-4452-8038-b92dbc77a042" />


# Future Enhancements

Support for 20+ plant species

ONNX model for mobile apps

Voice-based symptom input

Offline mode

In-app farmer advisory system

# License:

MIT License
