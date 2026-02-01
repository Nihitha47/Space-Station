# Deployment Guide - Vercel Serverless Functions

## 📋 Prerequisites

- [x] Vercel account (sign up at https://vercel.com)
- [x] Git repository (GitHub, GitLab, or Bitbucket)
- [x] MySQL database accessible from the internet
- [x] Node.js installed (for Vercel CLI)

## 🗄️ Database Setup

### Option 1: PlanetScale (Recommended - Free Tier Available)

1. Sign up at https://planetscale.com
2. Create a new database
3. Get connection credentials from "Connect" button
4. Note down: host, username, password, database name

### Option 2: AWS RDS

1. Create MySQL instance in AWS RDS
2. Configure security group to allow public access
3. Note connection details

### Option 3: Azure Database for MySQL

1. Create Azure Database for MySQL
2. Configure firewall rules
3. Note connection details

### Option 4: Railway (Free Tier)

1. Sign up at https://railway.app
2. Create new MySQL database
3. Get connection credentials

## 🚀 Deployment Steps

### Method 1: Deploy via Vercel Dashboard (Easiest)

1. **Push Code to Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Space Station Management System"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to https://vercel.com/new
   - Import your Git repository
   - Vercel will auto-detect the Python project

3. **Configure Environment Variables**
   - In project settings, add:
     - `DB_HOST`: your_database_host
     - `DB_USER`: your_database_username
     - `DB_PASSWORD`: your_database_password
     - `DB_NAME`: space_station_db

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Your API is now live!

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```
   
   Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N**
   - Project name? **space-station-api**
   - Directory? **./Space-Station**

4. **Add Environment Variables**
   ```bash
   vercel env add DB_HOST
   vercel env add DB_USER
   vercel env add DB_PASSWORD
   vercel env add DB_NAME
   ```
   
   Enter values when prompted, select "Production"

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## ✅ Verify Deployment

After deployment, test your API:

```bash
# Replace with your Vercel URL
VERCEL_URL="https://your-app.vercel.app"

# Test root endpoint
curl $VERCEL_URL

# Test health check
curl $VERCEL_URL/health

# Test login
curl -X POST $VERCEL_URL/login \
  -H "Content-Type: application/json" \
  -d '{"crew_id": 1, "password": "password123"}'

# Test missions
curl $VERCEL_URL/missions
```

## 🔒 Update CORS for Production

After deployment, update CORS in [api/index.py](api/index.py):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-angular-app.vercel.app",  # Your Angular frontend
        "http://localhost:4200"  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Redeploy:
```bash
vercel --prod
```

## 📊 Monitor Your API

### Vercel Dashboard

- View logs: Project → Deployments → Select deployment → View logs
- Monitor usage: Project → Analytics
- Check errors: Project → Logs

### Test Endpoints

Use the API documentation at:
- `https://your-app.vercel.app/docs`
- `https://your-app.vercel.app/redoc`

## 🔄 Continuous Deployment

Once connected to Git, Vercel automatically deploys:
- **Production**: Commits to `main` branch
- **Preview**: Pull requests and other branches

To trigger deployment:
```bash
git add .
git commit -m "Update API"
git push origin main
```

## 🐛 Troubleshooting

### Build Failures

**Error: Module not found**
- Check `requirements.txt` includes all dependencies
- Verify Python version compatibility

**Error: Database connection failed**
- Verify environment variables are set correctly
- Check database is publicly accessible
- Verify firewall rules allow Vercel IPs

### Runtime Errors

**500 Internal Server Error**
- Check Vercel logs for detailed error
- Verify database credentials
- Ensure tables exist

**CORS Errors**
- Update CORS settings in [api/index.py](api/index.py)
- Redeploy application

### Performance Issues

**Cold Start Delays**
- First request after inactivity may be slow
- Consider upgrading to Vercel Pro for improved cold starts
- Optimize database queries

## 📈 Scaling Considerations

### Database Connections

Serverless functions create new connections frequently. Consider:

1. **Connection Pooling**: Already implemented in [api/database.py](api/database.py)
2. **Database Proxy**: Use PlanetScale or AWS RDS Proxy
3. **Pool Size**: Adjust in [api/database.py](api/database.py):
   ```python
   "pool_size": 5  # Increase if needed
   ```

### Rate Limiting

Implement rate limiting for production:
```bash
pip install slowapi
```

Add to [api/index.py](api/index.py):
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/missions")
@limiter.limit("60/minute")
async def get_missions():
    # ...
```

## 🎯 Post-Deployment Checklist

- [ ] Verify all endpoints work
- [ ] Update CORS settings
- [ ] Test login with real credentials
- [ ] Monitor initial traffic
- [ ] Set up custom domain (optional)
- [ ] Configure SSL (automatic with Vercel)
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Document API for frontend team
- [ ] Share API documentation URL

## 🌐 Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your domain
3. Configure DNS records as instructed
4. Wait for SSL certificate generation

## 📞 Support

- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- GitHub Issues: Create issue in your repository

## 🎉 Success!

Your Space Station Management System API is now deployed and ready to handle requests from your Angular frontend!

**Your API URLs:**
- Production: `https://your-app.vercel.app`
- Documentation: `https://your-app.vercel.app/docs`
- Health Check: `https://your-app.vercel.app/health`
