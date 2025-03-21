import pandas as pd
import time
import pickle
import transformers
import torch
import accelerate
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from huggingface_hub import login
import json
import argparse

device = "cuda"  # specify device

model_id = "Qwen/Qwen2.5-7B-Instruct"

# Load the model with a specified cache directory
model = AutoModelForCausalLM.from_pretrained(model_id, cache_dir="TODO", torch_dtype="auto", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir="TODO")



parser = argparse.ArgumentParser()
parser.add_argument("--lang", default='en', type=str, required=True,
                        help="The language of prompt, selected from: [en, fr, es, nl, ru]")
parser.add_argument("--test_lang", default='en', type=str, required=True,
                        help="The language of prompt, selected from: [en, fr, es, nl, ru]")
parser.add_argument("--type", default='amazonfood', type=str, required=True)
args = parser.parse_args()

def get_category(type):
# "amazonfood" "coursera" "education" "hotel" "laptop" "phone" "res"
    if type == "amazonfood":
        return ['amazon availability', 'amazon prices', 'food general', 'food misc', 'food prices', 'food quality', 'food recommendation', 'food style_options', 'polarity negative', 'polarity positive', 'shipment delivery', 'shipment prices', 'shipment quality']
    elif type == "coursera":
        return ['assignments comprehensiveness', 'assignments quality', 'assignments quantity', 'assignments relatability', 'assignments workload', 'course comprehensiveness', 'course general', 'course quality', 'course relatability', 'course value', 'course workload', 'faculty comprehensiveness', 'faculty general', 'faculty relatability', 'faculty response', 'faculty value', 'grades general', 'material comprehensiveness', 'material quality', 'material quantity', 'material relatability', 'material workload', 'polarity negative', 'polarity neutral', 'polarity positive', 'presentation comprehensiveness', 'presentation quality', 'presentation quantity', 'presentation relatability', 'presentation workload']
    elif type == "education":
        return ['Course_General_Feedback', 'Instructor', 'Mathematical_Related_Concept', 'Other', 'Teaching_Setup']
    elif type == "hotel":
        return ['facilities cleanliness', 'facilities comfort', 'facilities design_features', 'facilities general', 'facilities miscellaneous', 'facilities prices', 'facilities quality', 'food_drinks miscellaneous', 'food_drinks prices', 'food_drinks quality', 'food_drinks style_options', 'hotel cleanliness', 'hotel comfort', 'hotel design_features', 'hotel general', 'hotel miscellaneous', 'hotel prices', 'hotel quality', 'location general', 'polarity negative', 'polarity neutral', 'polarity positive', 'room_amenities cleanliness', 'room_amenities comfort', 'room_amenities design_features', 'room_amenities general', 'room_amenities miscellaneous', 'room_amenities prices', 'room_amenities quality', 'rooms cleanliness', 'rooms comfort', 'rooms design_features', 'rooms general', 'rooms miscellaneous', 'rooms prices', 'rooms quality', 'service general']
    elif type == "laptop":
        return ['BATTERY#DESIGN_FEATURES', 'BATTERY#GENERAL', 'BATTERY#OPERATION_PERFORMANCE', 'BATTERY#QUALITY', 'COMPANY#DESIGN_FEATURES', 'COMPANY#GENERAL', 'COMPANY#OPERATION_PERFORMANCE', 'COMPANY#PRICE', 'COMPANY#QUALITY', 'CPU#DESIGN_FEATURES', 'CPU#GENERAL', 'CPU#OPERATION_PERFORMANCE', 'CPU#PRICE', 'CPU#QUALITY', 'DISPLAY#DESIGN_FEATURES', 'DISPLAY#GENERAL', 'DISPLAY#OPERATION_PERFORMANCE', 'DISPLAY#PRICE', 'DISPLAY#QUALITY', 'DISPLAY#USABILITY', 'FANS&COOLING#DESIGN_FEATURES', 'FANS&COOLING#GENERAL', 'FANS&COOLING#OPERATION_PERFORMANCE', 'FANS&COOLING#QUALITY', 'GRAPHICS#DESIGN_FEATURES', 'GRAPHICS#GENERAL', 'GRAPHICS#OPERATION_PERFORMANCE', 'GRAPHICS#USABILITY', 'HARDWARE#DESIGN_FEATURES', 'HARDWARE#GENERAL', 'HARDWARE#OPERATION_PERFORMANCE', 'HARDWARE#PRICE', 'HARDWARE#QUALITY', 'HARDWARE#USABILITY', 'HARD_DISC#DESIGN_FEATURES', 'HARD_DISC#GENERAL', 'HARD_DISC#OPERATION_PERFORMANCE', 'HARD_DISC#PRICE', 'HARD_DISC#QUALITY', 'HARD_DISC#USABILITY', 'KEYBOARD#DESIGN_FEATURES', 'KEYBOARD#GENERAL', 'KEYBOARD#OPERATION_PERFORMANCE', 'KEYBOARD#PORTABILITY', 'KEYBOARD#PRICE', 'KEYBOARD#QUALITY', 'KEYBOARD#USABILITY', 'LAPTOP#CONNECTIVITY', 'LAPTOP#DESIGN_FEATURES', 'LAPTOP#GENERAL', 'LAPTOP#MISCELLANEOUS', 'LAPTOP#OPERATION_PERFORMANCE', 'LAPTOP#PORTABILITY', 'LAPTOP#PRICE', 'LAPTOP#QUALITY', 'LAPTOP#USABILITY', 'MEMORY#DESIGN_FEATURES', 'MEMORY#GENERAL', 'MEMORY#OPERATION_PERFORMANCE', 'MEMORY#QUALITY', 'MEMORY#USABILITY', 'MOTHERBOARD#OPERATION_PERFORMANCE', 'MOTHERBOARD#QUALITY', 'MOUSE#GENERAL', 'MULTIMEDIA_DEVICES#CONNECTIVITY', 'MULTIMEDIA_DEVICES#DESIGN_FEATURES', 'MULTIMEDIA_DEVICES#GENERAL', 'MULTIMEDIA_DEVICES#OPERATION_PERFORMANCE', 'MULTIMEDIA_DEVICES#PRICE', 'MULTIMEDIA_DEVICES#QUALITY', 'MULTIMEDIA_DEVICES#USABILITY', 'OPTICAL_DRIVES#DESIGN_FEATURES', 'OPTICAL_DRIVES#GENERAL', 'OPTICAL_DRIVES#OPERATION_PERFORMANCE', 'OPTICAL_DRIVES#USABILITY', 'OS#DESIGN_FEATURES', 'OS#GENERAL', 'OS#MISCELLANEOUS', 'OS#OPERATION_PERFORMANCE', 'OS#QUALITY', 'OS#USABILITY', 'Out_Of_Scope#GENERAL', 'Out_Of_Scope#OPERATION_PERFORMANCE', 'Out_Of_Scope#USABILITY', 'PORTS#CONNECTIVITY', 'PORTS#DESIGN_FEATURES', 'PORTS#GENERAL', 'PORTS#OPERATION_PERFORMANCE', 'PORTS#PORTABILITY', 'PORTS#QUALITY', 'PORTS#USABILITY', 'POWER_SUPPLY#CONNECTIVITY', 'POWER_SUPPLY#DESIGN_FEATURES', 'POWER_SUPPLY#GENERAL', 'POWER_SUPPLY#OPERATION_PERFORMANCE', 'POWER_SUPPLY#QUALITY', 'SHIPPING#GENERAL', 'SHIPPING#OPERATION_PERFORMANCE', 'SHIPPING#PRICE', 'SHIPPING#QUALITY', 'SOFTWARE#DESIGN_FEATURES', 'SOFTWARE#GENERAL', 'SOFTWARE#OPERATION_PERFORMANCE', 'SOFTWARE#PORTABILITY', 'SOFTWARE#PRICE', 'SOFTWARE#QUALITY', 'SOFTWARE#USABILITY', 'SUPPORT#DESIGN_FEATURES', 'SUPPORT#GENERAL', 'SUPPORT#OPERATION_PERFORMANCE', 'SUPPORT#PRICE', 'SUPPORT#QUALITY', 'WARRANTY#GENERAL', 'WARRANTY#QUALITY']
    elif type == "phone":
        return ['After-sales Service#Exchange/Warranty/Return', 'Appearance Design#Aesthetics General', 'Appearance Design#Color', 'Appearance Design#Exterior Design Material', 'Appearance Design#Fuselage Size', 'Appearance Design#Grip Feeling', 'Appearance Design#Thickness', 'Appearance Design#Weight', 'Appearance Design#Workmanship and Texture', 'Audio/Sound#Tone quality', 'Audio/Sound#Volume and Speaker', 'Battery/Longevity#Battery Capacity', 'Battery/Longevity#Battery Life', 'Battery/Longevity#Charging Method', 'Battery/Longevity#Charging Speed', 'Battery/Longevity#General', 'Battery/Longevity#Power Consumption Speed', 'Battery/Longevity#Standby Time', 'Branding/Marketing#Promotional Giveaways', 'Buyer Attitude#Loyalty', 'Buyer Attitude#Recommendable', 'Buyer Attitude#Repurchase and Churn Tendency', 'Buyer Attitude#Shopping Experiences', 'Buyer Attitude#Shopping Willingness', 'Camera#Fill light', 'Camera#Front Camera', 'Camera#General', 'Camera#Rear Camera', 'Ease of Use#Audience Groups', 'Ease of Use#Easy to Use', 'Intelligent Assistant#Intelligent Assistant General', 'Intelligent Assistant#Wake-up Function', 'Key Design#General', 'Logistics#Lost and Damaged', 'Logistics#Shipping Fee', 'Logistics#Speed', 'Logistics#general', 'Overall#Overall', 'Performance#General', 'Performance#Heat Generation', 'Performance#Running Speed', 'Price#Price', 'Price#Value for Money', 'Product Accessories#Cell Phone Film', 'Product Accessories#Charger', 'Product Accessories#Charging Cable', 'Product Accessories#Headphones', 'Product Accessories#Phone Cases', 'Product Configuration#CPU', 'Product Configuration#Memory', 'Product Configuration#Operating Memory', 'Product Packaging#Completeness of Accessories', 'Product Packaging#General', 'Product Packaging#Instruction Manual', 'Product Packaging#Packaging Grade', 'Product Packaging#Packaging Materials', 'Product Quality#Cleanliness', 'Product Quality#Dustproof', 'Product Quality#Fall Protection', 'Product Quality#General', 'Product Quality#Genuine Product', 'Product Quality#Water Resistant', 'Screen#Clarity', 'Screen#General', 'Screen#Screen-to-Body Ratio', 'Screen#Size', 'Security#Screen Unlock', 'Seller Service#Attitude', 'Seller Service#Inventory', 'Seller Service#Seller Expertise', 'Seller Service#Shipping', 'Seller Service#Timeliness of Seller Service', 'Shooting Functions#General', 'Shooting Functions#Pixel', 'Signal#Call Quality', 'Signal#Signal General', 'Signal#Signal of Mobile Network', 'Signal#Wifi Signal', 'Smart Connect#Bluetooth Connection', 'Smart Connect#Positioning and GPS', 'System#Application', 'System#Lock Screen Design', 'System#NFC', 'System#Operation Smoothness', 'System#Software Compatibility', 'System#System General', 'System#System Upgrade', 'System#UI Interface Aesthetics']
    elif type == "res":
        return ['location general', 'food prices', 'food quality', 'ambience general', 'service general', 'restaurant prices', 'drinks prices', 'restaurant miscellaneous', 'drinks quality', 'drinks style_options', 'restaurant general', 'food style_options']

