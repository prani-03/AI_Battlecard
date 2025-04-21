import streamlit as st
import json
import os
from data_collection import DataCollectionModule  # Your data collection module
from data_analysis import DataAnalysisModule      # Your data analysis module
from battlecard_generation import BattlecardGenerationModule  # Your battlecard generation module
from battlecard_design import BattlecardDesignModule  # Your battlecard design module

def main():
    st.title("Battlecard Generation for EcoTex Fabric")

    # Competitor Selection
    st.header("Select Competitor")
    competitors = ['Nike', 'Adidas', 'H&M', 'Zara', 'Levi Strauss & Co.']
    selected_competitor = st.selectbox("Choose a Competitor", competitors)

    # Fixed Product Information
    product_name = "EcoTex Fabric"
    key_features = ["Eco-friendly materials", "Durable", "Comfortable"]
    strengths = ["Sustainable production", "Competitive pricing"]

    # Button to trigger data collection and analysis
    if st.button("Generate Battlecard"):
        with st.spinner("Collecting data..."):
            # Collect data for the selected competitor
            data_collector = DataCollectionModule([selected_competitor], ['Textile Manufacturing'])
            collected_data = data_collector.collect_data()

            # Save collected data to JSON file
            with open('collected_data.json', 'w') as f:
                json.dump(collected_data, f, indent=4)

            st.success("Data collection complete!")

        with st.spinner("Analyzing data..."):
            # Analyze the collected data
            analysis_module = DataAnalysisModule('collected_data.json')
            analyzed_data = analysis_module.analyze_data()

            # Save analyzed data to JSON file
            with open('analyzed_data.json', 'w') as f:
                json.dump(analyzed_data, f, indent=4)

            st.success("Data analysis complete!")

        with st.spinner("Generating battlecards..."):
            competitor_profiles_file = 'analyzed_data.json'
            product_info_file = 'own_product_info.json'

            battlecard_generator = BattlecardGenerationModule(competitor_profiles_file, product_info_file)

            battlecards = battlecard_generator.create_battlecards(batch_size=2)
            battlecard_generator.save_battlecards(battlecards, 'battlecards.json')


            # Generate battlecards based on analyzed data
            #battlecard_generator = BattlecardGenerationModule('analyzed_data.json', {
                #"product_name": product_name,
                #"key_features": key_features,
                #"strengths": strengths
            #})
            
            #battlecards = battlecard_generator.create_battlecards()
            
            # Save the generated battlecards to a JSON file
            #battlecard_generator.save_battlecards(battlecards, 'battlecards.json')

            st.success("Battlecards generated successfully!")

        with st.spinner("Designing PDFs..."):
            # Design the PDFs for each battlecard
            design_module = BattlecardDesignModule('battlecards.json')
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

if __name__ == "__main__":
    main()