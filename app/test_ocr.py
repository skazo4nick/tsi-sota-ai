import os
from dotenv import load_dotenv
load_dotenv()
from app.pdf_ocr import PDFOCRProcessor

def main():
    try:
        processor = PDFOCRProcessor()
        # Test the uploaded PDF workflow using the provided file path
        pdf_path = "/workspaces/tsi-sota-ai/app/data/pdfs/Port-Rotterdam-Inland-Container-Shipping-Guidelines..pdf"
        markdown_output = processor.process_uploaded_pdf(pdf_path)
        print("Markdown Output from Uploaded PDF:")
        print(markdown_output)

        print("\nLog file content after processing:")
        with open(processor.log_file_path, 'r') as log_file:
            print(log_file.read())

    except Exception as e:
        print(f"Error during OCR processing: {e}")

if __name__ == "__main__":
    main()
