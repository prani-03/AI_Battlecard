import streamlit as st
import os
import json
from data_collection import DataCollectionModule  # Import the class from the module
from data_analysis import DataAnalysisModule       # Import the class from the module
from battlecard_generation import BattlecardGenerationModule  # Import the class from the module
from battlecard_design import BattlecardDesignModule  # Import the class from the module
from streamlit_marquee import streamlit_marquee


# Define your product and competitor logos
your_product_logo = "zara.png"  # Replace with your logo path
competitor_logos = [
    {"name": "Nike", "logo": "nike.png"},  # Replace with competitor logo paths
    {"name": "Levis", "logo": "levis.png"},
    {"name": "H & M", "logo": "hm.png"},
    {"name": "Pantaloons", "logo": "pantaloons.png"},
    {"name": "Skechers", "logo": "skechers.png"},
    {"name": "Zudio", "logo": "zudio.png"},
]

# Set page config
st.set_page_config(layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
            font-family: TimesNewRoman, sans-serif;
        }
        .custom-container {
            width: 90%; /* Set desired width */
            margin: auto; /* Center the container */
        }
        .header {
            text-align: center;
            color: #333;
        }
        .logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 200px; /* Adjust width as needed */
        }
        .competitor-logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 150px; /* Adjust width as needed */
        }
        .info-area {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title of the app
st.title("Battlecard Creator")

# Display your product logo
st.header("Our Product")
st.image(your_product_logo, caption="Our Product Logo", output_format='PNG', width=500)

# Display competitor logos in a grid layout
st.header("Competitors")
cols = st.columns(len(competitor_logos))  # Create columns based on the number of competitors

for col, competitor in zip(cols, competitor_logos):
    with col:
        st.image(competitor["logo"], caption=competitor["name"], use_column_width='auto', output_format='PNG', width=150)

# Dropdown for selecting a competitor
competitor_names = [competitor["name"] for competitor in competitor_logos]
selected_competitor = st.selectbox("Select a Competitor", competitor_names)

# Display selected competitor logo
selected_competitor_logo = next((competitor["logo"] for competitor in competitor_logos if competitor["name"] == selected_competitor), None)

if selected_competitor_logo:
    st.image(selected_competitor_logo, caption=selected_competitor, output_format='PNG', width=200)

# Button to generate battlecard and integrate module functionality
if st.button("Generate Battlecard"):
    with st.spinner("Generating battlecard..."):
        try:
            # Step 1: Data Collection
            with st.spinner("Collecting data..."):
                collector = DataCollectionModule([selected_competitor], 'Textile Manufacturing')
                collected_data = collector.collect_data()

                # Save collected data to JSON file
                with open('collected_data.json', 'w') as f:
                    json.dump(collected_data, f, indent=4)

                st.success("Data collection complete!")
            
            # Step 2: Data Analysis
            with st.spinner("Analyzing data..."):
                data_file = 'collected_data.json'
                analyzer = DataAnalysisModule(data_file)
                analyzed_data = analyzer.analyze_data()

                # Save analyzed data to JSON file
                with open('analyzed_data.json', 'w') as f:
                    json.dump(analyzed_data, f, indent=4)

                st.success("Data analysis complete!")
            
            # Step 3: Generate Battlecard
            with st.spinner("Generating battlecards..."):
                competitor_profiles_file = 'analyzed_data.json'
                product_info_file = 'own_product_info.json'

                battlecard_generator = BattlecardGenerationModule(competitor_profiles_file, product_info_file)

                battlecard_content, competitor_name = battlecard_generator.generate_battlecard()
                battlecard_generator.save_battlecard(battlecard_content, competitor_name, 'battlecards.json')
                
                st.success("Battlecards generated successfully!")

            # Step 4: Design Battlecard
            with st.spinner("Designing PDFs..."):
                battlecards_file = 'battlecards.json'  # Ensure this file exists with correct structure
                design_module = BattlecardDesignModule(battlecards_file)
                design_module.generate_all_battlecards()

                st.success("PDFs designed successfully!")
            
            # Provide download links for the generated battlecards
            pdf_path = f'output/{selected_competitor}_battlecard.pdf'
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as pdf_file:
                    st.download_button(
                        label=f"Download Battlecard for {selected_competitor}",
                        data=pdf_file,
                        file_name=f"{selected_competitor}_battlecard.pdf",
                        mime='application/pdf'
                    )
            else:
                st.warning(f"No battlecard found for {selected_competitor}")
        
        except Exception as e:
            st.error(f"An error occurred while generating the battlecard: {e}")
