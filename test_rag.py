#!/usr/bin/env python3
"""Test the RAG system implementation."""

import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_rag_base():
    """Test that we can import and instantiate RAG components."""
    print("Testing RAG system...")

    try:
        from src.rag import RAGSystem, MockRetriever, MockGenerator
        print("+ All RAG classes imported successfully")
    except Exception as e:
        print(f"✗ Failed to import RAG classes: {e}")
        return False

    # Test creating mock components
    try:
        retriever = MockRetriever()
        generator = MockGenerator()
        print("+ Created mock retriever and generator")
    except Exception as e:
        print(f"✗ Error creating mock components: {e}")
        return False

    # Test creating RAG system
    try:
        rag = RAGSystem(retriever=retriever, generator=generator)
        print(f"+ Created RAG system: {rag}")
    except Exception as e:
        print(f"✗ Error creating RAG system: {e}")
        return False

    return True

def test_rag_functionality():
    """Test basic RAG functionality without requiring external dependencies."""
    print("\nTesting RAG functionality...")

    try:
        from src.rag import RAGSystem, MockRetriever, MockGenerator

        # Create components
        retriever = MockRetriever()
        generator = MockGenerator()
        rag = RAGSystem(retriever=retriever, generator=generator)

        # Test that we can call methods
        assert hasattr(rag, 'retrieve'), "RAG should have retrieve method"
        assert hasattr(rag, 'generate'), "RAG should have generate method"
        assert hasattr(rag, 'query'), "RAG should have query method"
        print("+ RAG system has required methods")

        # Test retrieval
        query = "test query"
        context = rag.retrieve(query, top_k=1)
        assert isinstance(context, list), "Retrieve should return a list"
        assert len(context) > 0, "Should retrieve at least one document"
        print("+ Retrieve method works")

        # Test generation
        # Note: the mock generator requires loading? It has a load_model method but predict works without?
        # Actually, the MockGenerator's generate method calls load_model if not loaded.
        response = rag.generate(query, context)
        assert isinstance(response, str), "Generate should return a string"
        assert len(response) > 0, "Should generate a non-empty response"
        print("+ Generate method works")

        # Test full query
        result = rag.query(query, top_k=2)
        assert isinstance(result, dict), "Query should return a dict"
        assert "query" in result, "Result should have query"
        assert "context" in result, "Result should have context"
        assert "response" in result, "Result should have response"
        assert result["query"] == query, "Query should match"
        assert isinstance(result["context"], list), "Context should be a list"
        assert isinstance(result["response"], str), "Response should be a string"
        print("+ Query method works")

        return True

    except Exception as e:
        print(f"✗ Error testing RAG functionality: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the RAG tests."""
    print("=== RAG System Test ===\n")

    tests = [
        test_rag_base,
        test_rag_functionality
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    print("\n" + "="*50)
    if all_passed:
        print("+ All RAG tests passed!")
        print("\nRAG system implementations are ready to use.")
        print("\nTo use the RAG system:")
        print("  from src.rag import RAGSystem, MockRetriever, MockGenerator")
        print("  # For testing, use mock components:")
        print("  retriever = MockRetriever()")
        print("  generator = MockGenerator()")
        print("  rag = RAGSystem(retriever=retriever, generator=generator)")
        print("  # For a real system, implement your own retriever and generator")
        print("  # that inherit from BaseRetriever and BaseGenerator.")
        print("  # Process a query:")
        print("  result = rag.query('Your question here')")
        return 0
    else:
        print("- Some RAG tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())