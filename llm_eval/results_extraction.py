import re
import json
import os

mode = "uabsa" # TODO: select from ["uabsa", "tasd"]

# Improved regular expression to match multiple dictionary structures and allow spaces, line breaks, etc.

if mode == "uabsa":
    # Improved regular expression to match multiple dictionary structures and allow spaces, line breaks, etc.
    entity_sentiment_regex = re.compile(r'\{\s*"entity":\s*"(?P<entity>.*?)",\s*"sentiment":\s*"(?P<sentiment>.*?)"\s*\}')

    def extract_entities_and_sentiments(result):
        """Extract entity and sentiment from the result using regular expressions, supporting a list of multiple dictionaries."""
        if result.strip() == "[]":
            return []  # If it's an empty list, return an empty list directly
        else:
            matches = entity_sentiment_regex.findall(result)
            return [{"entity": entity, "sentiment": sentiment} for entity, sentiment in matches]
elif mode == "tasd":
    entity_sentiment_regex = re.compile(
        r'\{\s*"entity":\s*"(?P<entity>.*?)",\s*"category":\s*"(?P<category>.*?)",\s*"sentiment":\s*"(?P<sentiment>.*?)"\s*\}'
    )

    def extract_entities_and_sentiments(result):
        """Extract entity and sentiment from the result using regular expressions, supporting a list of multiple dictionaries."""
        if result.strip() == "[]":
            return []  # If it's an empty list, return an empty list directly
        else:
            matches = entity_sentiment_regex.findall(result)
            return [{"entity": entity, "category": category, "sentiment": sentiment} for entity, category, sentiment in matches]

def process_data(data):
    """Iterate through the data and extract or correct the result field."""
    for item in data:
        result = item.get("result", "")

        # Extract information using regular expressions
        extracted = extract_entities_and_sentiments(result)

        if extracted or extracted == []:  # If extraction is successful, update the result field
            item["result"] = extracted
        else:
            # If extraction fails, prompt the user to manually input the result
            print(f"\n#####Failed to extract from 'result': {result}")
            corrected_result = input("Please enter the corrected result (a list of dicts with 'entity' and 'sentiment' or an empty list): ")
            try:
                # Attempt to parse the user input
                item["result"] = json.loads(corrected_result)
            except Exception as e:
                print(f"Failed to parse the corrected result: {e}")
                print("Skipping this item...\n")

    return data

def main():
    model = "mistral" # TODO: select from ["llama", "gemma", "mistral", "qwen"]
    for data_type in ["food", "coursera", "education", "hotel", "laptop", "phone", "res"]:
        for test_lang in ["en", "ar", "da", "de", "es", "fr", "hi", "hr", "id", "ja", "ko", "nl", "pt", "ru", "sk", "sv", "sw", "th", "tr", "vi", "zh"]:
            input_file = f"data/{data_type}/{test_lang}/triplet_{model}_zeroshot_results_{test_lang}.json"
            # Define file path
            output_file = f"data_processed/{data_type}/{test_lang}/triplet_{model}_zeroshot_results_{test_lang}_processed.json"
            # Get directory path
            output_dir = os.path.dirname(output_file)
            # Check and create directory (if not existing)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Confirm that the input file exists
            if not os.path.exists(input_file):
                print(f"Error: The file '{input_file}' does not exist.")
                return

            try:
                # Read data from the input file
                with open(input_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error reading the input file: {e}")
                return

            # Process data
            processed_data = process_data(data)
            output_dir = os.path.dirname(output_file)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            try:
                # Write the processed data to the output file
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(processed_data, f, ensure_ascii=False, indent=4)
                print(f"\nProcessing completed. Data saved to '{output_file}'.")
            except Exception as e:
                print(f"Error writing to the output file: {e}")

if __name__ == "__main__":
    main()
