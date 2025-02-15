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

def check_gpu_count():
    gpu_count = torch.cuda.device_count()
    if gpu_count > 0:
        print(f"{gpu_count} GPU(s) available:")
        for i in range(gpu_count):
            print(f" - GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("No GPU available.")

check_gpu_count()


model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

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

Please return the final output (not code) based on the following text in json format.
'''
                    f"Text: '{sentence}'."
                    ),
                }
            ]
       
        outputs = chatbot(messages, max_new_tokens=512,do_sample=False)

        generated_text = outputs[0]["generated_text"][1]["content"]
        print(generated_text)

        results.append({
            "sentence": sentence,
            "result": generated_text
        })

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    print(f"Results saved in {output_json_path}")


file_path = f"data/{args.type}/{args.test_lang}/test.txt"
output_json_path = f"data/{args.type}/{args.test_lang}/llama_zeroshot_results_{args.test_lang}.json"

analyze_sentiments(file_path, output_json_path)