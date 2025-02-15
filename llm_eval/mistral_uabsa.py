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



model_id = "mistralai/Mistral-7B-Instruct-v0.3"

# Load the model with a specified cache directory
model = AutoModelForCausalLM.from_pretrained(model_id, cache_dir="TODO", torch_dtype=torch.bfloat16, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir="TODO")


chatbot = pipeline("text-generation", model=model, tokenizer=tokenizer)

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

def analyze_sentiments(file_path, output_json_path):
    sentences = read_sentences_from_file(file_path)
    results = []

    for sentence in sentences:
        print('Testing sentence：' + sentence)
        if args.lang=='en':
            messages = [
                {
                    "role": "user",
                    "content": (
                        # "Given a sentence and an aspect-term label set {positive, negative, neutral}, your task is to:\n"
                        # "1.Identify the aspect-terms present in the sentence.\n 2.For each identified aspect-term, assign one of the following labels: [positive, negative, neutral].\n 3.Output the result in the JSON format.\n"
                        # f"Text: '{sentence}'."
                    # "Please identify the aspect-terms mentioned in the following given text. For each aspect-term, determine whether the sentiment is [positive, negative, neutral]. Return the result in a JSON format only with 'aspect' and 'sentiment' as keys."                   
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

Please return the final (not code) output based on the following text in json format.
'''
                    f"Text: '{sentence}'."

                    ),
                }
            ]
        if args.lang=='fr':
            messages = [
                {
                    "role": "user",
                    "content": (
                        # "Étant donné une phrase et un ensemble d'étiquettes de termes d'aspect {positif, négatif, neutre}, votre tâche est de:\n"
                        # "1.Identifier les termes d’aspect présents dans la phrase.\n 2.Pour chaque terme d’aspect identifié, attribuez une des étiquettes suivantes : [positif, négatif, neutre].\n 3.Produire le résultat au format JSON.\n"
                        # f"Text: '{sentence}'."
                    "Veuillez identifier les termes d’aspect mentionnés dans le texte donné ci-dessous. Pour chaque terme d’aspect, déterminez si le sentiment est [positive, negative, neutral]. Retournez le résultat au format JSON uniquement avec les clés 'aspect' et 'sentiment'."                   
                    f"Texte : '{sentence}'."

                    ),
                }
            ]
        if args.lang=='es':
            messages = [
                {
                    "role": "user",
                    "content": (
                        # "Dada una oración y un conjunto de etiquetas de términos de aspecto {positivo, negativo, neutral}, tu tarea es:\n"
                        # "1.Identificar los términos de aspecto presentes en la oración.\n 2.Para cada término de aspecto identificado, asignar una de las siguientes etiquetas: [positivo, negativo, neutral].\n 3.Salida del resultado en formato JSON.\n"
                        # f"Text: '{sentence}'."
                     "Por favor, identifique los términos de aspecto mencionados en el siguiente texto dado. Para cada término de aspecto, determine si el sentimiento es [positive, negative, neutral]. Devuelva el resultado en formato JSON solo con las claves 'aspect' y 'sentimiento'."                   
                    f"Texto: '{sentence}'."

                    ),
                }
            ]
        if args.lang=='nl':
            messages = [
                {
                    "role": "user",
                    "content": (
                        # "Gegeven een zin en een set labels voor aspect-termen {positief, negatief, neutraal}, is je taak om:\n"
                        # "1.Identificeer de aspect-termen die aanwezig zijn in de zin.\n 2.Wijs voor elke geïdentificeerde aspect-term een van de volgende labels toe: [positief, negatief, neutraal].\n 3.Geef het resultaat in JSON-indeling.\n"
                        # f"Text: '{sentence}'."
                     "Identificeer de aspect-termen die in de onderstaande gegeven tekst worden genoemd. Bepaal voor elk aspect-term of het sentiment [positive, negative, neutral] is. Geef het resultaat terug in JSON-indeling met alleen de sleutels 'aspect' en 'sentiment'"                   
                    f"Tekst: '{sentence}'."

                    ),
                }
            ]
        if args.lang=='ru':
            messages = [
                {
                    "role": "user",
                    "content": (
                        # "Дано предложение и набор меток аспектных терминов {положительный, отрицательный, нейтральный}, ваша задача:\n"
                        # "1.Определите термины аспекта, присутствующие в предложении.\n 2.Для каждого определённого термина аспекта назначьте один из следующих ярлыков: [положительный, отрицательный, нейтральный].\n 3.Выведите результат в формате JSON.\n"
                        # f"Text: '{sentence}'."
                     "Пожалуйста, определите аспектные термины, упомянутые в приведённом ниже тексте. Для каждого аспектного термина определите, является ли настроение [positive, negative, neutral]. Верните результат в формате JSON, используя только ключи 'aspect' и 'sentiment'."                   
                    f" Текст: '{sentence}'."

                    ),
                }
            ]
       
        outputs = chatbot(messages, max_new_tokens=512, do_sample=False)

        generated_text = outputs[0]["generated_text"][1]["content"]
        print(generated_text)

        results.append({
            "sentence": sentence,
            "result": generated_text
        })

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    print(f"Results saved {output_json_path}")

file_path = f"data/{args.type}/{args.test_lang}/test.txt"
output_json_path = f"data/{args.type}/{args.test_lang}/mistral_zeroshot_results_{args.test_lang}.json"

analyze_sentiments(file_path, output_json_path)

