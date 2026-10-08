#!/usr/bin/env python3
"""Test the summarizer implementation."""

import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_summarizer_base():
    """Test that we can import and instantiate summarizer models."""
    print("Testing summarizer implementations...")

    try:
        from src.ml import Summarizer, SummarizerFactory
        print("+ All summarizer classes imported successfully")
    except Exception as e:
        print(f"✗ Failed to import summarizer classes: {e}")
        return False

    # Test Summarizer
    try:
        summarizer = Summarizer()
        print(f"+ Created Summarizer: {summarizer.model_name}")
        assert not summarizer.is_loaded(), "Summarizer should not be loaded initially"
        print("+ Summarizer correctly reports not loaded initially")
    except Exception as e:
        print(f"✗ Error creating Summarizer: {e}")
        return False

    # Test SummarizerFactory
    try:
        # Test default provider
        summarizer_from_factory = SummarizerFactory.create_summarizer()
        print(f"+ SummarizerFactory created summarizer: {summarizer_from_factory.model_name}")

        # Test with custom parameters
        summarizer_custom = SummarizerFactory.create_summarizer(
            model_name="facebook/bart-large-cnn",
            min_length=10,
            max_length=50
        )
        print(f"+ SummarizerFactory created custom summarizer: {summarizer_custom.model_name}")
        print(f"  min_length: {summarizer_custom.min_length}")
        print(f"  max_length: {summarizer_custom.max_length}")

    except Exception as e:
        print(f"✗ Error testing SummarizerFactory: {e}")
        return False

    return True

def test_summarizer_functionality():
    """Test basic summarizer functionality without requiring model downloads."""
    print("\nTesting summarizer functionality...")

    try:
        from src.ml import Summarizer

        # Test that we can instantiate and check basic properties
        summarizer = Summarizer()
        assert hasattr(summarizer, 'load_model'), "Summarizer should have load_model method"
        assert hasattr(summarizer, 'predict'), "Summarizer should have predict method"
        assert hasattr(summarizer, 'is_loaded'), "Summarizer should have is_loaded method"
        assert hasattr(summarizer, 'unload'), "Summarizer should have unload method"
        print("+ Summarizer has all required methods")

        # Test that we can call methods that don't require model loading
        # (these should either work or give clear errors about model not loaded)
        try:
            result = summarizer.predict("test")
            # If we get here, the model somehow loaded (unexpected but OK)
            print("+ Predict method works")
        except RuntimeError as e:
            if "not loaded" in str(e):
                print("+ Predict method correctly reports model not loaded")
            else:
                print(f"✗ Unexpected error in predict: {e}")
                return False
        except Exception as e:
            print(f"✗ Unexpected error in predict: {e}")
            return False

        return True

    except Exception as e:
        print(f"✗ Error testing summarizer functionality: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the summarizer tests."""
    print("=== Summarizer Implementation Test ===\n")

    tests = [
        test_summarizer_base,
        test_summarizer_functionality
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    print("\n" + "="*50)
    if all_passed:
        print("+ All summarizer tests passed!")
        print("\nSummarizer implementations are ready to use.")
        print("\nTo use the summarizer model:")
        print("  from src.ml import Summarizer, SummarizerFactory")
        print("  # For summarization (uses facebook/bart-large-cnn by default):")
        print("  summarizer = Summarizer()")
        print("  # Or use the factory:")
        print("  summarizer = SummarizerFactory.create_summarizer()")
        print("\nFirst run will download the summarization model (~1.6GB), subsequent runs will be faster.")
        return 0
    else:
        print("- Some summarizer tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())