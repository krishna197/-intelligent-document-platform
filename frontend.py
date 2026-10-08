import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from PIL import Image
import io
import base64
import json
from typing import Dict, List, Any
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Intelligent Document Analytics Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for colorful, modern look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #FFBE0B, #FB5607);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2E86AB;
        border-bottom: 3px solid #A23B72;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .uploadedFile {
        border: 2px dashed #4ECDC4;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    h1, h2, h3 {
        color: #2E86AB;
    }
</style>
""", unsafe_allow_html=True)

# API base URL
API_BASE_URL = "http://localhost:8001"

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def upload_document(file):
    """Upload a document to the API"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{API_BASE_URL}/api/v1/upload", files=files)
        return response.json()
    except Exception as e:
        st.error(f"Error uploading document: {str(e)}")
        return None

def test_ner(text):
    """Test Named Entity Recognition"""
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/extract",
                               json={"text": text})
        return response.json()
    except Exception as e:
        st.error(f"Error in NER extraction: {str(e)}")
        return None

def test_summarization(text):
    """Test text summarization"""
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/",
                               json={"text": text})
        return response.json()
    except Exception as e:
        st.error(f"Error in summarization: {str(e)}")
        return None

def test_rag_question(question, context=None):
    """Test RAG question answering"""
    try:
        payload = {"question": question}
        if context:
            payload["context"] = context
        response = requests.post(f"{API_BASE_URL}/api/v1/rag/query",
                               json=payload)
        return response.json()
    except Exception as e:
        st.error(f"Error in RAG query: {str(e)}")
        return None

def create_3d_scatter_plot():
    """Create a sample 3D scatter plot for demonstration"""
    # Generate sample 3D data
    np.random.seed(42)
    n_points = 100

    x = np.random.randn(n_points)
    y = np.random.randn(n_points)
    z = np.random.randn(n_points)
    colors = np.random.rand(n_points)

    fig = go.Figure(data=go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=8,
            color=colors,  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
            opacity=0.8
        )
    ))

    fig.update_layout(
        title='3D Embedding Visualization (Sample Data)',
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis'
        ),
        width=700,
        height=500,
        margin=dict(r=20, b=10, l=10, t=40)
    )

    return fig

def create_wordcloud_3d():
    """Create a 3D word cloud visualization"""
    # Sample data for 3D word cloud effect
    words = ['Document', 'Processing', 'NER', 'RAG', 'Summarization',
             'ML', 'AI', 'Cloud', 'Analytics', 'Platform', 'Python',
             'FastAPI', 'Streamlit', 'Plotly', '3D']

    # Generate positions and sizes
    np.random.seed(42)
    x = np.random.randn(len(words)) * 3
    y = np.random.randn(len(words)) * 3
    z = np.random.randn(len(words)) * 2
    sizes = np.random.rand(len(words)) * 20 + 10
    colors = np.linspace(0, 1, len(words))  # Simple color array

    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='text',
        text=words,
        marker=dict(
            size=sizes,
            color=colors,
            colorscale='Viridis',
            opacity=0.8
        )
    )])

    fig.update_layout(
        title='3D Word Cloud Visualization',
        scene=dict(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        ),
        width=700,
        height=500,
        margin=dict(r=20, b=10, l=10, t=40)
    )

    return fig

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">📄 Intelligent Document Analytics Platform</h1>',
                unsafe_allow_html=True)

    # Check API health
    if not check_api_health():
        st.error("⚠️ API is not running! Please start the FastAPI backend first.")
        st.info("Run: `uvicorn src.api.main:app --reload` in the project directory")
        st.stop()
    else:
        st.success("✅ API is connected and running!")

    # Sidebar
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        page = st.selectbox(
            "Choose a section",
            ["🏠 Home", "📤 Document Upload", "🏷️ NER Testing", "📝 Summarization",
             "❓ RAG Q&A", "📊 3D Visualizations", "🔧 System Info"]
        )

        st.markdown("---")
        st.markdown("### 🎨 Theme")
        theme = st.color_picker("Pick accent color", "#FF6B6B")

        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        st.metric("API Status", "Online", "✅")
        st.metric("Last Updated", time.strftime("%H:%M:%S"))

    # Main content based on selection
    if page == "🏠 Home":
        show_home()
    elif page == "📤 Document Upload":
        show_document_upload()
    elif page == "🏷️ NER Testing":
        show_ner_testing()
    elif page == "📝 Summarization":
        show_summarization()
    elif page == "❓ RAG Q&A":
        show_rag_qa()
    elif page == "📊 3D Visualizations":
        show_3d_visualizations()
    elif page == "🔧 System Info":
        show_system_info()

