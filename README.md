# 🔍 OLMoCR Streamlit App

A comprehensive web application for high-quality OCR and document processing, built with Streamlit and inspired by the OLMoCR research project.

[![Docker Build](https://github.com/1ordmk/olmocr-streamlit-app/actions/workflows/docker-build.yml/badge.svg)](https://github.com/1ordmk/olmocr-streamlit-app/actions/workflows/docker-build.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/1ordmk/olmocr-streamlit-app)](https://hub.docker.com/r/1ordmk/olmocr-streamlit-app)

## 🌟 Features

- **📄 Document Processing**: Upload and process PDFs, images, and scanned documents
- **🔍 Advanced OCR**: Multiple processing types including table extraction, equation recognition, and handwriting
- **📊 Interactive Dashboard**: Real-time analytics and performance metrics
- **📖 Document Viewer**: Side-by-side comparison of original and extracted content
- **🏆 Benchmark Suite**: Comprehensive testing across multiple document types
- **⚙️ Pipeline Manager**: Batch processing and workflow configuration

## 🚀 Quick Start

### Option 1: Run with Docker (Recommended)

```bash
# Pull and run the latest image
docker run -p 8501:8501 1ordmk/olmocr-streamlit-app:latest
```

Then open http://localhost:8501 in your browser.

### Option 2: Run with Docker Compose

```bash
# Clone the repository
git clone https://github.com/1ordmk/olmocr-streamlit-app.git
cd olmocr-streamlit-app

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f
```

### Option 3: Local Development

```bash
# Clone the repository
git clone https://github.com/1ordmk/olmocr-streamlit-app.git
cd olmocr-streamlit-app

# Create virtual environment
python -m venv olmocr_env
source olmocr_env/bin/activate  # On Windows: olmocr_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run olmocr_app.py
```

## 🐳 Docker Hub

The application is available on Docker Hub:

```bash
docker pull 1ordmk/olmocr-streamlit-app:latest
```

**Available tags:**
- `latest` - Latest stable version
- `main` - Latest development version
- `v1.0.0` - Specific version releases

## 📋 System Requirements

- **Memory**: 2GB RAM minimum, 4GB recommended
- **CPU**: Any modern CPU (multi-core recommended for batch processing)
- **Storage**: 1GB free space
- **Network**: Internet connection for initial setup

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STREAMLIT_SERVER_PORT` | Server port | `8501` |
| `STREAMLIT_SERVER_ADDRESS` | Server address | `0.0.0.0` |
| `PYTHONUNBUFFERED` | Python output buffering | `1` |

### Volume Mounts

```bash
# Mount data directory for persistent storage
docker run -p 8501:8501 -v ./data:/app/data 1ordmk/olmocr-streamlit-app:latest
```

## 🎯 Use Cases

### Business Applications
- **Document Digitization**: Convert paper records to searchable digital format
- **Invoice Processing**: Automated data extraction from invoices and receipts
- **Form Processing**: Extract structured data from filled forms
- **Contract Analysis**: Pull key information from legal documents

### Research & Academia
- **Literature Review**: Extract data from research papers and publications
- **Historical Documents**: Digitize and make searchable old manuscripts
- **Survey Processing**: Convert paper surveys to digital data
- **Archive Management**: Preserve and organize document collections

### Personal Use
- **Document Organization**: Digitize personal documents and files
- **Note Taking**: Convert handwritten notes to digital text
- **Receipt Management**: Extract data from receipts for expense tracking
- **Book Digitization**: Convert book pages to searchable text

## 📊 Processing Types

| Type | Description | Best For |
|------|-------------|----------|
| **Standard OCR** | Basic text extraction | Regular documents, letters |
| **Table Extraction** | Structured data extraction | Spreadsheets, financial reports |
| **Equation Recognition** | Mathematical formulas | Academic papers, textbooks |
| **Handwriting Recognition** | Handwritten text | Notes, forms, letters |
| **Multi-language** | Multiple language support | International documents |
| **Form Processing** | Structured form data | Applications, surveys |

## 🔧 Development

### Building the Docker Image

```bash
# Build locally
docker build -t olmocr-streamlit-app .

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t olmocr-streamlit-app .
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 API Documentation

The application exposes the following endpoints:

- `http://localhost:8501` - Main application interface
- `http://localhost:8501/_stcore/health` - Health check endpoint
- `http://localhost:8501/_stcore/metrics` - Application metrics

## 🚨 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Use a different port
docker run -p 8502:8501 YOUR_DOCKERHUB_USERNAME/olmocr-streamlit-app:latest
```

**Memory issues:**
```bash
# Increase Docker memory limit or use smaller batch sizes
```

**Permission errors:**
```bash
# Ensure proper file permissions
chmod -R 755 ./data
```

### Logs

```bash
# Docker logs
docker logs <container_id>

# Docker Compose logs
docker-compose logs -f olmocr-app
```

## 📈 Performance

- **Single document**: ~2-5 seconds processing time
- **Batch processing**: Configurable parallel workers
- **Memory usage**: ~500MB-2GB depending on document size
- **Concurrent users**: Supports multiple simultaneous users

## 🔒 Security

- Runs as non-root user in container
- No sensitive data stored permanently
- Files processed in memory only
- Health checks enabled

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the [OLMoCR research project](https://github.com/allenai/olmocr)
- Built with [Streamlit](https://streamlit.io/)
- OCR capabilities based on vision language models

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/1ordmk/olmocr-streamlit-app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/1ordmk/olmocr-streamlit-app/discussions)
- **Docker Hub**: [Container Registry](https://hub.docker.com/r/1ordmk/olmocr-streamlit-app)

---

⭐ **Star this repository if you find it useful!**
