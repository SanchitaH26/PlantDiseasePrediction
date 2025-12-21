from deep_translator import GoogleTranslator
import re
DISEASE_NAME_TRANSLATIONS = {'hi': {"Tomato Early Blight": "टमाटर अर्ली ब्लाइट",
    "Tomato Late Blight": "टमाटर लेट ब्लाइट",
    "Tomato Leaf Mold": "टमाटर पत्ती फफूंदी",
        "Tomato Mosaic Virus": "टमाटर मोज़ेक वायरस",
        "Tomato Yellow Leaf Curl Virus": "टमाटर पत्ती पीलापन वायरस",
        "Tomato Septoria Leaf Spot": "टमाटर सेप्टोरिया पत्ती धब्बा",
        "Two-Spotted Spider Mite Infestation": "दो धब्बे वाला स्पाइडर माइट संक्रमण",
        "Tomato Target Spot": "टमाटर टारगेट स्पॉट",
        "Tomato Bacterial Spot": "टमाटर बैक्टीरियल स्पॉट",
        "Pepper Bacterial Spot": "शिमला मिर्च बैक्टीरियल स्पॉट",
        "Potato Early Blight": "आलू अर्ली ब्लाइट",
        "Potato Late Blight": "आलू लेट ब्लाइट",
        "Healthy Plant": "स्वस्थ पौधा",
        "Healthy Tomato Plant": "स्वस्थ टमाटर का पौधा",
        "Healthy Pepper Plant": "स्वस्थ मिर्च का पौधा",
        "Healthy Potato Plant": "स्वस्थ आलू का पौधा",
    },'kn': {
     "Tomato Early Blight": "ಟೊಮಾಟೊ ಪ್ರಾರಂಭಿಕ ಬ್ಲೈಟ್",
    "Tomato Late Blight": "ಟೊಮಾಟೊ ತಡ ಬ್ಲೈಟ್",
"Tomato Leaf Mold": "ಟೊಮಾಟೊ ಎಲೆ ಬೂದಿ",
    "Tomato Mosaic Virus": "ಟೊಮಾಟೊ ಮೋಸೈಕ್ ವೈರಸ್",
        "Tomato Yellow Leaf Curl Virus": "ಟೊಮಾಟೊ ಹಳದಿ ಎಲೆ ಮುಗುಳ್ನಗೆ ವೈರಸ್",
        "Tomato Septoria Leaf Spot": "ಟೊಮಾಟೊ ಸೆಪ್ಟೋರಿಯಾ ಎಲೆ ಕಲೆ",
        "Two-Spotted Spider Mite Infestation": "ಎರಡು ಕಲೆಗಳಿರುವ ಸ್ಪೈಡರ್ ಮೈಟ್ ಆಕ್ರಮಣ",
        "Tomato Target Spot": "ಟೊಮಾಟೊ ಟಾರ್ಗೆಟ್ ಸ್ಪಾಟ್",
        "Tomato Bacterial Spot": "ಟೊಮಾಟೊ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಕಲೆ",
        "Pepper Bacterial Spot": "ಮೆಣಸಿನಕಾಯಿ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಕಲೆ",
        "Potato Early Blight": "ಆಲೂಗಡ್ಡೆ ಪ್ರಾರಂಭಿಕ ಬ್ಲೈಟ್",
        "Potato Late Blight": "ಆಲೂಗಡ್ಡೆ ತಡ ಬ್ಲೈಟ್",
        "Healthy Plant": "ಆರೋಗ್ಯಕರ ಸಸಿ",
        "Healthy Tomato Plant": "ಆರೋಗ್ಯಕರ ಟೊಮಾಟೊ ಸಸಿ",
        "Healthy Pepper Plant": "ಆರೋಗ್ಯಕರ ಮೆಣಸಿನಕಾಯಿ ಸಸಿ",
        "Healthy Potato Plant": "ಆರೋಗ್ಯಕರ ಆಲೂಗಡ್ಡೆ ಸಸಿ",
    }
}
DISEASE_DATABASE = {
    "tomato bacterial spot": {
        "disease":"Tomato Bacterial Spot",
        "plant":"tomato",
        "symptoms":["dark spots", "yellow halo", "leaf spots", "black spots", "bacterial spots", 
                    "small spots", "water soaked", "greasy spots"],
        "cause":"Caused by Xanthomonas bacteria. Spreads through water splash, infected seeds, and contaminated tools.",
        "treatment":"""1. Remove and destroy infected leaves immediately
2.Apply copper-based bactericides every 7-10 days
3.Use copper hydroxide or copper sulfate sprays
4.Avoid overhead watering - water at soil level only
5.Use disease-free certified seeds
6.Practice 3-year crop rotation
7.Space plants 24-36 inches apart for air circulation
8.Disinfect tools with 10% bleach solution
9.Remove plant debris at end of season"""
 },
"tomato early blight": {
    "disease": "Tomato Early Blight",
  "plant": "tomato",
        "symptoms": ["brown spots", "target spots", "concentric rings", "bull's eye pattern", "bulls eye",
                    "leaf yellowing", "wilting", "dark spots with rings", "lower leaf spots", "brown leaf",
                    "circular spots", "ring pattern"],
        "cause": "Caused by Alternaria solani fungus. Thrives in warm (75-85°F), humid conditions.",
        "treatment": """1. Remove infected lower leaves immediately
2.Apply fungicide containing chlorothalonil or mancozeb
3.Spray every 7-10 days during wet weather
4.Mulch heavily (2-3 inches) to prevent soil splash
5.Water at base of plant only
6.Stake or cage plants to keep off ground
7.Ensure good air circulation - space 2-3 feet apart
8.Rotate crops annually (3-year rotation ideal)
9.Use resistant varieties
10.Remove all plant debris at season end"""
 },
"tomato late blight": {
        "disease": "Tomato Late Blight",
        "plant": "tomato",
        "symptoms": ["water soaked spots", "water soaked lesions", "white mold", "rapid wilting", 
                    "brown patches", "fuzzy growth", "gray mold", "blackened stems", "rotten fruit", 
                    "wet spots", "watery spots", "soaked"],
        "cause": "Caused by Phytophthora infestans. Spreads rapidly in cool, wet weather.",
        "treatment": """1. URGENT - Remove infected plants immediately
2. Apply preventive fungicide before symptoms appear
3. Use chlorothalonil, mancozeb, or copper fungicides
4. Spray every 5-7 days in wet weather
5. DO NOT compost infected material
6. Improve air circulation drastically
7. Avoid evening watering
8. Use resistant varieties
9. Harvest green tomatoes before blight reaches them"""
    },
    "tomato leaf mold": {
        "disease": "Tomato Leaf Mold",
        "plant": "tomato",
        "symptoms": ["yellow spots", "fuzzy mold", "gray mold underside", "olive green mold",
                    "leaf curl", "yellow patches", "velvety growth", "mold leaf", "fungus"],
        "cause": "Caused by Passalora fulva fungus. Loves high humidity and poor ventilation.",
        "treatment": """1. Remove affected leaves immediately
2. Increase ventilation significantly
3. Prune excess foliage for airflow
4. Lower humidity below 85%
5. Avoid overhead watering
6. Apply fungicide if severe
7. Use resistant varieties
8. Remove lower leaves touching soil"""
    },
    "tomato mosaic virus": {
        "disease": "Tomato Mosaic Virus",
        "plant": "tomato",
        "symptoms": ["mottled leaves", "mosaic pattern", "light and dark green patches", 
                    "distorted growth", "yellow streaks", "stunted plants", "fern leaf", "streaked"],
        "cause": "Viral infection. NO CURE EXISTS. Spreads through handling and tools.",
        "treatment": """1. NO CURE - Remove entire infected plant
2. DO NOT compost infected plants
3. Disinfect ALL tools with 10% bleach
4. Wash hands thoroughly before touching plants
5. Control aphids and whiteflies
6. Use virus-free seeds
7. Plant resistant varieties
8. Never smoke near tomato plants
9. Isolate new plants for 2 weeks"""
    },
    "tomato septoria leaf spot": {
        "disease": "Tomato Septoria Leaf Spot",
        "plant": "tomato",
        "symptoms": ["small circular spots", "dark margins", "gray centers", "yellow leaves",
                    "tan spots", "black dots in center", "lower leaf yellowing", "circular spots", "small spots"],
        "cause": "Caused by Septoria lycopersici fungus. Spreads through water splash.",
        "treatment": """1. Remove lower infected leaves immediately
2. Apply fungicide containing chlorothalonil or copper
3. Spray every 7-10 days during wet weather
4. Mulch heavily to prevent soil splash
5. Water at soil level ONLY
6. Stake plants 12+ inches off ground
7. Space plants 2-3 feet apart
8. Remove all plant debris at season end
9. Practice 2-3 year crop rotation"""
    },
    "tomato spider mites": {
        "disease": "Two-Spotted Spider Mite Infestation",
        "plant": "tomato",
        "symptoms": ["tiny webs", "stippled leaves", "bronze appearance", "yellow speckling",
                    "tiny moving dots", "leaf drop", "fine webbing", "pale leaves", "web", "spider"],
        "cause": "Caused by spider mites. Thrive in hot, dry conditions.",
        "treatment": """1. Spray with strong water jet daily
2. Apply insecticidal soap every 3 days
3. Use neem oil spray weekly
4. Increase humidity around plants
5. Release predatory mites
6. Remove heavily infested leaves
7. Avoid over-fertilizing
8. Use reflective mulch"""
    },
    "tomato target spot": {
        "disease": "Tomato Target Spot",
        "plant": "tomato",
        "symptoms": ["target spots", "concentric rings", "brown lesions", "bull's eye pattern", 
                    "rings spots", "target pattern"],
        "cause": "Caused by Corynespora cassiicola fungus.",
        "treatment": """1. Remove infected leaves and fruit
2. Apply fungicide (azoxystrobin or chlorothalonil)
3. Improve air circulation
4. Mulch to prevent soil splash
5. Water at base only
6. Practice crop rotation"""
    },
    "tomato yellow leaf curl virus": {
        "disease": "Tomato Yellow Leaf Curl Virus",
        "plant": "tomato",
        "symptoms": ["yellow curled leaves", "upward leaf curl", "stunted growth", 
                    "no fruit", "reduced fruit set", "small leaves", "bushy appearance", 
                    "yellow curl", "curl yellow", "curled", "curling"],
        "cause": "Spread by whiteflies. NO CURE.",
        "treatment": """1. NO CURE - Remove infected plants
2. Control whiteflies aggressively
3. Use yellow sticky traps
4. Apply neem oil twice weekly
5. Use reflective aluminum mulch
6. Plant resistant varieties
7. Use insect screening for young plants
8. Remove weeds that harbor whiteflies"""
    },
    "tomato healthy": {
        "disease": "Healthy Tomato Plant",
        "plant": "tomato",
        "symptoms": ["green leaves", "no spots", "vigorous growth", "healthy appearance", 
                    "healthy", "good", "normal", "fine"],
        "cause": "Plant is healthy!",
        "treatment": """Your tomato plant is healthy! Maintain good practices:
1. Water 1-2 inches per week
2. Fertilize every 2-3 weeks
3. Monitor for pests weekly
4. Prune suckers for indeterminate varieties
5. Mulch with 2-3 inches organic material
6. Ensure 6-8 hours sunlight daily
7. Support with stakes or cages"""
    },
    "pepper bacterial spot": {
        "disease": "Pepper Bacterial Spot",
        "plant": "pepper",
        "symptoms": ["raised spots", "brown lesions", "brown spots", "yellow halo", 
                    "defoliation", "corky spots", "water soaked spots", "leaf drop"],
        "cause": "Caused by Xanthomonas bacteria. Spreads through seeds, water, tools.",
        "treatment": """1. Remove infected leaves immediately
2. Apply copper bactericide weekly
3. Use disease-free certified seeds
4. Disinfect tools between plants
5. Avoid overhead irrigation
6. Rotate crops for 3 years
7. Space plants 18-24 inches apart
8. Remove plant debris at season end"""
    },
    "pepper healthy": {
        "disease": "Healthy Pepper Plant",
        "plant": "pepper",
        "symptoms": ["green leaves", "no spots", "vigorous growth", "healthy appearance", 
                    "healthy", "good", "normal", "fine"],
        "cause": "Plant is healthy!",
        "treatment": """Your pepper plant is healthy! Maintain good practices:
1. Water 1 inch per week
2. Fertilize every 2 weeks
3. Monitor for aphids, spider mites
4. Ensure 6-8 hours sunlight
5. Mulch to retain moisture
6. Support heavy branches
7. Harvest regularly"""
    },
    "potato early blight": {
        "disease": "Potato Early Blight",
        "plant": "potato",
        "symptoms": ["brown spots", "concentric rings", "target pattern", "bull's eye spots",
                    "yellowing", "lower leaf spots", "dark lesions", "rings brown", "circular"],
        "cause": "Caused by Alternaria solani fungus. Overwinters in soil debris.",
        "treatment": """1. Remove infected foliage immediately
2. Apply fungicide (mancozeb or chlorothalonil)
3. Spray every 7-10 days in wet weather
4. Hill soil around plants
5. Practice 3-4 year crop rotation
6. Destroy plant debris after harvest
7. Use certified disease-free seed potatoes
8. Space rows 30-36 inches apart"""
    },
    "potato late blight": {
        "disease": "Potato Late Blight",
        "plant": "potato",
        "symptoms": ["water soaked lesions", "water soaked spots", "white mold", 
                    "blackened stems", "rotten tubers", "brown patches", "fuzzy white growth", 
                    "wet spots", "watery", "soaked"],
        "cause": "Caused by Phytophthora infestans. EXTREMELY DESTRUCTIVE.",
        "treatment": """1. EMERGENCY - Act immediately!
2. Apply preventive fungicide
3. Spray every 5-7 days in wet weather
4. Remove infected plants entirely
5. Never compost infected material
6. Harvest early before blight reaches tubers
7. Kill vines 2 weeks before harvest
8. Use resistant varieties
9. Destroy volunteer potatoes"""
    }, 
    "potato healthy": {
        "disease": "Healthy Potato Plant",
        "plant": "potato",
        "symptoms": ["green leaves", "no spots", "vigorous growth", "healthy foliage", 
                    "healthy", "good", "normal", "fine"],
        "cause": "Plant is healthy!",
        "treatment": """Your potato plant is healthy! Maintain good practices:
1. Water deeply once a week
2. Hill soil as plants grow
3. Monitor for Colorado potato beetles
4. Apply mulch to retain moisture
5. Fertilize at planting and flowering
6. Harvest when foliage dies back
7. Cure potatoes before storage"""
    },
    "healthy": {
        "disease": "Healthy Plant",
        "plant": "general",
        "symptoms": ["green leaves", "no spots", "vigorous growth", "no discoloration", 
                    "healthy", "good", "normal", "fine"],
        "cause": "Plant is healthy!",
        "treatment": """Your plant is healthy! General care tips:
1. Water consistently
2. Fertilize regularly
3. Monitor for pests weekly
4. Ensure proper spacing
5. Remove dead leaves promptly
6. Practice crop rotation
7. Keep area clean and weed-free
8. Mulch appropriately"""
    }
}
INDIAN_LANGUAGES={'hi':'Hindi','kn':'Kannada','te':'Telugu','ta':'Tamil','mr':'Marathi','gu':'Gujarati','bn':'Bengali','ml':'Malayalam','pa':'Punjabi','or':'Odia','as':'Assamese','ur':'Urdu'
}
def detect_language(text):
    script_ranges={'hi':r'[\u0900-\u097F]','kn':r'[\u0C80-\u0CFF]','te':r'[\u0C00-\u0C7F]','ta':r'[\u0B80-\u0BFF]','ml':r'[\u0D00-\u0D7F]', 'gu':r'[\u0A80-\u0AFF]','pa':r'[\u0A00-\u0A7F]','bn':r'[\u0980-\u09FF]', 'or':r'[\u0B00-\u0B7F]'}
    for lang_code,pattern in script_ranges.items():
        if re.search(pattern,text):
            return lang_code
    return 'en'
