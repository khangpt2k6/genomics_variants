# Moffitt Variant Interpretation Dashboard

A comprehensive clinical variant interpretation platform for Moffitt Cancer Center, built with Django REST API backend and React TypeScript frontend.

## 🏗️ Architecture

### Backend (Django)
- **Framework**: Django 4.2.7 with Django REST Framework
- **Database**: PostgreSQL with advanced indexing
- **Features**:
  - Comprehensive variant data models
  - Clinical significance tracking (ClinVar integration)
  - Drug response data (CIViC integration)
  - COSMIC cancer mutation database
  - Galaxy platform integration
  - Advanced filtering and search capabilities
  - Celery task queue for background processing
  - Redis caching

### Frontend (React)
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI) v5
- **State Management**: React Query for server state
- **Charts**: Recharts for data visualization
- **Features**:
  - Modern, responsive dashboard
  - Advanced variant filtering and search
  - Real-time data visualization
  - Interactive variant detail views
  - Annotation job management
  - Galaxy integration interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Redis (for Celery)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database and API credentials
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API URL
   ```

4. **Start development server**:
   ```bash
   npm start
   ```

## 📊 Features

### Dashboard
- Overview statistics and metrics
- Variant distribution charts
- Recent variants list
- Real-time data updates

### Variants Management
- Advanced filtering and search
- Bulk operations
- Export capabilities
- Detailed variant views with:
  - Clinical significance data
  - Drug response information
  - COSMIC cancer data
  - Functional annotations

### Annotations
- Job management and monitoring
- Progress tracking
- Source integration (ClinVar, COSMIC, CIViC)
- Batch processing capabilities

### Galaxy Integration
- Instance management
- Dataset synchronization
- Workflow execution
- Real-time status monitoring

## 🔧 API Endpoints

### Variants
- `GET /api/variants/` - List variants with filtering
- `GET /api/variants/{id}/` - Get variant details
- `GET /api/variants/statistics/` - Get variant statistics
- `GET /api/variants/search_by_gene/` - Search by gene symbol

### Annotations
- `GET /api/annotations/sources/` - List annotation sources
- `GET /api/annotations/jobs/` - List annotation jobs
- `POST /api/annotations/jobs/` - Create annotation job
- `GET /api/annotations/variant-annotations/` - List variant annotations

### Galaxy Integration
- `GET /api/galaxy/instances/` - List Galaxy instances
- `GET /api/galaxy/datasets/` - List datasets
- `GET /api/galaxy/workflows/` - List workflows
- `POST /api/galaxy/sync-jobs/` - Create sync job

## 🗄️ Database Models

### Core Models
- **Variant**: Genetic variant information
- **ClinicalSignificance**: ClinVar clinical significance data
- **DrugResponse**: CIViC drug response data
- **COSMICData**: COSMIC cancer mutation data
- **VariantAnnotation**: Combined annotation data

### Integration Models
- **GalaxyInstance**: Galaxy server configurations
- **GalaxyDataset**: Dataset tracking and metadata
- **GalaxyWorkflow**: Workflow execution tracking
- **AnnotationJob**: Background annotation processing

## 🔍 Advanced Features

### Filtering & Search
- Multi-field search across variants
- Advanced filtering by clinical significance
- Population frequency filtering
- Impact and consequence filtering
- Date range filtering

### Data Visualization
- Interactive charts and graphs
- Real-time statistics
- Export capabilities
- Responsive design

### Performance
- Database indexing for fast queries
- Pagination for large datasets
- Caching for frequently accessed data
- Background task processing

## 🛠️ Development

### Backend Development
```bash
# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Run Celery worker
celery -A moffitt_variants worker -l info

# Run Celery beat (scheduler)
celery -A moffitt_variants beat -l info
```

### Frontend Development
```bash
# Run tests
npm test

# Build for production
npm run build

# Type checking
npx tsc --noEmit
```

## 📝 Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=moffitt_variants
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
GALAXY_URL=your-galaxy-url
GALAXY_API_KEY=your-galaxy-api-key
CLINVAR_API_KEY=your-clinvar-api-key
COSMIC_API_KEY=your-cosmic-api-key
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏥 About Moffitt Cancer Center

Moffitt Cancer Center is a leading cancer research and treatment center dedicated to contributing to the prevention and cure of cancer through research, education, and patient care.

## 📞 Support

For technical support or questions, please contact the development team or create an issue in the repository.
