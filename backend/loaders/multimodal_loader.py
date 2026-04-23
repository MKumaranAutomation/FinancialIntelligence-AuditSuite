import os
import pandas as pd
from PIL import Image
import pdfplumber
import fitz  # PyMuPDF
from typing import List, Dict, Any, Union
import google.generativeai as genai
from dotenv import load_dotenv
from multiprocessing import Pool

load_dotenv()

def _extract_tables_from_page(args):
    """Worker function for multiprocessing table extraction."""
    file_path, page_index = args
    try:
        with pdfplumber.open(file_path) as pdf:
            page = pdf.pages[page_index]
            tables = page.extract_tables()
            return tables if tables else []
    except:
        return []

class MultiModalFinancialLoader:
    """
    Handles ingestion of various financial documents with multi-core performance.
    """
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')

    def load_document(self, file_path: str, deep_scan: bool = False) -> Dict[str, Any]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.pdf']:
            return self._process_pdf_optimized(file_path, deep_scan=deep_scan)
        elif ext in ['.jpg', '.jpeg', '.png', '.heic']:
            return self._process_image(file_path)
        return self._process_spreadsheet(file_path)

    def _process_pdf_optimized(self, file_path: str, deep_scan: bool = False) -> Dict[str, Any]:
        """
        High-performance hybrid PDF processing.
        """
        data = {"text": "", "tables": [], "metadata": {"source": file_path}}
        
        # 1. Instant Text Extraction (PyMuPDF) - Always runs
        with fitz.open(file_path) as doc:
            num_pages = len(doc)
            for page in doc:
                data["text"] += page.get_text() + "\n"
        
        # 2. Parallel Table Extraction (Multiprocessing) - Only if deep_scan is enabled
        if deep_scan:
            print(f"[*] Starting deep forensic scan for {num_pages} pages...")
            with Pool(processes=os.cpu_count()) as pool:
                args = [(file_path, i) for i in range(num_pages)]
                results = pool.map(_extract_tables_from_page, args)
                
                for table_list in results:
                    if table_list:
                        data["tables"].extend(table_list)
        else:
            print(f"[*] Standard scan complete (skipping tables for speed).")
                
        return data

    def _process_image(self, file_path: str) -> Dict[str, Any]:
        img = Image.open(file_path)
        prompt = "Analyze this financial image. Extract all text and key entities: Date, Vendor, Total."
        response = self.model.generate_content([prompt, img])
        return {"text": response.text, "metadata": {"source": file_path, "type": "image_analysis"}}

    def _process_spreadsheet(self, file_path: str) -> Dict[str, Any]:
        ext = os.path.splitext(file_path)[1].lower()
        df = pd.read_csv(file_path) if ext == '.csv' else pd.read_excel(file_path)
        return {"text": df.to_string(), "data": df.to_dict(orient='records'), "metadata": {"source": file_path, "type": "spreadsheet"}}

if __name__ == "__main__":
    # Test stub
    loader = MultiModalFinancialLoader()
    print("MultiModal Loader Initialized.")