def translate_text(text,source_lang='auto',target_lang='en'):
    try:
        if source_lang==target_lang:
            return text
        if source_lang=='auto':
            source_lang=detect_language(text)
            if source_lang==target_lang:
                return text
        translated=GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text
def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]',' ',text)
    text = re.sub(r'\s+',' ',text)
    return text
def extract_plant_type(user_input):
    user_input=normalize_text(user_input)
    plant_keywords={'tomato':['tomato','tomatoes','tomatos'],'pepper':['pepper','peppers','bellpepper','chili','chilli','capsicum'],'potato':['potato','potatoes','potatos']}
    for plant,keywords in plant_keywords.items():
        for keyword in keywords:
            if keyword in user_input:
                return plant
    return None
def symptom_match(symptom, text):
    symptom_words=symptom.lower().split()
    matches=sum(1 for word in symptom_words if word in text)
    return matches>=len(symptom_words)*0.6
def extract_symptoms(user_input):
    user_input=normalize_text(user_input)
    detected_symptoms=[]
    for disease_key,disease_info in DISEASE_DATABASE.items():
        for symptom in disease_info["symptoms"]:
            if symptom_match(symptom, user_input):
                detected_symptoms.append((disease_key,symptom))
    return detected_symptoms
def diagnose_disease(user_input,auto_translate_output=True):
    original_input=user_input
    input_lang=detect_language(user_input)
    print(f"\n[DEBUG] Original input:{original_input}")
    print(f"[DEBUG] Detected language:{input_lang}")
    english_input=user_input
    if input_lang!='en':
        english_input=translate_text(user_input,source_lang=input_lang,target_lang='en')
        print(f"[DEBUG] Translated to English:{english_input}")
    normalized_input=normalize_text(english_input)
    print(f"[DEBUG] Normalized:{normalized_input}")
    plant_type=extract_plant_type(normalized_input)
    print(f"[DEBUG] Detected plant:{plant_type}")
    detected = extract_symptoms(normalized_input)
    print(f"[DEBUG] Detected symptoms: {len(detected)} matches")
    if not detected:
        return None
    disease_scores={}
    for disease_key,symptom in detected:
        disease_info=DISEASE_DATABASE[disease_key]
        score=1
        if plant_type and disease_info.get('plant')==plant_type:
            score+=10
        elif plant_type and disease_info.get('plant')!=plant_type and disease_info.get('plant')!='general':
            score-=5
        disease_scores[disease_key]=disease_scores.get(disease_key, 0)+score
    if not disease_scores:
        return None
    best_match=max(disease_scores.items(),key=lambda x:x[1])
    print(f"[DEBUG] Best match:{best_match[0]} (score:{best_match[1]})")
    result=DISEASE_DATABASE[best_match[0]].copy()
    result['input_language']=input_lang
    result['english_translation']=english_input if input_lang != 'en' else None
    result['confidence_score']=best_match[1]
    result['is_healthy']='healthy' in best_match[0]
    if auto_translate_output and input_lang!='en':
        if input_lang in DISEASE_NAME_TRANSLATIONS and result['disease'] in DISEASE_NAME_TRANSLATIONS[input_lang]:
            result['disease']=DISEASE_NAME_TRANSLATIONS[input_lang][result['disease']]
        else:
            result['disease']=translate_text(result['disease'],source_lang='en',target_lang=input_lang)
        result['cause']=translate_text(result['cause'],source_lang='en',target_lang=input_lang)
        result['treatment']=translate_text(result['treatment'],source_lang='en',target_lang=input_lang)
    return result
