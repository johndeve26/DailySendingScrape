import csv
import os

class SaveToCSV:
    def __init__(self, site, rough, date):
        self.date = date
        self.rough = rough
        self.site = site
        self.data = {}  # To store data for CSV formatting

    def read_file(self, file):
        filepath = f'{self.site}/{file}_{self.rough}_new.txt'

        # Check if the file exists; if not, create it
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write('')  # Create an empty file
            print(f'File "{file}.txt" created.')

        # Read data from the file
        with open(filepath, 'r') as f:
            data = [url.strip() for url in f.readlines() if url.strip()]  # Filter out empty lines

        self.data[file] = data  # Store data for this file

    def format_to_csv(self):
        # Create a directory for saving the CSV file if it doesn't exist
        directory = f'{self.site}/listing_CSV'
        os.makedirs(directory, exist_ok=True)

        # Define the CSV file path
        csv_file_path = os.path.join(directory, f'{self.site}_new_listings_for_{self.date}.csv')
        print(csv_file_path)

        # Write data to CSV
        with open(csv_file_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)

            # Write the header row
            csv_writer.writerow(['Keyword', 'URL'])

            # Write each URL with the corresponding keyword
            for keyword, urls in self.data.items():
                for url in urls:
                    csv_writer.writerow([keyword, url])

        print(f"Data saved successfully to {csv_file_path}")

    def get_terms(self):
        with open('search_terms.txt', 'r') as file:
            search_terms = [term.strip() for term in file.readlines()]
        return search_terms

    def save_to_csv(self):
        search_terms = self.get_terms()

        for each_term in search_terms:
            self.read_file(each_term)

        # Call format_to_csv after reading all terms
        self.format_to_csv()

# # Example usage
# if __name__ == '__main__':
#     sss = SaveToCSV('crexi')
#     sss.save_to_csv()
