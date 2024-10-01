import csv
import random
import string

def generate_business_name():
    prefixes = ["A1", "Best", "Top", "Super", "Prime", "Elite", "Pro", "Expert", "Quality", "Reliable"]
    suffixes = ["Solutions", "Services", "Consulting", "Associates", "Group", "Company", "Enterprises", "Industries", "Systems", "Technologies"]
    name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
    if random.random() < 0.3:  # 30% chance to add a business entity type
        entities = ["Inc.", "LLC", "Ltd.", "Corp.", "Company"]
        name += f" {random.choice(entities)}"
    return name

def generate_address():
    street_numbers = [str(random.randint(100, 9999)) for _ in range(50)]
    street_names = ["Main", "Oak", "Pine", "Maple", "Cedar", "Elm", "Washington", "Park", "Lake", "Hill"]
    street_types = ["St", "Ave", "Blvd", "Rd", "Ln", "Dr", "Way", "Pl", "Ct", "Terrace"]
    return f"{random.choice(street_numbers)} {random.choice(street_names)} {random.choice(street_types)}"

def generate_zipcode():
    return f"{random.randint(10000, 99999)}"

def introduce_variation(text, variation_type):
    if variation_type == "typo":
        i = random.randint(0, len(text) - 1)
        return text[:i] + random.choice(string.ascii_letters) + text[i+1:]
    elif variation_type == "missing":
        i = random.randint(0, len(text) - 1)
        return text[:i] + text[i+1:]
    elif variation_type == "extra":
        i = random.randint(0, len(text))
        return text[:i] + random.choice(string.ascii_letters) + text[i:]
    return text

def generate_test_data(filename, num_records):
    businesses = []
    for _ in range(num_records):
        biz_name = generate_business_name()
        biz_addr = generate_address()
        biz_zipcode = generate_zipcode()
        
        # Introduce variations
        if random.random() < 0.2:  # 20% chance of name variation
            biz_name = introduce_variation(biz_name, random.choice(["typo", "missing", "extra"]))
        if random.random() < 0.2:  # 20% chance of address variation
            biz_addr = introduce_variation(biz_addr, random.choice(["typo", "missing", "extra"]))
        if random.random() < 0.1:  # 10% chance of zipcode variation
            biz_zipcode = introduce_variation(biz_zipcode, random.choice(["typo", "missing"]))
        
        businesses.append((biz_name, biz_addr, biz_zipcode))
    
    # Add some duplicates with variations
    num_duplicates = num_records // 10  # 10% duplicates
    for _ in range(num_duplicates):
        original = random.choice(businesses)
        duplicate = list(original)
        field_to_vary = random.randint(0, 2)
        duplicate[field_to_vary] = introduce_variation(duplicate[field_to_vary], random.choice(["typo", "missing", "extra"]))
        businesses.append(tuple(duplicate))
    
    # Write to CSV
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['biz_name', 'biz_addr', 'biz_zipcode'])
        for business in businesses:
            writer.writerow(business)

if __name__ == "__main__":
    output_file = "input_businesses.csv"
    num_records = 1000
    generate_test_data(output_file, num_records)
    print(f"Test data generated and saved to {output_file}")
    print(f"Number of records: {num_records}")
