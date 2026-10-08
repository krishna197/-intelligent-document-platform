#!/usr/bin/env python3
"""Verify that the project setup is working correctly."""

import sys
import subprocess

def test_imports():
    """Test that key packages can be imported."""
    print("Testing key package imports...")

    try:
        import boto3
        print("+ Boto3 imported successfully")
    except ImportError as e:
        print(f"- Failed to import boto3: {e}")
        return False

    try:
        import google.cloud.storage
        print("+ Google Cloud Storage imported successfully")
    except ImportError as e:
        print(f"- Failed to import google.cloud.storage: {e}")
        return False

    try:
        import fastapi
        print("+ FastAPI imported successfully")
    except ImportError as e:
        print(f"- Failed to import fastapi: {e}")
        return False

    try:
        import PyPDF2
        print("+ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"- Failed to import PyPDF2: {e}")
        return False

    try:
        import sentence_transformers
        print("+ Sentence Transformers imported successfully")
    except ImportError as e:
        print(f"- Failed to import sentence_transformers: {e}")
        return False

    return True

def test_project_imports():
    """Test that our project modules can be imported."""
    print("\nTesting project module imports...")

    try:
        from src.api.main import app
        print("+ API main module imported successfully")
    except ImportError as e:
        print(f"- Failed to import src.api.main: {e}")
        return False

    try:
        from src.processors.base import BaseDocumentProcessor
        print("+ Processors base module imported successfully")
    except ImportError as e:
        print(f"- Failed to import src.processors.base: {e}")
        return False

    try:
        from src.processors.pdf import PDFProcessor
        print("+ PDF processor imported successfully")
    except ImportError as e:
        print(f"- Failed to import src.processors.pdf: {e}")
        return False

    try:
        from src.processors.text import TextProcessor
        print("+ Text processor imported successfully")
    except ImportError as e:
        print(f"- Failed to import src.processors.text: {e}")
        return False

    return True

def test_virtual_environment():
    """Test that we're in a virtual environment."""
    print("\nTesting virtual environment...")

    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("+ Running in virtual environment")
        print(f"  Virtual environment path: {sys.prefix}")
        return True
    else:
        print("- Not running in virtual environment")
        return False

def main():
    """Run all verification tests."""
    print("=== Intelligent Document Platform Setup Verification ===\n")

    tests = [
        test_virtual_environment,
        test_imports,
        test_project_imports
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    print("\n" + "="*50)
    if all_passed:
        print("+ All tests passed! Setup is ready for development.")
        print("\nNext steps:")
        print("1. Configure AWS and GCP credentials")
        print("2. Create storage buckets in both clouds")
        print("3. Begin implementing document processing pipeline")
        return 0
    else:
        print("- Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())