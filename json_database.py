import json

#TODO: page_id'yi notion so ya göre konrol et eğer yoksa json içersinden sil.

class JsonDatabase:
    def __init__(self, file_name):
        self.file_name = "Json/db/" + file_name
        try:
            with open(self.file_name, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {'pages': []}

    def write_data(self, page_id, normalized_name:str):
        # Check if the page_id already exists in the "pages" list
        if any(d['page_id'] == page_id for d in self.data['pages']):
            raise ValueError(f"page_id {page_id} already exists in the database.")

        # Append the new data as a dictionary to the "pages" list
        self.data['pages'].append({'page_id': page_id, 'normalized_name': normalized_name.lower()})

        # Write the data to the JSON file
        with open(self.file_name, 'w') as f:
            json.dump(self.data, f)

    def read_data(self):
        # Read and return the "pages" list from the JSON file
        return self.data['pages']

    def delete_data(self, page_id):
        # Remove the data with the given page_id from the "pages" list
        self.data['pages'] = [d for d in self.data['pages'] if d['page_id'] != page_id]

        # Write the data to the JSON file
        with open(self.file_name, 'w') as f:
            json.dump(self.data, f)

    def update_data(self, page_id, new_normalized_name:str):
        # Find the data with the given page_id in the "pages" list and update its normalized_name
        for d in self.data['pages']:
            if d['page_id'] == page_id:
                d['normalized_name'] = new_normalized_name.lower()

        # Write the data to the JSON file
        with open(self.file_name, 'w') as f:
            json.dump(self.data, f)

    def find_data(self, search_term:str):
        # Search for data by page_id or normalized_name
        results = []
        for d in self.data['pages']:
            if str(d['page_id']) == search_term or d['normalized_name'].lower() == search_term.lower():
                results.append(d)

        return results