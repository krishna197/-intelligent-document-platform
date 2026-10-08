"""Text document processor."""

from typing import Dict, Any
from .base import BaseDocumentProcessor
import logging

logger = logging.getLogger(__name__)


class TextProcessor(BaseDocumentProcessor):
    """Processor for plain text documents."""

    def process(self, file_path: str) -> Dict[str, Any]:
        """Process a text document.

        Args:
            file_path: Path to the text file

        Returns:
            Dictionary containing extracted text and metadata
        """
        if not self.validate_file(file_path):
            raise ValueError(f"Invalid file: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()

            # Basic metadata
            import os
            file_stats = os.stat(file_path)
            metadata = {
                'file_size': file_stats.st_size,
                'line_count': text_content.count('\n') + 1,
                'word_count': len(text_content.split()),
                'char_count': len(text_content)
            }

            result = {
                'file_path': file_path,
                'file_type': 'txt',
                'text_content': text_content,
                'metadata': metadata
            }

            self.logger.info(f"Processed text file: {file_path}")
            return result

        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    text_content = file.read()
                self.logger.warning(f"Used latin-1 encoding for {file_path}")
            except Exception as e:
                self.logger.error(f"Could not decode text file {file_path}: {e}")
                raise

        except Exception as e:
            self.logger.error(f"Error processing text file {file_path}: {e}")
            raise