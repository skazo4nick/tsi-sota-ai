import os
from mistralai import Mistral
import json
from datetime import datetime

class PDFOCRProcessor:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
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

    def download_mistral_md(self, local_file_path: str):
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
            base_name = os.path.splitext(os.path.basename(local_file_path))[0]
            target_file_name = base_name + "-mistral.md"
            md_dir = "app/data/md"
            os.makedirs(md_dir, exist_ok=True)
            target_file_path = os.path.join(md_dir, target_file_name)
            with open(target_file_path, "w") as f:
                f.write(markdown_content)
            log_entry = {
                "source_file_path": local_file_path,
                "mistral_file_id": uploaded_pdf.id,
                "signed_url": signed_url_response.url,
                "target_file_path": target_file_path,
                "timestamps": {
                    "start_upload": start_time.isoformat(),
                    "upload_complete": datetime.now().isoformat(),
                    "start_processing": datetime.now().isoformat(),
                    "end_processing": datetime.now().isoformat()
                },
                "status": "success"
            }
            self._append_log_data(log_entry)
            return target_file_path
        except Exception as e:
            error_log_entry = {
                "source_file_path": local_file_path,
                "mistral_file_id": None,
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

    def upload_and_process_pdf(self, local_file_path: str) -> str:
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
    
            log_entry = {
                "source_file_path": local_file_path,
                "mistral_file_id": uploaded_pdf.id,
                "signed_url": signed_url_response.url,
                "target_file_path": None,
                "timestamps": {
                    "start_upload": start_time.isoformat(),
                    "upload_complete": datetime.now().isoformat(),
                    "start_processing": datetime.now().isoformat(),
                    "end_processing": datetime.now().isoformat()
                },
                "status": "success"
            }
            self._append_log_data(log_entry)
            return signed_url_response.url
        except Exception as e:
            error_log_entry = {
                "source_file_path": local_file_path,
                "mistral_file_id": None,
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

    def download_md_from_signed_url(self, signed_url: str) -> str:
        try:
            ocr_response = self.client.ocr.process(
                model="mistral-ocr-latest",
                document={"type": "document_url", "document_url": signed_url},
                include_image_base64=False
            )
            markdown_content = ""
            for page in ocr_response.pages:
                markdown_content += page.markdown + "\n\n"
            return markdown_content
        except Exception as e:
            raise

    def download_and_log_md(self, source_file_path: str, signed_url: str) -> str:
        try:
            md_content = self.download_md_from_signed_url(signed_url)
            base_name = os.path.splitext(os.path.basename(source_file_path))[0]
            target_file_name = base_name + "-mistral.md"
            md_dir = "app/data/md"
            os.makedirs(md_dir, exist_ok=True)
            target_file_path = os.path.join(md_dir, target_file_name)
            with open(target_file_path, "w") as f:
                f.write(md_content)
            log_data = self._load_log_data()
            updated = False
            for record in log_data:
                if record.get("source_file_path") == source_file_path and record.get("target_file_path") is None:
                    record["target_file_path"] = target_file_path
                    record["download_status"] = "success"
                    record["download_timestamp"] = datetime.now().isoformat()
                    updated = True
                    break
            if updated:
                with open(self.log_file_path, "w") as f:
                    json.dump(log_data, f, indent=4)
            return target_file_path
        except Exception as e:
            log_data = self._load_log_data()
            updated = False
            for record in log_data:
                if record.get("source_file_path") == source_file_path and record.get("target_file_path") is None:
                    record["download_status"] = "error"
                    record["download_timestamp"] = datetime.now().isoformat()
                    record["download_error_details"] = str(e)
                    updated = True
                    break
            if updated:
                with open(self.log_file_path, "w") as f:
                    json.dump(log_data, f, indent=4)
            raise
