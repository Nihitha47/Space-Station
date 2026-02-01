# Quick Start Guide - Space Station Management System API

## 🚀 Get Started in 3 Steps

### Step 1: Configure Database

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your MySQL credentials:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=space_station_db
   ```

3. Create database and tables:
   ```bash
   mysql -u root -p < database_setup.sql
   ```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Server

```bash
python run_dev.py
```

**That's it!** Your API is now running at http://localhost:8000

## 📚 Next Steps

- **Interactive API Docs**: http://localhost:8000/docs
- **Test Authentication**: Try logging in with crew_id=1, password=password123
- **Explore Endpoints**: Use the Swagger UI to test all endpoints

## 🧪 Quick Test

Test the login endpoint:

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"crew_id": 1, "password": "password123"}'
```

Expected response:
```json
{
  "crew_id": 1,
  "name": "John Mitchell",
  "role": "Commander",
  "nationality": "USA",
  "message": "Login successful"
}
```

## 🚢 Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Add environment variables in Vercel Dashboard
# Then deploy to production
vercel --prod
```

## 📖 Full Documentation

See [README.md](README.md) for complete documentation.

## ✅ Pre-loaded Sample Data

The database setup includes 5 crew members, 5 missions, and 7 experiments.

**Test Credentials:**
- crew_id: 1, password: password123 (John Mitchell - Commander)
- crew_id: 2, password: password123 (Sarah Chen - Flight Engineer)
- crew_id: 3, password: password123 (Alexei Volkov - Mission Specialist)
- crew_id: 4, password: password123 (Maria Santos - Scientist)
- crew_id: 5, password: password123 (Yuki Tanaka - Pilot)

## 🆘 Troubleshooting

**Database connection error?**
- Check your .env file credentials
- Ensure MySQL is running
- Verify database exists: `mysql -u root -p -e "SHOW DATABASES;"`

**Import errors?**
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: Python 3.8+ required

**Port already in use?**
- Change port in run_dev.py
- Or kill existing process: `lsof -ti:8000 | xargs kill` (Mac/Linux) or check Task Manager (Windows)