def show_home():
    st.markdown('<h2 class="section-header">Welcome to the Document Analytics Platform</h2>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📤 Document Processing</h3>
            <p>Upload and process PDF, DOCX, TXT files</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🏷️ AI Models</h3>
            <p>NER, Summarization, Classification</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>❓ RAG System</h3>
            <p>Question Answering with Context</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Features overview
    st.markdown('<h2 class="section-header">Platform Features</h2>',
                unsafe_allow_html=True)

    features = [
        ("🚀", "High Performance", "Built with FastAPI for async processing"),
        ("🤖", "ML Powered", "State-of-the-art NLP models from Hugging Face"),
        ("☁️", "Multi-Cloud", "AWS, GCP, and Cloudflare R2 storage support"),
        ("🔍", "Advanced Search", "Vector embeddings + semantic search"),
        ("📊", "Analytics Dashboard", "Interactive visualizations and metrics"),
        ("🔐", "Secure & Scalable", "Production-ready with proper error handling")
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1.5rem; margin: 1rem 0;
                       background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
                <h3>{icon} {title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Sample 3D visualization
    st.markdown('<h2 class="section-header">Sample 3D Visualization</h2>',
                unsafe_allow_html=True)
    fig = create_3d_scatter_plot()
    st.plotly_chart(fig, use_container_width=True)

def show_document_upload():
    st.markdown('<h2 class="section-header">📤 Document Upload & Processing</h2>',
                unsafe_allow_html=True)

    st.markdown("Upload documents to extract text, analyze content, and test platform features.")

    uploaded_file = st.file_uploader(
        "Choose a document file",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT"
    )

    if uploaded_file is not None:
        # Display file info
        st.markdown(f"""
        <div class="uploadedFile">
            <h4>📄 File Selected: {uploaded_file.name}</h4>
            <p>Size: {uploaded_file.size / 1024:.1f} KB</p>
            <p>Type: {uploaded_file.type}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Process Document", type="primary"):
            with st.spinner("Processing document..."):
                result = upload_document(uploaded_file)

                if result:
                    st.success("✅ Document processed successfully!")

                    # Display results in tabs
                    tab1, tab2, tab3 = st.tabs(["📄 Extracted Text", "📊 Analysis", "🔍 Metadata"])

                    with tab1:
                        if 'text' in result:
                            st.text_area("Extracted Content", result['text'], height=200)
                        else:
                            st.write(result)

                    with tab2:
                        # Show some analytics
                        if 'text' in result and result['text']:
                            text = result['text']
                            word_count = len(text.split())
                            char_count = len(text)
                            sentence_count = text.count('.') + text.count('!') + text.count('?')

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Words", word_count)
                            with col2:
                                st.metric("Characters", char_count)
                            with col3:
                                st.metric("Sentences", sentence_count)

                    with tab3:
                        st.json(result)

def show_ner_testing():
    st.markdown('<h2 class="section-header">🏷️ Named Entity Recognition Testing</h2>',
                unsafe_allow_html=True)

    st.markdown("Test the NER model with custom text or sample documents.")

    # Text input options
    input_method = st.radio("Choose input method:", ["✍️ Type Text", "📄 Use Sample Text"])

    if input_method == "✍️ Type Text":
        text = st.text_area(
            "Enter text for NER analysis:",
            placeholder="Enter your text here... Apple Inc. was founded by Steve Jobs in Cupertino, California.",
            height=150
        )
    else:
        # Sample text
        text = """
        Apple Inc. is an American multinational technology company headquartered in Cupertino, California.
        Founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in April 1976, Apple has grown to become
        one of the world's most valuable companies. The company designs, develops, and sells consumer
        electronics, computer software, and online services. Key products include the iPhone, iPad, Mac,
        Apple Watch, and Apple TV. Tim Cook has served as CEO since 2011, succeeding the visionary Steve Jobs.
        """
        st.text_area("Sample Text:", text, height=150, disabled=True)

    if st.button("🔍 Extract Entities", type="primary") and text.strip():
        with st.spinner("Analyzing text for named entities..."):
            result = test_ner(text)

            if result:
                st.success("✅ NER analysis completed!")

                # Display results
                if isinstance(result, dict) and 'entities' in result:
                    entities = result['entities']

                    if entities:
                        # Create colorful visualization
                        st.markdown('<h3 class="section-header">🎯 Detected Entities</h3>',
                                    unsafe_allow_html=True)

                        # Group by entity type for better display
                        entity_types = {}
                        for entity in entities:
                            label = entity.get('label', 'UNKNOWN')
                            if label not in entity_types:
                                entity_types[label] = []
                            entity_types[label].append(entity.get('text', ''))

                        # Display entities in colorful boxes
                        cols = st.columns(2)
                        color_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFBE0B', '#FB5607', '#8338EC']

                        for i, (label, texts) in enumerate(entity_types.items()):
                            with cols[i % 2]:
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, {color_palette[i % len(color_palette)]}20, {color_palette[i % len(color_palette)]}10);
                                           border-left: 4px solid {color_palette[i % len(color_palette)]};
                                           padding: 1rem; margin: 0.5rem 0; border-radius: 5px;">
                                    <h4 style="color: {color_palette[i % len(color_palette)]}; margin: 0 0 0.5rem 0;">{label}</h4>
                                    <ul style="margin: 0; padding-left: 1.2rem;">
                                    {''.join([f'<li>• {text}</li>' for text in set(texts)])}
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)

                        # Show raw JSON
                        with st.expander("🔍 View Raw Results"):
                            st.json(result)
                    else:
                        st.info("No entities detected in the provided text.")
                else:
                    st.json(result)

def show_summarization():
    st.markdown('<h2 class="section-header">📝 Text Summarization Testing</h2>',
                unsafe_allow_html=True)

    st.markdown("Test the summarization model to generate concise summaries of long texts.")

    # Text input
    text = st.text_area(
        "Enter text to summarize:",
        placeholder="Paste a long article, document, or text that you want to summarize...",
        height=200
    )

    # Summary options
    col1, col2 = st.columns(2)
    with col1:
        max_length = st.slider("Maximum Summary Length", 50, 300, 150)
    with col2:
        min_length = st.slider("Minimum Summary Length", 10, 100, 30)

    if st.button("📝 Generate Summary", type="primary") and text.strip():
        with st.spinner("Generating summary..."):
            # In a real implementation, we'd send these parameters to the API
            result = test_summarization(text)

            if result:
                st.success("✅ Summary generated!")

                # Display original vs summary
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown('<h3 class="section-header">📄 Original Text</h3>',
                                unsafe_allow_html=True)
                    st.text_area("", text, height=250, disabled=True)

                    # Stats
                    orig_words = len(text.split())
                    st.caption(f"Words: {orig_words:,} | Characters: {len(text):,}")

                with col2:
                    st.markdown('<h3 class="section-header">📋 Summary</h3>',
                                unsafe_allow_html=True)
                    if isinstance(result, dict) and 'summary_text' in result:
                        summary = result['summary_text']
                        st.text_area("", summary, height=250, disabled=True)

                        # Stats
                        summary_words = len(summary.split())
                        compression = ((orig_words - summary_words) / orig_words) * 100
                        st.caption(f"Words: {summary_words:,} | Compression: {compression:.1f}%")
                    else:
                        st.text_area("", str(result), height=250, disabled=True)

                # Show raw result
                with st.expander("🔍 View Raw API Response"):
                    st.json(result)

def show_rag_qa():
    st.markdown('<h2 class="section-header">❓ RAG Question Answering</h2>',
                unsafe_allow_html=True)

    st.markdown("Test the Retrieval-Augmented Generation system by asking questions about provided context.")

    # Context input
    st.markdown("### 📚 Context (Knowledge Base)")
    context_input = st.text_area(
        "Enter context or knowledge base:",
        placeholder="Provide background information that the AI can use to answer questions...",
        height=150
    )

    # Question input
    st.markdown("### ❓ Question")
    question = st.text_input(
        "Ask a question about the context:",
        placeholder="What is the main topic discussed in the context?"
    )

    if st.button("🔍 Get Answer", type="primary") and question.strip():
        with st.spinner("Searching for answer..."):
            result = test_rag_question(question, context_input if context_input.strip() else None)

            if result:
                st.success("✅ Answer generated!")

                # Display Q&A in a nice format
                st.markdown('<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; color: white;">',
                            unsafe_allow_html=True)
                st.markdown(f"### ❓ Question")
                st.markdown(f"**{question}**")
                st.markdown(f"### 💡 Answer")
                if isinstance(result, dict) and 'answer' in result:
                    st.markdown(f"**{result['answer']}**")
                else:
                    st.markdown(f"**{result}**")
                st.markdown('</div>', unsafe_allow_html=True)

                # Show additional info if available
                if isinstance(result, dict):
                    with st.expander("🔍 View Detailed Response"):
                        st.json(result)

def show_3d_visualizations():
    st.markdown('<h2 class="section-header">📊 3D Visualizations & Analytics</h2>',
                unsafe_allow_html=True)

    st.markdown("Explore 3D visualizations of document embeddings, word clouds, and model performance metrics.")

    viz_type = st.selectbox(
        "Choose visualization type:",
        ["🎯 3D Embedding Space", "☁️ 3D Word Cloud", "📈 Model Performance", "🔗 Document Similarity"]
    )

    if viz_type == "🎯 3D Embedding Space":
        st.markdown("### 3D Document Embedding Visualization")
        st.markdown("See how documents are positioned in the 3D embedding space based on semantic similarity.")

        fig = create_3d_scatter_plot()
        st.plotly_chart(fig, use_container_width=True)

        st.info("""
        💡 **How to interpret this visualization:**
        - Points closer together represent semantically similar documents
        - Color intensity represents different document categories or topics
        - Use your mouse to rotate, zoom, and pan the 3D view
        """)

    elif viz_type == "☁️ 3D Word Cloud":
        st.markdown("### 3D Word Cloud Visualization")
        st.markdown("Explore key terms from documents in an interactive 3D word cloud.")

        st.info("📝 This 3D word cloud shows prominent terms extracted from processed documents.")
        # Note: Full implementation would require importing matplotlib and generating actual word positions
        # For demo, we'll show a placeholder
        fig = go.Figure()
        fig.update_layout(
            title="3D Word Cloud (Demo)",
            scene=dict(
                xaxis=dict(showbackground=False),
                yaxis=dict(showbackground=False),
                zaxis=dict(showbackground=False)
            ),
            annotations=[
                dict(
                    showarrow=False,
                    text="3D Word Cloud Visualization<br>Shows key terms from document corpus",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    font=dict(size=20, color="gray")
                )
            ],
            width=700,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "📈 Model Performance":
        st.markdown("### Model Performance Metrics")

        # Sample performance data
        models = ['NER', 'Summarization', 'Classification', 'RAG']
        accuracy = [92.3, 88.7, 90.1, 85.4]
        speed = [45, 120, 38, 95]  # ms per inference

        col1, col2 = st.columns(2)

        with col1:
            fig_acc = go.Figure(data=[
                go.Bar(name='Accuracy (%)', x=models, y=accuracy,
                       marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFBE0B'])
            ])
            fig_acc.update_layout(title="Model Accuracy Comparison", yaxis_title="Accuracy (%)")
            st.plotly_chart(fig_acc, use_container_width=True)

        with col2:
            fig_speed = go.Figure(data=[
                go.Bar(name='Speed (ms)', x=models, y=speed,
                       marker_color=['#FB5607', '#8338EC', '#F72585', '#4CC9F0'])
            ])
            fig_speed.update_layout(title="Inference Speed Comparison", yaxis_title="Time (ms)")
            st.plotly_chart(fig_speed, use_container_width=True)

    elif viz_type == "🔗 Document Similarity":
        st.markdown("### Document Similarity Network")
        st.markdown("Visualize relationships between documents based on semantic similarity.")

        # Create a simple network graph
        fig = go.Figure()

        # Add nodes (documents)
        nodes = ['Doc 1', 'Doc 2', 'Doc 3', 'Doc 4', 'Doc 5']
        x_nodes = [0, 2, 1, 3, 2]
        y_nodes = [0, 0, 2, 2, 4]

        fig.add_trace(go.Scatter(
            x=x_nodes, y=y_nodes,
            mode='markers+text',
            text=nodes,
            textposition="middle center",
            marker=dict(size=20, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFBE0B', '#FB5607']),
            name="Documents"
        ))

        # Add edges (similarities)
        edges = [(0,1,0.8), (0,2,0.6), (1,3,0.7), (2,4,0.5), (3,4,0.9)]
        for i, j, weight in edges:
            fig.add_trace(go.Scatter(
                x=[x_nodes[i], x_nodes[j]], y=[y_nodes[i], y_nodes[j]],
                mode='lines',
                line=dict(width=weight*5, color='rgba(125,125,125,0.5)'),
                showlegend=False,
                hoverinfo='none'
            ))

        fig.update_layout(
            title="Document Similarity Network",
            showlegend=False,
            width=700,
            height=500,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

        st.plotly_chart(fig, use_container_width=True)

def show_system_info():
    st.markdown('<h2 class="section-header">🔧 System Information & Diagnostics</h2>',
                unsafe_allow_html=True)

    # API Health Check
    st.markdown("### 🏥 API Health Status")
    if check_api_health():
        st.success("✅ API Server: Online and responding")
    else:
        st.error("❌ API Server: Offline or not responding")

    # Endpoint testing
    st.markdown("### 🔌 Endpoint Tests")

    endpoints = [
        ("/docs", "GET", "API Documentation"),
        ("/openapi.json", "GET", "OpenAPI Schema"),
        ("/api/v1/health", "GET", "Health Check (if available)"),
        ("/api/v1/documents/upload", "POST", "Document Upload Endpoint")
    ]

    for endpoint, method, description in endpoints:
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            st.text(f"{method} {endpoint}")
        with col2:
            try:
                if method == "GET":
                    resp = requests.get(f"{API_BASE_URL}{endpoint}", timeout=3)
                else:
                    resp = requests.post(f"{API_BASE_URL}{endpoint}", timeout=3)
                status = "✅" if resp.status_code < 500 else "❌"
            except:
                status = "⚠️"
            with col2:
                st.text(status)
        with col3:
            st.text(description)

    # Environment info
    st.markdown("### 💻 Environment Information")
    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **Backend Technology Stack:**
        - Framework: FastAPI
        - Language: Python 3.14+
        - Server: Uvicorn
        - ML: Transformers, spaCy, Sentence Transformers
        - Vector DB: FAISS
        """)

    with col2:
        st.info("""
        **Frontend Technology Stack:**
        - Framework: Streamlit
        - Visualization: Plotly
        - Styling: Custom CSS3
        - 3D: Plotly 3D Scatter
        """)

    # Performance metrics
    st.markdown("### ⚡ Performance Metrics")

    # Simulate some metrics
    metrics_data = {
        "Average Response Time": "125 ms",
        "Requests per Minute": "45",
        "Memory Usage": "285 MB",
        "CPU Utilization": "15%"
    }

    cols = st.columns(2)
    for i, (label, value) in enumerate(metrics_data.items()):
        with cols[i % 2]:
            st.metric(label, value)

# Run the app
if __name__ == "__main__":
    main()