import streamlit as st
import pandas as pd
import json
import io
import base64
from typing import Dict, List, Any, Optional
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import re

# Page configuration
st.set_page_config(
    page_title="OLMoCR - OCR & Document Processing",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
    }
    
    .processing-status {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success { background-color: #d4edda; border-left: 4px solid #28a745; }
    .warning { background-color: #fff3cd; border-left: 4px solid #ffc107; }
    .error { background-color: #f8d7da; border-left: 4px solid #dc3545; }
    .info { background-color: #d1ecf1; border-left: 4px solid #17a2b8; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_documents' not in st.session_state:
    st.session_state.processed_documents = []
if 'processing_history' not in st.session_state:
    st.session_state.processing_history = []
if 'benchmark_results' not in st.session_state:
    st.session_state.benchmark_results = []

class OLMoCRApp:
    def __init__(self):
        self.models = {
            "olmOCR-7B-0725": {"size": "7B", "speed": "Fast", "quality": "High"},
            "olmOCR-7B-0225-preview": {"size": "7B", "speed": "Medium", "quality": "Very High"},
            "Qwen2-VL-7B": {"size": "7B", "speed": "Medium", "quality": "High"},
            "Molmo-O-7B": {"size": "7B", "speed": "Fast", "quality": "Medium"}
        }
        
        self.processing_options = {
            "Standard OCR": "Basic text extraction with layout preservation",
            "Table Extraction": "Specialized processing for tabular data",
            "Equation Recognition": "Mathematical equations and formulas",
            "Handwriting Recognition": "Handwritten text processing",
            "Multi-language": "Support for multiple languages",
            "Form Processing": "Structured form data extraction"
        }

    def render_header(self):
        st.markdown("""
        <div class="main-header">
            <h1>🔍 OLMoCR - Advanced OCR & Document Processing</h1>
            <p>High-quality document conversion powered by Vision Language Models</p>
        </div>
        """, unsafe_allow_html=True)

    def render_sidebar(self):
        with st.sidebar:
            st.title("⚙️ Configuration")
            
            # Model selection
            st.subheader("Model Settings")
            selected_model = st.selectbox("Select OCR Model", list(self.models.keys()))
            
            model_info = self.models[selected_model]
            st.info(f"**Size:** {model_info['size']} | **Speed:** {model_info['speed']} | **Quality:** {model_info['quality']}")
            
            # Processing options
            st.subheader("Processing Options")
            processing_type = st.selectbox("Processing Type", list(self.processing_options.keys()))
            st.caption(self.processing_options[processing_type])
            
            # Advanced settings
            with st.expander("Advanced Settings"):
                max_pages = st.number_input("Max Pages to Process", min_value=1, max_value=1000, value=50)
                target_image_dim = st.slider("Image Resolution", 512, 2048, 1024, step=128)
                confidence_threshold = st.slider("Confidence Threshold", 0.1, 1.0, 0.7, step=0.1)
                apply_filtering = st.checkbox("Apply Language & Spam Filtering", value=True)
                preserve_layout = st.checkbox("Preserve Document Layout", value=True)
            
            # Batch processing settings
            st.subheader("Batch Processing")
            batch_size = st.number_input("Batch Size", min_value=1, max_value=100, value=10)
            parallel_workers = st.number_input("Parallel Workers", min_value=1, max_value=8, value=2)
            
            return {
                'model': selected_model,
                'processing_type': processing_type,
                'max_pages': max_pages,
                'target_image_dim': target_image_dim,
                'confidence_threshold': confidence_threshold,
                'apply_filtering': apply_filtering,
                'preserve_layout': preserve_layout,
                'batch_size': batch_size,
                'parallel_workers': parallel_workers
            }

    def simulate_ocr_processing(self, file_data, config):
        """Simulate OCR processing with realistic outputs"""
        time.sleep(2)  # Simulate processing time
        
        # Generate mock results based on file type and config
        results = {
            'filename': file_data['name'],
            'file_size': file_data['size'],
            'pages_processed': min(file_data.get('estimated_pages', 5), config['max_pages']),
            'processing_time': 2.5 + (file_data['size'] / 1024 / 1024) * 0.5,
            'confidence_score': config['confidence_threshold'] + 0.15,
            'text_length': file_data['size'] * 2,  # Rough estimate
            'errors': 0 if config['confidence_threshold'] > 0.5 else 1,
            'warnings': 0 if config['apply_filtering'] else 2,
            'extracted_text': self.generate_sample_text(config['processing_type']),
            'metadata': {
                'model_used': config['model'],
                'processing_type': config['processing_type'],
                'timestamp': datetime.now().isoformat(),
                'layout_preserved': config['preserve_layout']
            }
        }
        
        return results

    def generate_sample_text(self, processing_type):
        """Generate sample extracted text based on processing type"""
        samples = {
            "Standard OCR": """
            ANNUAL REPORT 2024
            
            Executive Summary
            This year has been marked by significant growth and innovation across all business units. 
            Our revenue increased by 23% compared to the previous year, reaching $2.4 billion.
            
            Key Achievements:
            • Launched 5 new product lines
            • Expanded to 12 new markets
            • Achieved 99.7% customer satisfaction
            """,
            
            "Table Extraction": """
            | Quarter | Revenue | Growth |
            |---------|---------|--------|
            | Q1      | $580M   | 12%    |
            | Q2      | $620M   | 15%    |
            | Q3      | $640M   | 18%    |
            | Q4      | $560M   | 8%     |
            """,
            
            "Equation Recognition": """
            Mathematical Analysis Report
            
            The quadratic equation can be expressed as:
            ax² + bx + c = 0
            
            Where the discriminant Δ = b² - 4ac determines the nature of roots:
            x = (-b ± √Δ) / 2a
            
            Integration formula:
            ∫ f(x)dx = F(x) + C
            """,
            
            "Handwriting Recognition": """
            Meeting Notes - March 15, 2024
            
            Attendees: John Smith, Sarah Johnson, Mike Chen
            
            Action Items:
            - Review quarterly budget (Due: March 20)
            - Prepare presentation for board meeting
            - Follow up with client regarding contract
            
            Next meeting: March 22, 2024 at 2:00 PM
            """,
            
            "Multi-language": """
            Document Title: International Business Overview
            
            English: Welcome to our global expansion initiative.
            Español: Bienvenido a nuestra iniciativa de expansión global.
            Français: Bienvenue dans notre initiative d'expansion mondiale.
            Deutsch: Willkommen zu unserer globalen Expansionsinitiative.
            """,
            
            "Form Processing": """
            CUSTOMER INFORMATION FORM
            
            Name: John Doe
            Email: john.doe@email.com
            Phone: (555) 123-4567
            Address: 123 Main St, Anytown, ST 12345
            
            Service Type: Premium Support
            Start Date: 2024-03-15
            Contract Duration: 12 months
            """
        }
        
        return samples.get(processing_type, samples["Standard OCR"])

    def render_file_upload(self, config):
        st.subheader("📁 Document Upload")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose PDF, PNG, JPG, or other document files",
            accept_multiple_files=True,
            type=['pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp']
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
            
            # Display file information
            file_data = []
            for file in uploaded_files:
                file_info = {
                    'name': file.name,
                    'size': file.size,
                    'type': file.type,
                    'estimated_pages': max(1, file.size // (1024 * 100))  # Rough estimate
                }
                file_data.append(file_info)
            
            # Show file details
            df = pd.DataFrame(file_data)
            df['size_mb'] = (df['size'] / (1024*1024)).round(2)
            st.dataframe(df[['name', 'type', 'size_mb', 'estimated_pages']], use_container_width=True)
            
            # Process files button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Start Processing", use_container_width=True):
                    self.process_files(file_data, config)
            
            return file_data
        
        else:
            # Upload area placeholder
            st.markdown("""
            <div class="upload-area">
                <h3>📄 Drag and drop files here</h3>
                <p>Supported formats: PDF, PNG, JPG, JPEG, TIFF, BMP</p>
                <p>Maximum file size: 200MB per file</p>
            </div>
            """, unsafe_allow_html=True)
            
        return None

    def process_files(self, file_data, config):
        """Process uploaded files with progress tracking"""
        progress_bar = st.progress(0)
        status_placeholder = st.empty()
        
        results = []
        
        for i, file_info in enumerate(file_data):
            progress = (i + 1) / len(file_data)
            progress_bar.progress(progress)
            
            status_placeholder.markdown(f"""
            <div class="processing-status info">
                🔄 Processing: {file_info['name']} ({i+1}/{len(file_data)})
            </div>
            """, unsafe_allow_html=True)
            
            # Simulate processing
            result = self.simulate_ocr_processing(file_info, config)
            results.append(result)
            
            # Add to session state
            st.session_state.processed_documents.append(result)
            st.session_state.processing_history.append({
                'timestamp': datetime.now(),
                'filename': file_info['name'],
                'status': 'completed',
                'processing_time': result['processing_time']
            })
        
        status_placeholder.markdown("""
        <div class="processing-status success">
            ✅ All files processed successfully!
        </div>
        """, unsafe_allow_html=True)
        
        return results

    def render_results_dashboard(self):
        if not st.session_state.processed_documents:
            st.info("👆 Upload and process some documents to see results here!")
            return
        
        st.subheader("📊 Processing Results Dashboard")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_docs = len(st.session_state.processed_documents)
        total_pages = sum(doc['pages_processed'] for doc in st.session_state.processed_documents)
        avg_confidence = sum(doc['confidence_score'] for doc in st.session_state.processed_documents) / total_docs
        total_errors = sum(doc['errors'] for doc in st.session_state.processed_documents)
        
        with col1:
            st.metric("Documents Processed", total_docs)
        with col2:
            st.metric("Total Pages", total_pages)
        with col3:
            st.metric("Avg Confidence", f"{avg_confidence:.2f}")
        with col4:
            st.metric("Total Errors", total_errors)
        
        # Processing time chart
        if len(st.session_state.processed_documents) > 1:
            df = pd.DataFrame(st.session_state.processed_documents)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.bar(df, x='filename', y='processing_time',
                            title='Processing Time by Document')
                fig1.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.scatter(df, x='pages_processed', y='confidence_score',
                                size='file_size', hover_name='filename',
                                title='Confidence vs Pages Processed')
                st.plotly_chart(fig2, use_container_width=True)

    def render_document_viewer(self):
        if not st.session_state.processed_documents:
            return
        
        st.subheader("📖 Document Viewer")
        
        # Document selector
        doc_names = [doc['filename'] for doc in st.session_state.processed_documents]
        selected_doc = st.selectbox("Select Document", doc_names)
        
        if selected_doc:
            doc = next(doc for doc in st.session_state.processed_documents if doc['filename'] == selected_doc)
            
            # Document details
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("### Document Information")
                st.write(f"**Filename:** {doc['filename']}")
                st.write(f"**Pages:** {doc['pages_processed']}")
                st.write(f"**Processing Time:** {doc['processing_time']:.2f}s")
                st.write(f"**Confidence:** {doc['confidence_score']:.2f}")
                st.write(f"**Model Used:** {doc['metadata']['model_used']}")
                st.write(f"**Processing Type:** {doc['metadata']['processing_type']}")
                
                # Download options
                st.markdown("### Export Options")
                col_txt, col_json = st.columns(2)
                
                with col_txt:
                    if st.button("📄 Download Text"):
                        st.download_button(
                            label="Download as TXT",
                            data=doc['extracted_text'],
                            file_name=f"{doc['filename']}_extracted.txt",
                            mime="text/plain"
                        )
                
                with col_json:
                    if st.button("📋 Download JSON"):
                        json_data = json.dumps(doc, indent=2, default=str)
                        st.download_button(
                            label="Download as JSON",
                            data=json_data,
                            file_name=f"{doc['filename']}_metadata.json",
                            mime="application/json"
                        )
            
            with col2:
                st.markdown("### Extracted Text")
                st.text_area("", doc['extracted_text'], height=400, key=f"text_{selected_doc}")

    def render_benchmark_suite(self):
        st.subheader("🏆 OLMoCR-Bench Testing Suite")
        
        st.markdown("""
        The OLMoCR-Bench is a comprehensive benchmark suite covering over 7,000 test cases 
        across 1,400 documents to measure OCR system performance.
        """)
        
        # Benchmark categories
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Test Categories")
            categories = [
                "General Document OCR",
                "Table Extraction",
                "Mathematical Equations",
                "Handwritten Text",
                "Multi-language Documents",
                "Form Processing",
                "Poor Quality Images",
                "Complex Layouts"
            ]
            
            selected_categories = st.multiselect("Select benchmark categories", categories, default=categories[:3])
        
        with col2:
            st.markdown("### Performance Metrics")
            metrics = st.multiselect("Select metrics to evaluate",
                                   ["Character Accuracy", "Word Accuracy", "BLEU Score", "Edit Distance", "Layout Preservation"],
                                   default=["Character Accuracy", "Word Accuracy"])
        
        if st.button("🧪 Run Benchmark Tests"):
            self.run_benchmark_simulation(selected_categories, metrics)

    def run_benchmark_simulation(self, categories, metrics):
        """Simulate benchmark testing"""
        progress_bar = st.progress(0)
        results_placeholder = st.empty()
        
        benchmark_results = []
        
        for i, category in enumerate(categories):
            progress = (i + 1) / len(categories)
            progress_bar.progress(progress)
            
            # Simulate test results
            result = {
                'category': category,
                'test_count': 100 + i * 50,
                'character_accuracy': 0.85 + (i * 0.02),
                'word_accuracy': 0.82 + (i * 0.015),
                'bleu_score': 0.78 + (i * 0.01),
                'edit_distance': 15 - i,
                'layout_preservation': 0.90 + (i * 0.005)
            }
            benchmark_results.append(result)
            time.sleep(0.5)  # Simulate processing time
        
        st.session_state.benchmark_results = benchmark_results
        
        # Display results
        df = pd.DataFrame(benchmark_results)
        
        # Overall score chart
        fig = go.Figure()
        
        for metric in metrics:
            if metric.lower().replace(' ', '_') in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['category'],
                    y=df[metric.lower().replace(' ', '_')],
                    mode='lines+markers',
                    name=metric
                ))
        
        fig.update_layout(title="Benchmark Results by Category", xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed results table
        st.dataframe(df, use_container_width=True)

    def render_pipeline_manager(self):
        st.subheader("⚙️ Processing Pipeline Manager")
        
        tab1, tab2, tab3 = st.tabs(["Pipeline Configuration", "Batch Processing", "Processing History"])
        
        with tab1:
            st.markdown("### Pipeline Setup")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Pre-processing Steps**")
                preprocess_options = st.multiselect(
                    "Select preprocessing steps",
                    ["Image Enhancement", "Noise Reduction", "Skew Correction", "Border Removal"],
                    default=["Image Enhancement", "Skew Correction"]
                )
                
                st.markdown("**Post-processing Steps**")
                postprocess_options = st.multiselect(
                    "Select post-processing steps",
                    ["Spell Check", "Grammar Correction", "Format Normalization", "Language Detection"],
                    default=["Spell Check", "Language Detection"]
                )
            
            with col2:
                st.markdown("**Quality Controls**")
                min_confidence = st.slider("Minimum Confidence Threshold", 0.0, 1.0, 0.7)
                max_error_rate = st.slider("Maximum Error Rate", 0.0, 0.5, 0.1)
                
                st.markdown("**Output Formats**")
                output_formats = st.multiselect(
                    "Select output formats",
                    ["Plain Text", "Markdown", "JSON", "XML", "Dolma JSONL"],
                    default=["Plain Text", "JSON"]
                )
        
        with tab2:
            st.markdown("### Batch Processing")
            
            # S3 configuration (mock)
            st.markdown("**AWS S3 Configuration**")
            col1, col2 = st.columns(2)
            
            with col1:
                s3_input_bucket = st.text_input("Input S3 Bucket", placeholder="s3://my-bucket/input/")
                s3_output_bucket = st.text_input("Output S3 Bucket", placeholder="s3://my-bucket/output/")
            
            with col2:
                workspace_profile = st.text_input("Workspace Profile", placeholder="default")
                pdf_profile = st.text_input("PDF Profile", placeholder="default")
            
            # Beaker configuration (for AI2 users)
            with st.expander("Beaker Cluster Configuration"):
                use_beaker = st.checkbox("Use Beaker for distributed processing")
                if use_beaker:
                    beaker_workspace = st.text_input("Beaker Workspace")
                    beaker_cluster = st.text_input("Beaker Cluster")
                    beaker_gpus = st.number_input("Number of GPUs", min_value=1, max_value=8, value=4)
                    beaker_priority = st.selectbox("Priority", ["low", "normal", "high"])
        
        with tab3:
            st.markdown("### Processing History")
            
            if st.session_state.processing_history:
                df = pd.DataFrame(st.session_state.processing_history)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                # Timeline chart
                fig = px.timeline(df, x_start='timestamp', x_end='timestamp',
                                y='filename', color='status',
                                title='Processing Timeline')
                st.plotly_chart(fig, use_container_width=True)
                
                # History table
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No processing history available yet.")

    def run(self):
        self.render_header()
        
        # Get configuration from sidebar
        config = self.render_sidebar()
        
        # Main tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📁 Document Processing",
            "📊 Results Dashboard",
            "📖 Document Viewer",
            "🏆 Benchmark Suite",
            "⚙️ Pipeline Manager"
        ])
        
        with tab1:
            file_data = self.render_file_upload(config)
        
        with tab2:
            self.render_results_dashboard()
        
        with tab3:
            self.render_document_viewer()
        
        with tab4:
            self.render_benchmark_suite()
        
        with tab5:
            self.render_pipeline_manager()
        


# Run the app
if __name__ == "__main__":
    app = OLMoCRApp()
    app.run()
