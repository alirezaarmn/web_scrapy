from xhtml2pdf import pisa
import requests

def convert_url_to_pdf(url, file_name): 
    # Fetch the HTML content from the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch URL: {url}")
        return False
    
    html_content = response.text
    
    # Generate PDF
    with open("{}.pdf".format(file_name), "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
        
    return not pisa_status.err

# # URL to fetch #TODO: unittest
# url_to_fetch = "http://10.0.0.69:3000/"

# # PDF path to save
# pdf_path = "google"

# # Generate PDF
# if convert_url_to_pdf(url_to_fetch, "google"):
#     print(f"PDF generated and saved at {pdf_path}")
# else:
#     print("PDF generation failed")