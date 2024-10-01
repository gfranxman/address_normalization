import csv
import re
from fuzzywuzzy import fuzz
from usaddress import parse

def clean_business_name(name):
    # Convert to lowercase
    name = name.lower()
    # Remove punctuation and extra spaces
    name = re.sub(r'[^\w\s]', '', name)
    name = ' '.join(name.split())
    # Remove common business suffixes
    suffixes = ['inc', 'llc', 'ltd', 'corp']
    for suffix in suffixes:
        name = re.sub(r'\b' + suffix + r'\b', '', name)
    return name.strip()

def clean_address(address):
    # Parse address using usaddress library
    try:
        parsed_address = parse(address)
        # Extract relevant parts
        street_number = next((component[0] for component in parsed_address if component[1] == 'AddressNumber'), '')
        street_name = next((component[0] for component in parsed_address if component[1] == 'StreetName'), '')
        street_type = next((component[0] for component in parsed_address if component[1] == 'StreetNamePostType'), '')
        return f"{street_number} {street_name} {street_type}".strip()
    except:
        return address

def clean_zipcode(zipcode):
    # Extract first 5 digits of ZIP code
    match = re.search(r'\b\d{5}\b', zipcode)
    return match.group() if match else zipcode

def normalize_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['biz_name', 'biz_addr', 'biz_zipcode', 'normalized_name', 'normalized_addr', 'normalized_zipcode']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            normalized_row = {
                'biz_name': row['biz_name'],
                'biz_addr': row['biz_addr'],
                'biz_zipcode': row['biz_zipcode'],
                'normalized_name': clean_business_name(row['biz_name']),
                'normalized_addr': clean_address(row['biz_addr']),
                'normalized_zipcode': clean_zipcode(row['biz_zipcode'])
            }
            writer.writerow(normalized_row)

def find_duplicates(normalized_file, duplicate_file, threshold=80):
    businesses = []
    with open(normalized_file, 'r') as infile:
        reader = csv.DictReader(infile)
        businesses = list(reader)

    duplicates = []
    for i, biz1 in enumerate(businesses):
        for j, biz2 in enumerate(businesses[i+1:], start=i+1):
            name_similarity = fuzz.ratio(biz1['normalized_name'], biz2['normalized_name'])
            addr_similarity = fuzz.ratio(biz1['normalized_addr'], biz2['normalized_addr'])
            if name_similarity >= threshold and addr_similarity >= threshold and biz1['normalized_zipcode'] == biz2['normalized_zipcode']:
                duplicates.append((biz1, biz2))

    with open(duplicate_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Business 1', 'Business 2', 'Name Similarity', 'Address Similarity'])
        for biz1, biz2 in duplicates:
            writer.writerow([
                f"{biz1['biz_name']} | {biz1['biz_addr']} | {biz1['biz_zipcode']}",
                f"{biz2['biz_name']} | {biz2['biz_addr']} | {biz2['biz_zipcode']}",
                fuzz.ratio(biz1['normalized_name'], biz2['normalized_name']),
                fuzz.ratio(biz1['normalized_addr'], biz2['normalized_addr'])
            ])

if __name__ == "__main__":
    input_file = "input_businesses.csv"
    normalized_file = "normalized_businesses.csv"
    duplicate_file = "potential_duplicates.csv"

    normalize_data(input_file, normalized_file)
    find_duplicates(normalized_file, duplicate_file)

    print("Data normalization and duplicate detection complete.")
    print(f"Normalized data saved to: {normalized_file}")
    print(f"Potential duplicates saved to: {duplicate_file}")
