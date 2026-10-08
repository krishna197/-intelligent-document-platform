"""Base document processor class."""

from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class BaseDocumentProcessor(ABC):
    """Base class for document processors."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def process(self, file_path: str) -> Dict[str, Any]:
        """Process a document and return extracted information.

        Args:
            file_path: Path to the document file

        Returns:
            Dictionary containing processed document data
        """
        pass

    def validate_file(self, file_path: str) -> bool:
        """Validate that the file exists and is readable.

        Args:
            file_path: Path to the file to validate

        Returns:
            True if file is valid, False otherwise
        """
        import os
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return False

        if not os.access(file_path, os.R_OK):
            self.logger.error(f"File not readable: {file_path}")
            return False

        return True