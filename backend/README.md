# Space Station Management System - Backend API

FastAPI backend for managing space station crew, missions, and experiments, designed for deployment on Vercel serverless functions.

## 🚀 Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **MySQL** - Relational database
- **mysql-connector-python** - MySQL database driver with connection pooling
- **Pydantic** - Data validation and serialization
- **Vercel** - Serverless deployment platform

## 📁 Project Structure

```
Space-Station/
├── api/
│   ├── index.py              # Main FastAPI application (Vercel entry point)
│   ├── database.py           # MySQL connection with pooling
│   ├── models.py             # Pydantic schemas
│   └── routes/
│       ├── auth.py           # Authentication endpoints
│       ├── missions.py       # Mission CRUD endpoints
│       └── experiments.py    # Experiment CRUD endpoints
├── vercel.json               # Vercel deployment configuration
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🗄️ Database Schema

### Crew Table
```sql
CREATE TABLE crew (
    crew_id INT PRIMARY KEY,
    password VARCHAR(255),
    name VARCHAR(255),
    role VARCHAR(100),
    nationality VARCHAR(100)
);
```

### Mission Table
```sql
CREATE TABLE mission (
    mission_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    purpose VARCHAR(500),
    crew_id INT,
    FOREIGN KEY (crew_id) REFERENCES crew(crew_id)
);
```

### Experiment Table
```sql
CREATE TABLE experiment (
    experiment_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    status VARCHAR(100),
    crew_id INT,
    FOREIGN KEY (crew_id) REFERENCES crew(crew_id)
);
```

## 🔧 Setup Instructions

### 1. Environment Variables

Copy `.env.example` to `.env` and update with your database credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
DB_HOST=your_mysql_host
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=space_station_db
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
python -m uvicorn api.index:app --reload
```

The API will be available at `http://localhost:8000`

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📡 API Endpoints

### Authentication

#### Login
- **POST** `/login`
- **Request Body**:
  ```json
  {
    "crew_id": 1,
    "password": "password123"
  }
  ```
- **Response** (200):
  ```json
  {
    "crew_id": 1,
    "name": "John Doe",
    "role": "Commander",
    "nationality": "USA",
    "message": "Login successful"
  }
  ```

### Missions

#### Get All Missions
- **GET** `/missions`
- **Response** (200):
  ```json
  [
    {
      "mission_id": 1,
      "name": "ISS Maintenance",
      "purpose": "Routine maintenance of ISS modules",
      "crew_id": 1,
      "crew_name": "John Doe"
    }
  ]
  ```

#### Create Mission
- **POST** `/missions`
- **Request Body**:
  ```json
  {
    "name": "Mars Exploration",
    "purpose": "Initial Mars surface exploration",
    "crew_id": 1
  }
  ```

#### Update Mission
- **PUT** `/missions/{mission_id}`
- **Request Body** (all fields optional):
  ```json
  {
    "name": "Updated Mission Name",
    "purpose": "Updated purpose",
    "crew_id": 2
  }
  ```

#### Delete Mission
- **DELETE** `/missions/{mission_id}`

### Experiments

#### Get All Experiments
- **GET** `/experiments`
- **Response** (200):
  ```json
  [
    {
      "experiment_id": 1,
      "title": "Plant Growth in Microgravity",
      "status": "In Progress",
      "crew_id": 1,
      "crew_name": "John Doe"
    }
  ]
  ```

#### Create Experiment
- **POST** `/experiments`
- **Request Body**:
  ```json
  {
    "title": "Protein Crystal Growth",
    "status": "Planned",
    "crew_id": 1
  }
  ```

#### Update Experiment
- **PUT** `/experiments/{experiment_id}`
- **Request Body** (all fields optional):
  ```json
  {
    "title": "Updated Experiment Title",
    "status": "Completed",
    "crew_id": 2
  }
  ```

#### Delete Experiment
- **DELETE** `/experiments/{experiment_id}`

## 🚢 Deployment to Vercel

### Prerequisites
- Vercel account
- Vercel CLI installed: `npm install -g vercel`

### Steps

1. **Login to Vercel**:
   ```bash
   vercel login
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Add Environment Variables** in Vercel Dashboard:
   - Go to Project Settings → Environment Variables
   - Add: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

4. **Production Deployment**:
   ```bash
   vercel --prod
   ```

### Vercel Configuration

The `vercel.json` file configures Vercel to:
- Use Python runtime for `api/index.py`
- Route all requests to the FastAPI application

## 🔒 CORS Configuration

CORS is configured to allow all origins for development. For production, update [api/index.py](api/index.py):

```python
allow_origins=["https://your-angular-app.vercel.app"]
```

## 🧪 Testing the API

### Using curl

```bash
# Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"crew_id": 1, "password": "password123"}'

# Get missions
curl http://localhost:8000/missions

# Create mission
curl -X POST http://localhost:8000/missions \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Mission", "purpose": "Testing", "crew_id": 1}'
```

### Using the Interactive Docs

Navigate to `http://localhost:8000/docs` for the interactive Swagger UI where you can test all endpoints.

## 📝 Features

✅ Async/await support for better performance  
✅ MySQL connection pooling for efficiency  
✅ Comprehensive error handling  
✅ Input validation with Pydantic  
✅ SQL JOIN queries for related data  
✅ RESTful API design  
✅ OpenAPI documentation  
✅ CORS enabled for frontend integration  
✅ Environment-based configuration  
✅ Vercel serverless deployment ready  

## 🔍 Health Check

- **GET** `/health` - Check API and database connectivity

## ⚠️ Important Notes

1. **Password Security**: Current implementation uses plain text passwords. For production, implement password hashing with `bcrypt` or `passlib`.

2. **CORS**: Update CORS settings in production to allow only your frontend domain.

3. **Database**: Ensure your MySQL database is accessible from Vercel. Consider using:
   - PlanetScale
   - AWS RDS
   - Azure Database for MySQL
   - Any MySQL hosting with public access

4. **Connection Pooling**: The connection pool size is set to 5. Adjust based on your needs in [api/database.py](api/database.py).

## 📚 Documentation

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Vercel Python Runtime: https://vercel.com/docs/functions/serverless-functions/runtimes/python

## 🤝 Support

For issues or questions, please refer to the API documentation at `/docs` endpoint.