
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class BattlecardDesignModule:
    def __init__(self, battlecards_file):
        self.battlecards = self.load_json(battlecards_file)

    def load_json(self, file_path):
        """Load JSON data from a file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"File {file_path} not found.")
        except json.JSONDecodeError:
            raise Exception(f"Error decoding JSON from file {file_path}")

    def generate_battlecard_pdf(self, competitor_name, battlecard_content, output_dir='output'):
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Define the output PDF file path
        output_pdf_path = os.path.join(output_dir, f"{competitor_name}_battlecard.pdf")

        # Create a PDF document
        doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
        elements = []

        # Get sample styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        normal_style = styles['Normal']
        heading_style = styles['Heading2']

        # Add title
        title = Paragraph(f"Battlecard: Zara vs {competitor_name}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 24))

        # Add content from battlecard without duplicates
        content_paragraphs = battlecard_content.split('\n\n')
        
        for paragraph in content_paragraphs:
            if paragraph.strip():  # Avoid adding empty paragraphs
                elements.append(Paragraph(paragraph.replace("\n", "<br/>"), normal_style))
                elements.append(Spacer(1, 12))

        # Create a comparison table based on key differences extracted from the content
        self.create_comparison_table(elements, battlecard_content)

        # Add Key Selling Points section dynamically
        self.add_key_selling_points(elements, battlecard_content)

        # Add Conclusion section dynamically based on content
        self.add_conclusion(elements, battlecard_content)

        # Build the PDF
        doc.build(elements)

        print(f"Battlecard for {competitor_name} saved as {output_pdf_path}")

    def create_comparison_table(self, elements, battlecard_content):
        # Extracting key differences section from battlecard content
        lines = battlecard_content.splitlines()
        
        # Initialize table data with headers
        table_data = [['Feature', 'Zara', 'Competitor']]

        # Parse lines to find key differences and populate table data
        for line in lines:
            if line.startswith('|'):
                parts = line.split('|')
                if len(parts) >= 4:  # Ensure there are enough parts to extract data
                    feature = parts[1].strip().replace('*', '')  # Remove '*' characters
                    zara_value = parts[2].strip().replace('*', '')  # Remove '*' characters
                    competitor_value = parts[3].strip().replace('*', '')  # Remove '*' characters
                    
                    # Wrap cell content in Paragraph for proper text wrapping
                    table_data.append([
                        Paragraph(feature, getSampleStyleSheet()['Normal']),
                        Paragraph(zara_value, getSampleStyleSheet()['Normal']),
                        Paragraph(competitor_value, getSampleStyleSheet()['Normal'])
                    ])

        # Set fixed column widths to fit within A4 size sheet
        col_widths = [100, 200, 200]  # Adjust column widths as necessary

        # Create the table without specifying row heights for dynamic adjustment
        table = Table(table_data, colWidths=col_widths)

        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('TEXTCOLOR', (1, 1), (2, -1), colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1,-1), 'TOP'),   # Align text to top of cell for better visibility
        ])
        
        table.setStyle(style)

        elements.append(Spacer(1, 24))  # Add some space before the table
        elements.append(table)  # Add the table to the PDF
        elements.append(Spacer(1, 24))  # Add space after the table

    def add_key_selling_points(self, elements, battlecard_content):
        """Add a visually appealing section for Key Selling Points."""
        
        key_selling_points_title = Paragraph("Key Selling Points for Zara", getSampleStyleSheet()['Heading2'])
        elements.append(key_selling_points_title)
        
        selling_points_section_start = False
        
        for line in battlecard_content.splitlines():
            if line.strip().startswith("**Key Selling Points for Zara:**"):
                selling_points_section_start = True
                continue
            
            if selling_points_section_start:
                if line.strip() == "":
                    continue
                
                if line.startswith("* "):  # Check for bullet points in markdown format
                    point = line.replace("* ", "").strip()
                    elements.append(Paragraph(point.replace("*", ""), getSampleStyleSheet()['Normal']))
                    elements.append(Spacer(1, 6))

    def add_conclusion(self, elements, battlecard_content):
        """Add a conclusion section at the end of each battlecard based on content."""
        
        conclusion_title = Paragraph("Conclusion", getSampleStyleSheet()['Heading2'])
        elements.append(conclusion_title)

        conclusion_points = []
        
        # Dynamically extract points that indicate why Zara is superior.
        lines = battlecard_content.splitlines()
        
        for line in lines:
            if "superior" in line or "better" in line or "best" in line:
                conclusion_points.append(line.strip())
        
        if conclusion_points:
            conclusion_text = "Based on our analysis: " + ", ".join(conclusion_points)
            elements.append(Paragraph(conclusion_text.replace("\n", "<br/>"), getSampleStyleSheet()['Normal']))
        
    def generate_all_battlecards(self):
        for competitor_name in self.battlecards.keys():
            if competitor_name != 'Zara':  # Assuming Zara is the main brand being compared
                print(f"Designing battlecard for {competitor_name}...")
                self.generate_battlecard_pdf(competitor_name, self.battlecards[competitor_name]) 

if __name__ == '__main__':
    battlecards_file = 'battlecards.json'  # Ensure this file exists with correct structure

    design_module = BattlecardDesignModule(battlecards_file)

    design_module.generate_all_battlecards()