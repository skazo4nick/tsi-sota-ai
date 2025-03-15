import os
from mistralai import Mistral
import json
from datetime import datetime

class PDFOCRProcessor:
    def __init__(self):
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("Mistral API key not found in environment variables.")
        self.client = Mistral(api_key=self.api_key)
        self.log_file_path = "app/system_data/ocr_processed_files.json"

    def _load_log_data(self):
        try:
            with open(self.log_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def _append_log_data(self, log_entry):
        log_data = self._load_log_data()
        log_data.append(log_entry)
        with open(self.log_file_path, 'w') as f:
            json.dump(log_data, f, indent=4)

    def process_pdf_url(self, document_url: str):
        start_time = datetime.now()
        try:
            ocr_response = self.client.ocr.process(
                model="mistral-ocr-latest",
                document={"type": "document_url", "document_url": document_url},
                include_image_base64=False # To reduce response size, not needed for markdown text
            )
            markdown_content = ""
            for page in ocr_response.pages:
                markdown_content += page.markdown + "\n\n"

            log_entry = {
                "source_file_path": document_url,
                "mistral_file_id": None, # Not applicable for URL processing
                "signed_url": document_url, # Using URL as identifier
                "target_file_path": None, # Target path can be determined later if needed
                "timestamps": {
                    "start_processing": start_time.isoformat(),
                    "end_processing": datetime.now().isoformat()
                },
                "status": "success"
            }
            self._append_log_data(log_entry)
            return markdown_content
        except Exception as e:
            error_log_entry = {
                "source_file_path": document_url,
                "mistral_file_id": None,
                "signed_url": document_url,
                "target_file_path": None,
                "timestamps": {
                    "start_processing": start_time.isoformat(),
                    "end_processing": datetime.now().isoformat()
                },
                "status": "error",
                "error_details": str(e)
            }
            self._append_log_data(error_log_entry)
            raise

    def process_uploaded_pdf(self, local_file_path: str):
        start_time = datetime.now()
        try:
            with open(local_file_path, "rb") as file_content:
                uploaded_pdf = self.client.files.upload(
                    file={"file_name": os.path.basename(local_file_path), "content": file_content},
                    purpose="ocr"
                )
            signed_url_response = self.client.files.get_signed_url(file_id=uploaded_pdf.id)

            ocr_response = self.client.ocr.process(
                model="mistral-ocr-latest",
                document={"type": "document_url", "document_url": signed_url_response.url},
                include_image_base64=False
            )
            markdown_content = ""
            for page in ocr_response.pages:
                markdown_content += page.markdown + "\n\n"

            log_entry = {
                "source_file_path": local_file_path,
                "mistral_file_id": uploaded_pdf.id,
                "signed_url": signed_url_response.url,
                "target_file_path": None, # Target path can be determined later
                "timestamps": {
                    "start_upload": start_time.isoformat(),
                    "upload_complete": datetime.now().isoformat(),
                    "start_processing": datetime.now().isoformat(), # Processing starts after upload
                    "end_processing": datetime.now().isoformat()
                },
                "status": "success"
            }
            self._append_log_data(log_entry)
            return markdown_content

        except Exception as e:
            error_log_entry = {
                "source_file_path": local_file_path,
                "mistral_file_id": None, # Error occurred before upload or during processing
                "signed_url": None,
                "target_file_path": None,
                "timestamps": {
                    "start_upload": start_time.isoformat(),
                    "end_processing": datetime.now().isoformat()
                },
                "status": "error",
                "error_details": str(e)
            }
            self._append_log_data(error_log_entry)
            raise
