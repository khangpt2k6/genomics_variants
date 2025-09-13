# Moffitt Clinical Variant Interpretation Pipeline

A comprehensive pipeline that bridges the gap between raw VCF data from Galaxy and clinically interpretable results by annotating variants with ClinVar, COSMIC, and CIViC databases.

## Features

- **Galaxy Integration**: Automated VCF retrieval from Galaxy workflows
- **Multi-Database Annotation**: ClinVar, COSMIC, and CIViC integration
- **Clinical Dashboard**: Web interface for variant interpretation
- **Pathogenic Variant Detection**: Automated identification of variants of concern
- **Drug Response Analysis**: Biomarker and therapeutic relevance assessment

## Architecture

```
Galaxy API → VCF Parser → Annotation Services → PostgreSQL → Django API → React Dashboard
```

## Quick Start

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database and API credentials
```

3. Run database migrations:
```bash
python manage.py migrate
```

4. Start the Django server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the React development server:
```bash
npm start
```

## Configuration

See `.env.example` for required environment variables including:
- Database credentials
- Galaxy API credentials
- ClinVar, COSMIC, CIViC API keys
- Redis configuration for Celery

## API Documentation

The Django REST API provides endpoints for:
- Variant search and filtering
- Clinical significance data
- Drug response information
- COSMIC frequency data

## Clinical Impact

This pipeline enables:
- Rapid identification of pathogenic variants
- Evidence-based clinical decision making
- Streamlined variant interpretation workflow
- Integration with existing Moffitt infrastructure
