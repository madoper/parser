# Web Scraping Parser

## Project Overview

A comprehensive web scraping module with an interactive UI for parsing websites according to semantic markup standards.

This project implements a parser system that:
- Loads and parses sitemap.xml files (including nested sitemaps and compressed files)
- Provides an interactive interface for selecting data blocks on pages
- Supports CSS-selectors for data extraction
- Stores parsed data in MongoDB
- Includes task monitoring and logging

## Project Structure

```
.
├── backend/           # Python FastAPI backend
├── frontend/          # React TypeScript frontend
├── docs/              # Documentation
├── .github/           # GitHub Actions CI/CD
├── docker-compose.yml # Local development setup
├── semantic_markup_guide.md  # Coding standards
├── tasks_parser.md    # Technical specification
├── requirements.txt   # Python dependencies
├─━ package.json      # Frontend dependencies
└── README.md
```

## Quick Start

### Requirements
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- MongoDB 6.0+
- Redis 7.0+

### Local Development

```bash
# Clone repository
git clone https://github.com/madoper/parser.git
cd parser

# Start with Docker Compose
docker-compose up

# Backend will be at http://localhost:8000
# Frontend will be at http://localhost:3000
# API docs at http://localhost:8000/docs
```

## Documentation

- [Semantic Markup Guide](./semantic_markup_guide.md) - Code standards and conventions
- [Technical Specification](./tasks_parser.md) - Full technical requirements
- [API Documentation](./docs/api/README.md) - API endpoints reference
- [Architecture](./docs/architecture/system-design.md) - System design

## Key Features

### 1. Sitemap Processing
- Parse sitemap.xml, sitemap_index.xml
- Support for gzip-compressed files
- Recursive handling of nested sitemap indices
- Configurable depth limits and URL limits

### 2. Interactive Block Selection
- Visual page preview in browser
- Click-to-select DOM elements
- Automatic CSS-selector generation
- CSS-selector preview and validation

### 3. Parsing Configuration
- Configurable request delays and timeouts
- Request fingerprint rotation (User-Agent, headers)
- robots.txt compliance
- Concurrent request limits

### 4. Data Extraction
- CSS-selector based data extraction
- Multiple content types (text, HTML, attributes)
- Field mapping to MongoDB collections
- Duplicate handling strategies

### 5. Monitoring & Logging
- Real-time task monitoring
- Detailed logging and error tracking
- Task management (pause/resume/stop)
- Data export (CSV/JSON)

## Technology Stack

### Backend
- **Framework**: FastAPI with async support
- **Database**: MongoDB with Motor (async driver)
- **Cache**: Redis
- **Task Queue**: Celery
- **HTTP Client**: httpx with HTTP/2 support
- **Parsing**: lxml, BeautifulSoup4

### Frontend
- **Framework**: React 18 with Concurrent Features
- **Language**: TypeScript 5.0+
- **State Management**: Zustand + React Query
- **UI Framework**: Tailwind CSS + Headless UI
- **Forms**: react-hook-form + zod
- **Charts**: recharts

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (for production)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack

## Development Guide

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or .\\venv\\Scripts\\activate on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run linting
flake8 src/
black src/
isort src/

# Run server
uvicorn src.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install

# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

## Semantic Markup Standards

All code in this project follows semantic markup principles defined in [semantic_markup_guide.md](./semantic_markup_guide.md):

- **Meaningful naming**: Components, functions, and variables have clear, semantic names
- **Semantic prefixes**: Prefixes indicate component type and purpose
- **Comprehensive documentation**: All functions and classes include semantic comments
- **Type annotations**: Full Python type hints and TypeScript typing
- **Metadata tags**: Special comments for AI-assistants and analysis tools

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Follow semantic markup standards (see [semantic_markup_guide.md](./semantic_markup_guide.md))
2. Write tests for all new functionality
3. Update documentation as needed
4. Use meaningful commit messages
5. Submit pull requests to the develop branch

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation in `/docs`
- Review semantic markup guide for coding standards
