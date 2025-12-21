# Plant Disease Detection System

An AI-powered, role-based multilingual platform for early plant disease detection using **deep learning**, **natural language processing**, and **voice recognition**.  
The system supports farmers through image, text, and voice-based diagnosis, while providing administrators with full control over disease data via a secure dashboard. 
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

### **Voice-based Symptom Input**
- English voice input using **Google Speech Recognition API**
- Converts spoken symptoms into text in real time
- Seamlessly integrates with existing NLP diagnosis pipeline
- Enables hands-free interaction for farmers

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

## Secure Authentication & Role-Based Access

The system includes a secure login mechanism with **role-based access control** to ensure appropriate functionality for different users.

### **Farmer Login**
- Access to:
  - Image-based disease detection
  - Text-based symptom diagnosis
  - Voice-based symptom input (English)
- Receives disease diagnosis, causes, and treatment recommendations
- Simple, chatbot-style interface for ease of use

### **Admin Login**
- Access to an **Admin Dashboard**
- Can manage plant disease data stored in the database:
  - View all diseases from the PlantVillage dataset
  - Add new diseases
  - Edit existing disease details
  - Delete obsolete or incorrect disease records
- All changes are **persisted securely in the database**

### **Security**
- User credentials are securely stored using **SHA-256 (SHA-2) hashing**
- Plain-text passwords are never stored
- Role validation is enforced during login

---

# Tech Stack

## Backend
- Flask (Python 3.8+)
- TensorFlow 2.x, Keras
- Deep Translator  
- Pillow, NumPy  
- Flask-CORS
- MongoDB (User authentication & disease data storage)
- Secure password hashing (SHA-2 / SHA-256)


## Frontend
- HTML5  
- CSS3  
- JavaScript
- Google Speech Recognition API for voice input
- Role-based UI rendering (Farmer / Admin)
 

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

# Admin Dashboard

The Admin Dashboard provides complete control over disease data used by the system.

### **Admin Capabilities**
- View all plant diseases stored in the database
- Add new disease entries with symptoms and treatment details
- Update existing disease information
- Delete diseases when required

### **Real-Time Updates**
- Any changes made by the admin are immediately reflected in:
  - Farmer chatbot responses
  - Text-based and voice-based diagnosis

# Screenshots
## **Login Page**

<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/c69abc97-b28d-4b6a-9d7c-f77392a4b4a2" />

## **Farmer Dashboard (Chatbot & Detection)**

<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/c9d7fa43-e768-4cca-9ae6-51c8660734a1" />

## **Admin Dashboard**

<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/af5f624e-e91f-48bc-b1d2-1cbe1246ea22" />

## **Disease management by Admin**

<img width="1874" height="803" alt="image" src="https://github.com/user-attachments/assets/6a779eae-608c-4659-8ace-26961634f1d2" />

## **Image-Based Detection**

<img width="751" height="657" alt="image" src="https://github.com/user-attachments/assets/35ca1c5e-1856-4a7d-a656-ebe16f729ab1" />

## **Text-Based Diagnosis**

<img width="702" height="561" alt="image" src="https://github.com/user-attachments/assets/481ed867-d069-4a19-b3c1-a3f49e5dee5d" />

## **Multilingual text based analysis**

<img width="777" height="582" alt="image" src="https://github.com/user-attachments/assets/deee30ff-6dbd-4e60-beb4-62cdd310e950" />

## **Voice based (which is then converted into text) analysis**

<img width="720" height="536" alt="image" src="https://github.com/user-attachments/assets/906f1669-7c7e-4703-bf03-4d20aa3e29a6" />

# Future Enhancements

- Multilingual voice input (Indian languages)
- Mobile application support
- Offline diagnosis mode
- Crop-specific advisory recommendations
- Integration with government agricultural databases


# License:

MIT License
