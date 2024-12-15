import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
import json
from datetime import datetime, timedelta



# CRUMPLE
# c.execute('''CREATE TABLE receipts (id TEXT, email TEXT, original BLOB, timestamp INT, metadata TEXT, items TEXT)''')

# Database of food items and their typical shelf lives (in days)
FOOD_DATABASE = {
    'milk': 7,
    'eggs': 21,
    'bread': 5,
    'cheese': 30,
    'chicken': 2,
    'beef': 3,
    'fish': 2,
    'yogurt': 14,
    'lettuce': 5,
    'apple': 30
}

# prepare image for ocr to read easier
def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.convert('L')  # grayscale for clarity
    image = image.filter(ImageFilter.SHARPEN)  # sharpen  image
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # increase contrast
    return image

# extract text from the image
def extract_text_from_image(image):
    custom_config = r'--oem 3 --psm 6'  # lstm ocr engine = automatic page segmentation
    text = pytesseract.image_to_string(image, config=custom_config) # convert to text
    return text

# get items and prices from the text
def extract_items_and_prices(text):
    item_pattern = r'\n(?:.*?)((?:\w+\s*){1,5})\s+(\d+\.\d{2})'  # pattern for item names and prices
    matches = re.findall(item_pattern, text)
    return matches

# Filter extracted items for food products
def filter_food_items(matches, food_database):
    food_items = []
    for item, price in matches:
        for food in food_database:
            if food.lower() in item.lower():
                food_items.append({
                    'item': item,
                    'price': float(price),
                    'expiry_date': (datetime.now() + timedelta(days=food_database[food])).strftime('%Y-%m-%d')
                })
    return food_items

# Save extracted food items to a JSON file
def save_to_json(food_items, output_file):
    with open(output_file, 'w') as f:
        json.dump(food_items, f, indent=4)

# Main function
def main(image_path, output_file):
    print("Processing receipt...")
    # Preprocess the image
    processed_image = preprocess_image(image_path)
    
    # Perform OCR
    text = extract_text_from_image(processed_image)
    print("Extracted Text:\n", text)
    
    # Extract items and prices
    matches = extract_items_and_prices(text)
    print("\nExtracted Items and Prices:\n", matches)
    
    # Filter for food items and calculate expiry dates
    food_items = filter_food_items(matches, FOOD_DATABASE)
    print("\nFiltered Food Items with Expiry Dates:\n", food_items)
    
    # Save food items to a JSON file
    save_to_json(food_items, output_file)
    print(f"\nFood items saved to {output_file}")

# Run the script
if __name__ == "__main__":
    # Path to the receipt image
    receipt_image_path = 'receipt3.jpg'
    # Output JSON file
    output_json_file = 'food_items.json'
    # Run the main function
    main(receipt_image_path, output_json_file)
