#!/usr/bin/env python3
"""Test the NER implementations."""

import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_ner_base():
    """Test that we can import and instantiate NER models."""
    print("Testing NER implementations...")

    try:
        from src.ml import SpacyNER, TransformersNER, NERFactory
        print("+ All NER classes imported successfully")
    except Exception as e:
        print(f"✗ Failed to import NER classes: {e}")
        return False

    # Test SpacyNER
    try:
        spacy_ner = SpacyNER()
        print(f"+ Created SpacyNER: {spacy_ner.model_name}")
        assert not spacy_ner.is_loaded(), "SpacyNER should not be loaded initially"
        print("+ SpacyNER correctly reports not loaded initially")
    except Exception as e:
        print(f"✗ Error creating SpacyNER: {e}")
        return False

    # Test TransformersNER
    try:
        transformers_ner = TransformersNER()
        print(f"+ Created TransformersNER: {transformers_ner.model_name}")
        assert not transformers_ner.is_loaded(), "TransformersNER should not be loaded initially"
        print("+ TransformersNER correctly reports not loaded initially")
    except Exception as e:
        print(f"✗ Error creating TransformersNER: {e}")
        return False

    # Test NERFactory
    try:
        # Test spaCy provider
        spacy_from_factory = NERFactory.create_ner('spacy')
        print(f"+ NERFactory created spaCy NER: {spacy_from_factory.model_name}")

        # Test transformers provider
        transformers_from_factory = NERFactory.create_ner('transformers')
        print(f"+ NERFactory created transformers NER: {transformers_from_factory.model_name}")

        # Test invalid provider
        try:
            NERFactory.create_ner('invalid_provider')
            print("✗ Should not be able to create invalid NER provider")
            return False
        except ValueError as e:
            if "Unsupported NER provider" in str(e):
                print("+ NERFactory correctly rejects unsupported provider")
            else:
                print(f"✗ Unexpected error message: {e}")
                return False

    except Exception as e:
        print(f"✗ Error testing NERFactory: {e}")
        return False

    return True

def test_ner_functionality():
    """Test basic NER functionality without requiring model downloads."""
    print("\nTesting NER functionality...")

    try:
        from src.ml import SpacyNER

        # Test that we can instantiate and check basic properties
        ner = SpacyNER(model_name="en_core_web_sm")
        assert hasattr(ner, 'predict'), "NER should have predict method"
        assert hasattr(ner, 'load_model'), "NER should have load_model method"
        assert hasattr(ner, 'extract_entities'), "NER should have extract_entities method"
        assert hasattr(ner, 'get_entity_summary'), "NER should have get_entity_summary method"
        print("+ SpacyNER has all required methods")

        # Test that we can call methods that don't require model loading
        # (these should either work or give clear errors about model not loaded)
        try:
            result = ner.predict("test")
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

        # Test extract_entities method
        try:
            entities = ner.extract_entities("test")
            print("+ Extract entities method works")
        except RuntimeError as e:
            if "not loaded" in str(e):
                print("+ Extract entities method correctly reports model not loaded")
            else:
                print(f"✗ Unexpected error in extract_entities: {e}")
                return False
        except Exception as e:
            print(f"✗ Unexpected error in extract_entities: {e}")
            return False

        # Test get_entity_summary method
        try:
            summary = ner.get_entity_summary("test")
            print("+ Get entity summary method works")
        except RuntimeError as e:
            if "not loaded" in str(e):
                print("+ Get entity summary method correctly reports model not loaded")
            else:
                print(f"✗ Unexpected error in get_entity_summary: {e}")
                return False
        except Exception as e:
            print(f"✗ Unexpected error in get_entity_summary: {e}")
            return False

        return True

    except Exception as e:
        print(f"✗ Error testing NER functionality: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the NER tests."""
    print("=== NER Implementation Test ===\n")

    tests = [
        test_ner_base,
        test_ner_functionality
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    print("\n" + "="*50)
    if all_passed:
        print("+ All NER tests passed!")
        print("\nNER implementations are ready to use.")
        print("\nTo use the NER models:")
        print("  from src.ml import SpacyNER, TransformersNER, NERFactory")
        print("  # For fast, production-ready NER:")
        print("  ner = SpacyNER()  # Uses en_core_web_sm by default")
        print("  # For higher accuracy (slower, larger model):")
        print("  ner = TransformersNER()  # Uses BERT-based model")
        print("  # Or use the factory:")
        print("  ner = NERFactory.create_ner('spacy')")
        print("\nFirst run will download the spaCy model (~50MB), subsequent runs will be faster.")
        return 0
    else:
        print("- Some NER tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())