"""Text summarization model for generating summaries of text."""

from typing import List, Union, Dict, Any
import logging
from transformers import pipeline

from .base import BaseMLModel

logger = logging.getLogger(__name__)


class Summarizer(BaseMLModel):
    """Text summarization model using Hugging Face transformers."""

    def __init__(
        self,
        model_name: str = "facebook/bart-large-cnn",
        min_length: int = 30,
        max_length: int = 150,
        do_sample: bool = False,
    ):
        """
        Initialize the summarization model.

        Args:
            model_name: Hugging Face model name for summarization
            min_length: Minimum length of the summary
            max_length: Maximum length of the summary
            do_sample: Whether to use sampling; if False, uses greedy decoding
        """
        super().__init__(model_name)
        self.min_length = min_length
        self.max_length = max_length
        self.do_sample = do_sample
        self.summarizer_pipeline = None

    def load_model(self) -> None:
        """Load the summarization model."""
        try:
            self.logger.info(f"Loading summarization model: {self.model_name}")
            self.summarizer_pipeline = pipeline(
                "summarization",
                model=self.model_name,
                min_length=self.min_length,
                max_length=self.max_length,
                do_sample=self.do_sample,
            )
            self._is_loaded = True
            self.logger.info(f"Summarization model {self.model_name} loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load summarization model: {e}")
            raise

    def predict(self, texts: Union[str, List[str]]) -> Any:
        """
        Generate summaries for the input text(s).

        Args:
            texts: A single string or a list of strings to summarize

        Returns:
            Summary result(s) from the model
        """
        if self.summarizer_pipeline is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        # Handle single string or list of strings
        if isinstance(texts, str):
            return self.summarizer_pipeline(texts)[0]  # Returns a dict with 'summary_text'
        elif isinstance(texts, list):
            return self.summarizer_pipeline(texts)  # Returns a list of dicts
        else:
            raise ValueError(f"Unsupported input type: {type(texts)}")


# Factory for creating summarizer instances
class SummarizerFactory:
    """Factory for creating summarizer model instances."""

    @staticmethod
    def create_summarizer(**kwargs) -> Summarizer:
        """
        Create a summarizer model instance.

        Args:
            **kwargs: Configuration for the Summarizer constructor

        Returns:
            Summarizer model instance
        """
        return Summarizer(**kwargs)


# Example usage and testing function
def test_summarizer():
    """Test the summarizer implementation."""
    print("Testing Summarizer...")

    # Sample text for testing
    sample_text = """
    The Amazon rainforest, also known as Amazonia, is a moist broadleaf tropical rainforest in the Amazon biome
    that covers most of the Amazon basin of South America. This basin encompasses 7,000,000 km2 (2,700,000 sq mi),
    of which 5,500,000 km2 (2,100,000 sq mi) are covered by the rainforest. This region includes territory
    belonging to nine nations. The majority of the forest is contained within Brazil, with 60% of the rainforest,
    followed by Peru with 13%, Colombia with 10%, and with minor amounts in Venezuela, Ecuador, Bolivia,
    Guyana, Suriname and French Guiana. States or departments in four nations contain "Amazonas" in their names.
    The Amazon represents over half of the planet's remaining rainforests, and comprises the largest and most
    biodiverse tract of tropical rainforest in the world, with an estimated 390 billion individual trees divided
    into 16,000 species.
    """

    try:
        # Test the summarizer
        summarizer = SummarizerFactory.create_summarizer()
        print(f"+ Created summarizer: {summarizer.model_name}")

        # Test that we can instantiate (actual processing would download model)
        assert not summarizer.is_loaded(), "Summarizer should not be loaded initially"
        print("+ Summarizer correctly reports not loaded initially")

        # Load the model and test summarization
        summarizer.load_model()
        assert summarizer.is_loaded(), "Summarizer should be loaded after load_model()"
        print("+ Summarizer correctly reports loaded after load_model()")

        # Test summarization
        result = summarizer.predict(sample_text)
        assert isinstance(result, dict) and "summary_text" in result, "Should have summary_text in result"
        assert len(result["summary_text"]) > 0, "Should have a non-empty summary"
        print(f"+ Summarizer generated summary: {result['summary_text'][:100]}...")

        # Test unloading
        summarizer.unload()
        assert not summarizer.is_loaded(), "Summarizer should be unloaded"
        print("+ Summarizer unloading works correctly")

        print("\n+ Summarizer test completed successfully!")
        return True

    except Exception as e:
        print(f"✗ Error testing summarizer: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run test if executed directly
    test_summarizer()