def format_diagnosis(diagnosis, show_debug=False):
    if not diagnosis:
        return """
Could not identify the disease from your description.
Please try:
1.Mention the plant type (tomato/pepper/potato)
2.Describe symptoms clearly (brown spots, yellow leaves, etc.)
3.Mention patterns (rings, mold, wilting, curling)
Examples:
English:"My tomato has brown spots with rings"
Hindi:"मेरे टमाटर की पत्तियों पर भूरे धब्बे हैं"
Kannada:"ಟೊಮಾಟೊ ಎಲೆಯಲ್ಲಿ ಕಂದು ಕಲೆಗಳು"
        """
    is_healthy=diagnosis.get('is_healthy', False)
    input_lang=diagnosis.get('input_language', 'en')
    if is_healthy:
        if input_lang!='en':
            status_label=translate_text("STATUS",source_lang='en',target_lang=input_lang)
            plant_label=translate_text("PLANT",source_lang='en',target_lang=input_lang)
            observation_label=translate_text("OBSERVATION",source_lang='en',target_lang=input_lang)
            care_tips_label=translate_text("CARE TIPS",source_lang='en',target_lang=input_lang)
            note_label=translate_text("NOTE",source_lang='en',target_lang=input_lang)
            note_text=translate_text("Continue regular monitoring and maintenance.",source_lang='en',target_lang=input_lang)
        else:
            status_label="STATUS"
            plant_label="PLANT"
            observation_label="OBSERVATION"
            care_tips_label="CARE TIPS"
            note_label="NOTE"
            note_text="Continue regular monitoring and maintenance."
        output=f"""
{status_label}:{diagnosis['disease']}
{plant_label}:{diagnosis.get('plant', 'Unknown').title()}
"""
    else:
        if input_lang!='en':
            disease_label=translate_text("DISEASE",source_lang='en',target_lang=input_lang)
            plant_label=translate_text("PLANT",source_lang='en',target_lang=input_lang)
            cause_label=translate_text("CAUSE",source_lang='en',target_lang=input_lang)
            treatment_label=translate_text("TREATMENT",source_lang='en',target_lang=input_lang)
            note_label=translate_text("NOTE",source_lang='en',target_lang=input_lang)
            note_text=translate_text("For severe infections, consult local agricultural experts.",source_lang='en',target_lang=input_lang)
        else:
            disease_label="DISEASE"
            plant_label="PLANT"
            cause_label="CAUSE"
            treatment_label="TREATMENT"
            note_label="NOTE"
            note_text="For severe infections, consult local agricultural experts."
        output=f"""
{disease_label}:{diagnosis['disease']}
{plant_label}:{diagnosis.get('plant', 'Unknown').title()}
"""
    if show_debug:
        output+=f"\n[DEBUG INFO]"
        output+=f"\nInput Language:{diagnosis.get('input_language','N/A')}"
        if diagnosis.get('english_translation'):
            output+=f"\nEnglish Translation: {diagnosis['english_translation']}"
        if diagnosis.get('confidence_score'):
            output+=f"\nConfidence Score: {diagnosis['confidence_score']}"
        output+="\n" 
    if is_healthy:
        output+=f"""
{observation_label}:
{diagnosis['cause']}
{care_tips_label}:
{diagnosis['treatment']}
{note_label}:{note_text}
"""
    else:
        output+=f"""
{cause_label}:
{diagnosis['cause']}
{treatment_label}:
{diagnosis['treatment']}
{note_label}: {note_text}
""" 
    return output
