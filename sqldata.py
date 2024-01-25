# # """ 
# # UID:string
# # NAME:string
# # Score: integer
# # Country:  ISO 2 letter code
# # timestamp: string
# # """
## From i will create the 10000 entries and load them into the database using Mysql



import csv
import random
from datetime import datetime, timedelta

def generate_data(num_entries):
    data_list = []
    countries = ["US", "CA", "UK", "IN", "AU", "JP", "FR", "DE", "BR", "MX"]

    for _ in range(num_entries):
        uid = ''.join(random.choice('0123456789ABCDEF') for i in range(8))  # Generate a random UID
        name = 'User' + str(random.randint(1, 20000))  # Generate a random username
        score = random.randint(0, 100)  # Generate a random score
        country = random.choice(countries)  # Choose a random country code
        timestamp = (datetime.now() - timedelta(days=random.randint(1, 10))).strftime('%Y-%m-%d %H:%M:%S')  # Generate a random timestamp within the last year

        data = {
            'uid': uid,
            'name': name,
            'score': score,
            'country': country,
            'timestamp': timestamp
        }

        data_list.append(data)

    return data_list

# Generate data for 10,000 entries
generated_data = generate_data(10000)

# Specify the CSV file path
csv_file_path = "dataOutputfile.csv"

# Writing data to CSV file
with open(csv_file_path, mode='w', newline='') as file:
    fieldnames = ['uid', 'name', 'score', 'country', 'timestamp']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data
    writer.writerows(generated_data)

print(f"Data has been written to {csv_file_path}")

