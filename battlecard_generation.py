import json
import time
import google.generativeai as genai
import os

# Set your Gemini API key here (consider using environment variables for security)
GEMINI_API_KEY = 'Your Gemini API Key'

class BattlecardGenerationModule:
    def __init__(self, competitor_profiles_file, product_info_file):
        self.competitor_profile = self.load_json(competitor_profiles_file)
        self.product_info = self.load_json(product_info_file)

        # Debugging output to confirm correct loading
        #print("Loaded Product Info:", self.product_info)  
        #print("Loaded Competitor Profile:", self.competitor_profile)  

        genai.configure(api_key=GEMINI_API_KEY)  # Configure API key

    def load_json(self, file_path):
        """Load JSON data from a file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            raise
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {file_path}.")
            raise

    def make_gemini_request(self, prompt):
        """Make a request to Gemini's API."""
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')  # Specify the model
            response = model.generate_content(prompt)  # Call generate_content method
            return response.text.strip()  # Adjust based on response structure
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def generate_battlecard(self):
        """Generate a battlecard using Gemini based on product and competitor profiles."""
        prompt, competitor_name = self.create_battlecard_prompt()  # Get both prompt and competitor name
        return self.make_gemini_request(prompt), competitor_name  # Return both

    def create_battlecard_prompt(self):
        """Create a prompt for Gemini to generate a battlecard."""
        
        # Accessing own product info
        own_product_data = self.product_info.get("competitors", {}).get("Zara", {})
        own_product_name = own_product_data.get("name", "Unknown Product")
        own_keywords = ", ".join(own_product_data.get("keywords", []))
        own_features = ", ".join(own_product_data.get("key_features", []))

        # Accessing competitors correctly
        competitors = self.competitor_profile.get("competitors")
        
        if competitors is None:
            raise KeyError("'competitors' key not found in competitor profiles data")
        
        # Assuming there's only one competitor in this case
        competitor_name, competitor_data = next(iter(competitors.items()))
        
        competitor_keywords = ", ".join(competitor_data.get("keywords", []))
        competitor_features = ", ".join(competitor_data.get("key_features", []))

        # Debugging output to confirm values before constructing prompt
        #print(f"Own Product: {own_product_name}, Keywords: {own_keywords}, key_features: {own_features}")
        #print(f"Competitor Name: {competitor_name}, Keywords: {competitor_keywords}, key_features: {competitor_features}")

        prompt = (f"Our product '{own_product_name}' has the following keywords: {own_keywords} and following key features: {own_features}. "
                  f"Compare our product with the following competitor:\n\nCompetitor '{competitor_name}' has the following keywords: "
                  f"{competitor_keywords} and the following key features: {competitor_features}.\n\n"
                  f"Highlight the differences and suggest key selling points for why our product is a better choice.")
        
        return prompt, competitor_name

    def save_battlecard(self, battlecard_content, competitor_name, output_file):
        """Save the generated battlecard content to a JSON file with competitor name as the key."""
        with open(output_file, 'w') as f:
            json.dump({competitor_name: battlecard_content}, f, indent=4)
        print(f"Battlecard for {competitor_name} saved to {output_file}")


if __name__ == '__main__':
    competitor_profiles_file = 'analyzed_data.json'
    product_info_file = 'own_product_info.json'

    battlecard_generator = BattlecardGenerationModule(competitor_profiles_file, product_info_file)

    battlecard_content, competitor_name = battlecard_generator.generate_battlecard()
    battlecard_generator.save_battlecard(battlecard_content, competitor_name, 'battlecards.json')
