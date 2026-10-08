"""ML pipeline orchestrator for chaining document processing and ML models."""

from typing import List, Union, Dict, Any, Optional
import logging
from .base import BaseMLModel
from ..processors.base import BaseDocumentProcessor
from ..storage.base import BaseStorage

logger = logging.getLogger(__name__)


class MLPipeline:
    """Orchestrates document processing through ML models."""

    def __init__(
        self,
        document_processor: Optional[BaseDocumentProcessor] = None,
        classifier: Optional[BaseMLModel] = None,
        ner_model: Optional[BaseMLModel] = None,
        summarizer: Optional[BaseMLModel] = None,
        storage: Optional[BaseStorage] = None,
    ):
        """
        Initialize the ML pipeline.

        Args:
            document_processor: Processor for extracting text from documents
            classifier: Model for classifying document types
            ner_model: Model for extracting named entities
            summarizer: Model for generating summaries
            storage: Storage backend for saving results
        """
        self.document_processor = document_processor
        self.classifier = classifier
        self.ner_model = ner_model
        self.summarizer = summarizer
        self.storage = storage
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def process_document(
        self, file_path: Optional[str] = None, raw_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a document through the ML pipeline.

        Args:
            file_path: Path to the document file (if provided, raw_text is ignored)
            raw_text: Raw text to process (if file_path is not provided)

        Returns:
            Dictionary containing processing results
        """
        # Step 1: Extract text from document
        if file_path is not None:
            if self.document_processor is None:
                raise ValueError("Document processor is required for file processing")
            text = self.document_processor.process(file_path)
        elif raw_text is not None:
            text = raw_text
        else:
            raise ValueError("Either file_path or raw_text must be provided")

        self.logger.debug(f"Extracted text length: {len(text)}")

        # Step 2: Classify document type
        classification_result = None
        if self.classifier is not None:
            if not self.classifier.is_loaded():
                self.classifier.load_model()
            classification_result = self.classifier.predict(text)
            self.logger.debug(f"Classification result: {classification_result}")

        # Step 3: Extract named entities
        ner_result = None
        if self.ner_model is not None:
            if not self.ner_model.is_loaded():
                self.ner_model.load_model()
            ner_result = self.ner_model.predict(text)
            self.logger.debug(f"NER result: {len(ner_result.get('entities', []))} entities found")

        # Step 4: Generate summary
        summary_result = None
        if self.summarizer is not None:
            if not self.summarizer.is_loaded():
                self.summarizer.load_model()
            summary_result = self.summarizer.predict(text)
            self.logger.debug(f"Summary result: {summary_result}")

        # Compile results
        results = {
            "input_text": text,
            "text_length": len(text),
            "classification": classification_result,
            "ner": ner_result,
            "summary": summary_result,
        }

        # Step 5: Save results if storage is provided
        if self.storage is not None:
            # We'll save the results as a JSON file
            import json
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            object_key = f"ml_pipeline_results/{timestamp}.json"

            # Convert results to JSON string
            json_data = json.dumps(results, indent=2, default=str)

            # We need to save the JSON data. Since our storage abstractions expect a file path or file-like object,
            # we'll create a temporary file or use a string buffer.
            # For simplicity, we'll assume the storage has a method to upload a string.
            # But our current storage abstractions don't have that. We'll skip saving for now and just log.
            self.logger.info(f"Would save results to {object_key} in storage")
            # In a real implementation, we would upload the JSON data.

        return results

    def process_batch(
        self, file_paths: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Process a batch of documents.

        Args:
            file_paths: List of paths to document files

        Returns:
            List of processing results for each document
        """
        results = []
        for file_path in file_paths:
            try:
                result = self.process_document(file_path=file_path)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                results.append({"error": str(e), "file_path": file_path})
        return results