if __name__=="__main__":
    print("MULTILINGUAL PLANT DISEASE DIAGNOSIS SYSTEM")
    print("Supports All Major Indian Languages")
    test_inputs = [
        "My tomato has brown spots with concentric rings",
        "मेरे टमाटर की पत्तियों पर भूरे धब्बे हैं",
        "ಟೊಮಾಟೊ ಎಲೆಯಲ್ಲಿ ಕಂದು ಕಲೆಗಳು",
        "My tomato plant is healthy",
        "మా టమాటా మొక్క ఆరోగ్యంగా ఉంది",
    ]
    print("RUNNING TEST CASES")
    for test_input in test_inputs:
        print(f"INPUT:{test_input}")
        try:
            result=diagnose_disease(test_input,auto_translate_output=True)
            print(format_diagnosis(result,show_debug=True))
        except Exception as e:
            print(f"Error:{e}")
            ("continueError:{e}")
    print("INTERACTIVE MODE")
    print("Type in any Indian language!")
    print("Commands: 'quit' to exit")
    while True:
        try:
            user_input=input("\nDescribe the plant problem: ").strip()
            if user_input.lower()=='quit':
                print("\nThank you for using the Plant Disease Diagnosis System!")
                break
            if not user_input:
                print("Please enter a description.")
                continue
            print("\nProcessing...")
            diagnosis = diagnose_disease(user_input,auto_translate_output=True)
            print(format_diagnosis(diagnosis,show_debug=True))
        except KeyboardInterrupt:
            print("\n\nThank you!")
            break
        except Exception as e:
            print(f"Unexpected Error: {e}")
            continue