def read_sentences_from_file(file_path):
    sentences = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Split the line at the first occurrence of '####' and take the part before it
            sentence = line.split('####')[0].strip()
            sentences.append(sentence)
    return sentences

# Function to analyze sentiments and save results to JSON
def analyze_sentiments(file_path, output_json_path):
    sentences = read_sentences_from_file(file_path)
    results = []

    for sentence in sentences:
        print('Analyzing sentence: ' + sentence)

        if args.lang == 'en':
            prompt = (
    f"""
Aspect-Based Sentiment Analysis (ABSA) requires identifying specific entities mentioned in a text and determining the sentiment expressed toward each entity.

Each entity is associated with:
- A category from the list: {str(get_category(args.type))}.
- A sentiment: [positive, negative, neutral].

Your task is to:
1. Identify entities in the text, along with their categories and sentiments.
2. For each identified entity, assign a category from the provided category list.
3. Determine the sentiment for each entity as one of [positive, negative, neutral].
4. Return the results as a list of dictionaries, each containing the entity, category, and sentiment. If no entities are found, return an empty list.

Example Output Format:
[
  {"entity": "<entity>", "category": "<category>", "sentiment": "<sentiment>"}
]

Please return the final output (not code) in JSON format based on the following text:
Text: '{sentence}'.
"""
)
        elif args.lang == 'fr':
            prompt = (
                # "Veuillez identifier les termes d’aspect mentionnés dans le texte donné ci-dessous. "
                # "Pour chaque terme d’aspect, déterminez si le sentiment est [positif, négatif, neutre]. "
                "Veuillez identifier les termes d’aspect mentionnés dans le texte donné ci-dessous. Pour chaque terme d’aspect, déterminez si le sentiment est [positive, negative, neutral]. Retournez le résultat au format JSON uniquement avec les clés 'aspect' et 'sentiment'. "
                f"Texte : '{sentence}'."
            )
        elif args.lang == 'es':
            prompt = (
                # "Por favor, identifique los términos de aspecto mencionados en el siguiente texto dado. "
                # "Para cada término de aspecto, determine si el sentimiento es [positivo, negativo, neutral]. "
                "Por favor, identifique los términos de aspecto mencionados en el siguiente texto dado. Para cada término de aspecto, determine si el sentimiento es [positive, negative, neutral]. Devuelva el resultado en formato JSON solo con las claves 'aspect' y 'sentimiento'. "
                f"Texto: '{sentence}'."
            )
        elif args.lang == 'nl':
            prompt = (
                # "Identificeer de aspect-termen die in de onderstaande gegeven tekst worden genoemd. "
                # "Bepaal voor elk aspect-term of het sentiment [positief, negatief, neutraal] is. "
                "Identificeer de aspect-termen die in de onderstaande gegeven tekst worden genoemd. Bepaal voor elk aspect-term of het sentiment [positive, negative, neutral] is. Geef het resultaat terug in JSON-indeling met alleen de sleutels 'aspect' en 'sentiment'. "
                f"Tekst: '{sentence}'."
            )
        elif args.lang == 'ru':
            prompt = (
                # "Пожалуйста, определите аспектные термины, упомянутые в приведённом ниже тексте. "
                # "Для каждого аспектного термина определите, является ли настроение [положительным, отрицательным, нейтральным]. "
                "Пожалуйста, определите аспектные термины, упомянутые в приведённом ниже тексте. Для каждого аспектного термина определите, является ли настроение [positive, negative, neutral]. Верните результат в формате JSON, используя только ключи 'aspect' и 'sentiment'."
                f"Текст: '{sentence}'."
            )

        # Preparing input for the model
        messages = [{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}]
        
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = tokenizer([text], return_tensors="pt").to(device)

        # Generate the response from the model
        generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512, do_sample=False, temperature=0.0)

        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]

        # Decode and get the generated response
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(response)

        # Add the result to the list
        results.append({
            "sentence": sentence,
            "result": response
        })

    # Save the results to a JSON file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    print(f"Results saved to {output_json_path}")

file_path = f"data/{args.type}/{args.test_lang}/test.txt"
output_json_path = f"data/{args.type}/{args.test_lang}/triplet_qwen_zeroshot_results_{args.test_lang}.json"

analyze_sentiments(file_path, output_json_path)
