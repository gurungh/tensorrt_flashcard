import sys
import subprocess
from openai import OpenAI
import os
import csv
import re

# Function to generate items related to a category
def generate_category_items(category, n):
    OpenAI.api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI()

    # Constructing the prompt for GPT-4
    prompt = f"Please provide a comma-separated list of {n} real items in the category '{category}', that would be familiar and appealing for a child between the ages of 2 and 6.  Avoid fictional or toy tiems.  For example, if the category is 'Fruit' and we want three items, a good response would be [apple, pear, orange]"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=50,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        n=1
    )

    # Assuming the response is a comma-separated list of items
    items_str = response.choices[0].message.content
    items_str = re.sub(r'[^A-Za-z0-9 ,]+', '', items_str)
    items = [item.strip() for item in items_str.split(',')]
    items = [(category + " " + item) for item in items]
    
    return items

def generate_translations(descriptions, language):
    OpenAI.api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI()

    # Extract categories and words from descriptions
    categories = [desc.split(' ')[0] for desc in descriptions]
    words = [' '.join(desc.split(' ')[1:]) for desc in descriptions]

    # Constructing the prompt for translations
    prompt = f"Please provide a comma-separated list of the translations of these words {words} into {language}."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a bilingual expert fluent in English and {language}."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=100,  
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    # Parsing the translation response
    translation_str = response.choices[0].message.content
    translations = [trans.strip() for trans in translation_str.split(',')]

    romanization_prompt = f"Please provide a comma-separated list of the romanization of these words {translations}"
    rom_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a bilingual expert fluent in English and {language}."},
            {"role": "user", "content": romanization_prompt}
        ],
        temperature=0.5,
        max_tokens=50,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        n=1
    )
    # Assuming the response is a comma-separated list of items
    romanization_str = rom_response.choices[0].message.content
    romanizations = [rom.strip() for rom in romanization_str.split(',')]

    # Generating filenames and languages lists
    filenames = [(desc.replace(' ', '_') + ".png") for desc in descriptions]
    languages = [language] * len(descriptions)

    return categories, words, languages, translations, romanizations, filenames

def write_translations_to_csv(data):
    csv_file_name = 'output/translations.csv'
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(csv_file_name), exist_ok=True)

    # Open the CSV file for writing
    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)

        # Write the header row
        csvwriter.writerow(['Primary Language', 'Category', 'Primary Language Word', 'Learning Language', 'Translation', 'Romanization', 'Image File Name'])

        # Write data rows
        for item in data:
            csvwriter.writerow([
                item['Primary Language'], 
                item['Category'], 
                item['Word'], 
                item['Language'], 
                item['Translation'], 
                item['Romanization'],
                item['FileName']
    ])

if __name__ == "__main__":
    name = sys.argv[1]
    primary_language = sys.argv[2]
    learning_languages = sys.argv[3].split(',')
    categories = sys.argv[4].split(',')  # Split the string back into a list

    num_desc = 5
    all_data = []

    for category in categories:
        image_descriptions = generate_category_items(category, num_desc)

        for description in image_descriptions:
            command = ['python', '.\demo_txt2img.py', description]
            subprocess.run(command)  # Run the command

        for language in learning_languages:
            if language not in primary_language:
                categories, words, languages, translations, romanizations, file_names = generate_translations(image_descriptions, language)
                
                for i in range(len(words)):
                    data_item = {
                        'Primary Language': primary_language,
                        'Category': categories[i],
                        'Word': words[i],
                        'Language': languages[i],
                        'Translation': translations[i],
                        'Romanization': romanizations[i],
                        'FileName': file_names[i]
                    }
                    all_data.append(data_item)

    write_translations_to_csv(all_data)