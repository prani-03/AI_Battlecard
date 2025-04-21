import json
import spacy
from collections import defaultdict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

class DataAnalysisModule:
    def __init__(self, data_file):
        # Load collected raw data from JSON file
        try:
            with open(data_file, 'r') as f:
                self.data = json.load(f)
            print(f"Data loaded successfully from {data_file}.")
        except Exception as e:
            print(f"Error loading data file {data_file}: {e}")
            self.data = {}

    def analyze_text(self, text):
        """
        Analyzes the given text using spaCy to extract named entities.
        Returns a dictionary of entities categorized by their types.
        """
        doc = nlp(text)
        entities = defaultdict(list)
        for ent in doc.ents:
            entities[ent.label_].append(ent.text)
        return entities

    def process_competitor_data(self, competitor_data):
        """
        Processes competitor data by extracting key features, strengths, and 
        generating summaries from Google search results.
        """
        profiles = {}
        for competitor, search_results in competitor_data.items():
            profile = {
                'name': competitor,
                'keywords': [],  # To hold important keywords
                'summary': "",   # To summarize Google search results
                'entities': {},  # To hold extracted named entities
                'key_features': [],  # To hold key features
                'key_strengths': []   # To hold key strengths
            }

            # Process each Google search result for the competitor
            for result in search_results.get('google_results', []):
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                link = result.get('link', '')

                # Add the summary
                if title or snippet:  # Check if there's content to process
                    profile['summary'] += f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n\n"

                    # Extract keywords (named entities)
                    entities = self.analyze_text(f"{title} {snippet}")

                    # Add entities to profile and collect keywords
                    for entity_type, entity_list in entities.items():
                        if entity_type not in profile['entities']:
                            profile['entities'][entity_type] = []
                        profile['entities'][entity_type].extend(entity_list)
                        profile['keywords'].extend(entity_list)

                    # Heuristic to identify features and strengths
                    if "innovating" in snippet or "best" in snippet or "first" in snippet:
                        profile['key_strengths'].append(snippet)
                    else:
                        profile['key_features'].append(snippet)

            # Remove duplicates from keywords, features, and strengths
            profile['keywords'] = list(set(profile['keywords']))
            profile['key_features'] = list(set(profile['key_features']))
            profile['key_strengths'] = list(set(profile['key_strengths']))
            
            for entity_type in profile['entities']:
                profile['entities'][entity_type] = list(set(profile['entities'][entity_type]))

            profiles[competitor] = profile

        return profiles

    def analyze_data(self):
        """
        Analyzes the collected data to extract competitor and industry trend insights.
        """
        analyzed_data = {}

        # Process competitor data
        competitors_data = self.data.get('competitors', {})
        if competitors_data:
            try:
                analyzed_data['competitors'] = self.process_competitor_data(competitors_data)
            except Exception as e:
                print(f"Error processing competitors: {e}")
        else:
            print("No competitor data found in collected_data.json")

        # Process industry trends data (optional, depending on your needs)
        trends_data = self.data.get('industry_keywords', {})
        if trends_data:
            try:
                analyzed_data['industry_keywords'] = self.process_competitor_data(trends_data)
            except Exception as e:
                print(f"Error processing industry trends: {e}")
        else:
            print("No industry keyword data found in collected_data.json")

        return analyzed_data

if __name__ == '__main__':
    data_file = 'collected_data.json'

    # Initialize the analysis module
    analysis_module = DataAnalysisModule(data_file)

    # Analyze the data
    analyzed_data = analysis_module.analyze_data()

    # Output the analyzed data to analyzed_data.json
    try:
        with open('analyzed_data.json', 'w') as f:
            json.dump(analyzed_data, f, indent=4)
        print("Data analysis complete. Check analyzed_data.json for results.")
    except Exception as e:
        print(f"Error writing analyzed_data.json: {e}")
