import json
import pandas as pd
import re
import logging
import os
from constant import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Converter:
    def __init__(self, json_file_path, output_excel_path):
        self.json_file_path = json_file_path
        self.output_excel_path = output_excel_path

    def clean_text(self, text):
        if not isinstance(text, str):
            return text
        # Remove escape characters and unicode symbols
        text = re.sub(r'\\[nrt]', ' ', text)  # replaces \n, \r, \t with space
        text = re.sub(r'\\u[0-9a-fA-F]{4}', ' ', text)  # remove unicode like \u2022
        text = re.sub(r'[^\x20-\x7E]', ' ', text)  # remove non-ASCII including emojis
        text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces
        return text.strip()

    def json_to_excel(self):
        logging.info("Starting JSON to Excel conversion.")
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logging.info(f"Loaded {len(data)} records from {self.json_file_path}")
        except Exception as e:
            logging.error(f"Failed to load JSON file: {e}")
            return

        cleaned_data = []
        for i, entry in enumerate(data):
            cleaned_entry = {k: self.clean_text(v) for k, v in entry.items()}
            cleaned_data.append(cleaned_entry)
        logging.info("Finished cleaning data.")

        try:
            df = pd.DataFrame(cleaned_data)
            df.to_excel(self.output_excel_path, index=False)
            logging.info(f"Excel file successfully saved to {self.output_excel_path}")
        except Exception as e:
            logging.error(f"Failed to write Excel file: {e}")



if __name__ == "__main__":
    json_file_path = ConverterConstants.JSON_INPUT_PATH  # Path to your JSON file
    output_excel_path = ConverterConstants.EXCEL_SAVE_PATH  # Path to save the Excel file

    converter = Converter(json_file_path, output_excel_path)
    converter.json_to_excel()

