import os
from app.pdf_ocr import PDFOCRProcessor

def main():
    try:
        processor = PDFOCRProcessor()
        pdf_url = "https://arxiv.org/pdf/2201.04234.pdf"  # Example PDF URL
        markdown_output = processor.process_pdf_url(pdf_url)
        print("Markdown Output from URL:")
        print(markdown_output)

        # For testing uploaded PDF, you would need a local PDF file
        # For now, let's just test URL processing

        print("\\nLog file content after processing:")
        with open(processor.log_file_path, 'r') as log_file:
            print(log_file.read())

    except Exception as e:
        print(f"Error during OCR processing: {e}")

if __name__ == "__main__":
    main()
