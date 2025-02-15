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
                # f"Please identify the aspect-terms mentioned in the following text. "
                # f"Please identify the aspect-terms mentioned in the following given text. For each aspect-term, determine whether the sentiment is [positive, negative, neutral]. Return the result in a JSON format only with 'aspect' and 'sentiment' as keys."
                '''
Aspect-Based Sentiment Analysis (ABSA) involves identifying specific entity (such as a person, product, service, or experience) mentioned in a text and determining the sentiment expressed toward each entity.

Each entity is associated with a sentiment that can be [positive, negative, or neutral].

Your task is to:

1. Identify the entity with a sentiment mentioned in the given text.
2. For each identified entity, determine the sentiment in the label set (positive, negative, or neutral).
3. The output should be a list of dictionaries, where each dictionary contains the entity with a sentiment and its corresponding sentiment. If there are no sentiment-bearing entities in the text, the output should be an empty list.

Example Output format:

[
  {"entity": "<entity>", "sentiment": "<label>"}
]

Please return the final (not code) output base on the following text in json format.
''' 
                f"Text: '{sentence}'."
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
output_json_path = f"data/{args.type}/{args.test_lang}/qwen_zeroshot_results_{args.test_lang}.json"

analyze_sentiments(file_path, output_json_path)