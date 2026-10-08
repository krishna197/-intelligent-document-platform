#!/usr/bin/env python3
"""Demo script for NER models."""

from src.ml import SpacyNER, TransformersNER

def demo_spacy():
    print("=== spaCy NER Demo ===")
    ner = SpacyNER()
    ner.load_model()

    texts = [
        "Apple Inc. was founded by Steve Jobs in Cupertino, California on April 1, 1976.",
        "Barack Obama served as the 44th President of the United States from 2009 to 2017.",
        "The Treaty of Versailles was signed in 1919, ending World War I."
    ]

    for text in texts:
        print(f"\nText: {text}")
        result = ner.predict(text)
        print(f"Entities found: {len(result['entities'])}")
        for entity in result['entities']:
            print(f"  - {entity['text']} ({entity['label']}) [{entity['start']}:{entity['end']}]")

    ner.unload()

def demo_transformers():
    print("\n=== Transformers NER Demo ===")
    # Note: This might take a while to download the model the first time
    try:
        ner = TransformersNER()
        ner.load_model()

        texts = [
            "Apple Inc. was founded by Steve Jobs in Cupertino, California on April 1, 1976.",
            "Barack Obama served as the 44th President of the United States from 2009 to 2017."
        ]

        for text in texts:
            print(f"\nText: {text}")
            result = ner.predict(text)
            print(f"Entities found: {len(result['entities'])}")
            for entity in result['entities']:
                print(f"  - {entity['text']} ({entity['label']}) [{entity['start']}:{entity['end']}]")

        ner.unload()
    except Exception as e:
        print(f"Transformers NER demo failed (expected if model not available): {e}")

if __name__ == "__main__":
    demo_spacy()
    demo_transformers()