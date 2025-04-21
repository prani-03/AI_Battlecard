import requests
import json

# API Keys
GOOGLE_API_KEY = 'AIzaSyDqaw_zTlrS1_sNG9H5QJjSbmk90HJVyQQ'
GOOGLE_CSE_ID = '915f47576a7e74432'

class DataCollectionModule:
    def __init__(self, competitors, industry_keywords):
        self.competitors = competitors
        self.industry_keywords = industry_keywords

    def google_search(self, query):
        url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}&q={query}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            results = response.json()
            return results.get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            return []

    def collect_data(self):
        collected_data = {
            'competitors': {},
            'industry_keywords': {}
        }

        # Search for competitors
        for competitor in self.competitors:
            collected_data['competitors'][competitor] = {
                'google_results': self.google_search(competitor),
            }

        # Search for industry trends
        for keyword in self.industry_keywords:
            collected_data['industry_keywords'][keyword] = {
                'google_results': self.google_search(keyword),
            }

        return collected_data

if __name__ == '__main__':
    # Example inputs specific to the textile industry
    competitors=['Nike']
    #competitors = ['Nike', 'Adidas', 'H&M', 'Zara', 'Levi Strauss & Co.']
    industry_keywords=['Textile Manufacturing']
    #industry_keywords = ['Textile Manufacturing', 'Sustainable Fabrics', 'Fashion Textiles', 'Textile Trends']

    data_collector = DataCollectionModule(competitors, industry_keywords)
    data = data_collector.collect_data()

    # Output the collected data
    with open('collected_data.json', 'w') as f:
        json.dump(data, f, indent=4)

    print("Data collection complete. Check collected_data.json for results.")