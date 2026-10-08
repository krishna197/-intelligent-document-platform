"""PDF document processor."""

import PyPDF2
from typing import Dict, Any
from .base import BaseDocumentProcessor
import logging

logger = logging.getLogger(__name__)


class PDFProcessor(BaseDocumentProcessor):
    """Processor for PDF documents."""

    def process(self, file_path: str) -> Dict[str, Any]:
        """Process a PDF document.

        Args:
            file_path: Path to the PDF file

        Returns:
            Dictionary containing extracted text and metadata
        """
        if not self.validate_file(file_path):
            raise ValueError(f"Invalid file: {file_path}")

        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                # Extract text from all pages
                text_content = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text_content += page.extract_text() + "\n"
                    except Exception as e:
                        logger.warning(f"Could not extract text from page {page_num}: {e}")

                # Extract metadata
                metadata = {}
                if pdf_reader.metadata:
                    metadata = {
                        'title': pdf_reader.metadata.get('/title', ''),
                        'author': pdf_reader.metadata.get('/author', ''),
                        'subject': pdf_reader.metadata.get('/subject', ''),
                        'creator': pdf_reader.metadata.get('/creator', ''),
                        'producer': pdf_reader.metadata.get('/producer', ''),
                        'creation_date': str(pdf_reader.metadata.get('/creation_date', '')),
                        'modification_date': str(pdf_reader.metadata.get('/modification_date', ''))
                    }

                result = {
                    'file_path': file_path,
                    'file_type': 'pdf',
                    'text_content': text_content.strip(),
                    'page_count': len(pdf_reader.pages),
                    'metadata': metadata
                }

                self.logger.info(f"Processed PDF: {file_path} ({len(pdf_reader.pages)} pages)")
                return result

        except Exception as e:
            self.logger.error(f"Error processing PDF {file_path}: {e}")
            raise