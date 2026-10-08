"""Text classification model for document type detection."""

from typing import List, Union, Dict, Any
from transformers import pipeline
import torch
import logging

from .base import BaseMLModel

logger = logging.getLogger(__name__)


class DocumentClassifier(BaseMLModel):
    """Zero-shot text classifier for document type detection."""

    def __init__(self, model_name: str = "facebook/bart-large-mnli",
                 candidate_labels: List[str] = None,
                 device: int = None):
        """
        Initialize the document classifier.

        Args:
            model_name: Hugging Face model name for zero-shot classification
            candidate_labels: List of document types to classify into
            device: Device to run model on (-1 for CPU, 0+ for GPU)
        """
        super().__init__(model_name)
        self.candidate_labels = candidate_labels or [
            "resume", "invoice", "contract", "research paper",
            "business letter", "technical documentation", "email",
            "memo", "report", "presentation", "legal document", "financial statement"
        ]
        self.device = device
        self.classifier = None

        # Determine device if not specified
        if self.device is None:
            self.device = 0 if torch.cuda.is_available() else -1
            logger.info(f"Auto-selected device: {'GPU' if self.device >= 0 else 'CPU'}")

    def load_model(self) -> None:
        """Load the zero-shot classification model."""
        try:
            self.logger.info(f"Loading zero-shot classification model: {self.model_name}")
            self.logger.info(f"Candidate labels: {self.candidate_labels}")
            self.logger.info(f"Using device: {'GPU' if self.device >= 0 else 'CPU'}")

            self.classifier = pipeline(
                "zero-shot-classification",
                model=self.model_name,
                device=self.device
            )
            self._is_loaded = True
            self.logger.info("Zero-shot classification model loaded successfully")

        except Exception as e:
            self.logger.error(f"Failed to load zero-shot classification model: {e}")
            raise

    def predict(self, text: Union[str, List[str]]) -> Any:
        """
        Classify text into document types.

        Args:
            text: Text string or list of text strings to classify

        Returns:
            Classification results with labels and scores
        """
        if self.classifier is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        # Handle single text or list of texts
        if isinstance(text, str):
            result = self.classifier(text, self.candidate_labels)
            # Format result for consistency
            return {
                "labels": result["labels"],
                "scores": result["scores"],
                "top_label": result["labels"][0],
                "top_score": result["scores"][0]
            }
        elif isinstance(text, list):
            results = self.classifier(text, self.candidate_labels)
            # Format batch results
            formatted_results = []
            for i, result in enumerate(results):
                formatted_results.append({
                    "labels": result["labels"],
                    "scores": result["scores"],
                    "top_label": result["labels"][0],
                    "top_score": result["scores"][0]
                })
            return formatted_results
        else:
            raise ValueError(f"Unsupported input type: {type(text)}")

    def classify_document(self, text: str) -> Dict[str, Any]:
        """
        Convenience method for classifying a single document.

        Args:
            text: Document text to classify

        Returns:
            Dictionary with classification results and metadata
        """
        result = self.predict(text)
        return {
            "document_type": result["top_label"],
            "confidence": result["top_score"],
            "all_predictions": dict(zip(result["labels"], result["scores"])),
            "model_used": self.model_name
        }


# Example usage and testing function
def test_classifier():
    """Test the document classifier with sample texts."""
    print("Testing Document Classifier...")

    # Sample texts for testing
    sample_texts = [
        "John Doe\nSoftware Engineer\nExperience: 5 years in Python development\nSkills: Python, AWS, Machine Learning",
        "INVOICE\nInvoice Number: INV-2023-001\nDate: 2023-15-10\nAmount Due: $1,250.00\nFor: Web Development Services",
        "This agreement is made between Party A and Party B for the provision of consulting services.",
        "Abstract: This paper presents a novel approach to transformer-based language models for document classification.",
        "Dear Sir/Madam,\n\nI am writing to inquire about the status of my application for the position of Senior Developer."
    ]

    try:
        # Initialize classifier
        classifier = DocumentClassifier()

        # Test single classification
        print("\n--- Single Classification Test ---")
        for i, text in enumerate(sample_texts[:2]):  # Test first two samples
            result = classifier.classify_document(text)
            print(f"Sample {i+1}:")
            print(f"  Text preview: {text[:50]}...")
            print(f"  Predicted type: {result['document_type']} (confidence: {result['confidence']:.3f})")
            print(f"  Top 3 predictions: {dict(list(result['all_predictions'].items())[:3])}")
            print()

        # Test batch classification
        print("--- Batch Classification Test ---")
        batch_results = classifier.predict(sample_texts)
        for i, result in enumerate(batch_results):
            print(f"Sample {i+1}: {result['top_label']} ({result['top_score']:.3f})")

        print("\n+ Classifier tests completed successfully!")
        return True

    except Exception as e:
        print(f"✗ Error testing classifier: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run test if executed directly
    test_classifier()