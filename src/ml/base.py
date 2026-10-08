"""Base machine learning model interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union
import logging

logger = logging.getLogger(__name__)


class BaseMLModel(ABC):
    """Abstract base class for all ML models in the platform."""

    def __init__(self, model_name: str = None):
        """
        Initialize the ML model.

        Args:
            model_name: Optional name for the model instance
        """
        self.model_name = model_name or self.__class__.__name__
        self.logger = logging.getLogger(f"{__name__}.{self.model_name}")
        self._is_loaded = False
        self.logger.info(f"Initialized {self.model_name}")

    @abstractmethod
    def load_model(self) -> None:
        """Load the model into memory. Should be implemented by subclasses."""
        pass

    @abstractmethod
    def predict(self, inputs: Union[str, List[str], Dict[str, Any]]) -> Any:
        """
        Make predictions on inputs.

        Args:
            inputs: Input data for prediction (format depends on model type)

        Returns:
            Model predictions (format depends on model type)
        """
        pass

    def process(self, inputs: Union[str, List[str], Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process inputs and return structured results.

        This method handles model loading if needed and formats the output.

        Args:
            inputs: Input data for processing

        Returns:
            Dictionary containing predictions and metadata
        """
        if not self._is_loaded:
            self.logger.info(f"Loading model {self.model_name}")
            self.load_model()
            self._is_loaded = True

        try:
            start_time = self._get_current_time()
            predictions = self.predict(inputs)
            end_time = self._get_current_time()

            result = {
                "model_name": self.model_name,
                "predictions": predictions,
                "processing_time_ms": (end_time - start_time) * 1000,
                "status": "success"
            }

            self.logger.debug(f"Processed {len(inputs) if isinstance(inputs, list) else 1} items")
            return result

        except Exception as e:
            self.logger.error(f"Error during prediction: {e}")
            return {
                "model_name": self.model_name,
                "predictions": None,
                "error": str(e),
                "status": "error"
            }

    def _get_current_time(self) -> float:
        """Get current timestamp in seconds."""
        import time
        return time.time()

    def is_loaded(self) -> bool:
        """Check if the model is loaded."""
        return self._is_loaded

    def unload(self) -> None:
        """Unload the model to free memory."""
        self._is_loaded = False
        self.logger.info(f"Model {self.model_name} unloaded")


# Example concrete implementation for testing
class DummyModel(BaseMLModel):
    """Dummy model for testing the interface."""

    def load_model(self) -> None:
        """Load the dummy model."""
        self.logger.info("Loading dummy model")
        # In a real implementation, this would load actual model weights
        self._model_data = {"test": "value"}
        self._is_loaded = True

    def predict(self, inputs: Union[str, List[str], Dict[str, Any]]) -> Any:
        """Make dummy predictions."""
        if isinstance(inputs, str):
            return f"Processed: {inputs}"
        elif isinstance(inputs, list):
            return [f"Processed: {item}" for item in inputs]
        elif isinstance(inputs, dict):
            return {key: f"Processed: {value}" for key, value in inputs.items()}
        else:
            return f"Processed: {inputs}"