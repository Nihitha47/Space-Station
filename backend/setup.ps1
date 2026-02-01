# Space Station Management System - Setup Script for Windows
# Run this script to set up your development environment

Write-Host "🚀 Space Station Management System - Setup" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check pip installation
Write-Host "`nChecking pip installation..." -ForegroundColor Yellow
$pipVersion = pip --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ pip found: $pipVersion" -ForegroundColor Green
} else {
    Write-Host "❌ pip not found. Please install pip." -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
Write-Host "`nSetting up environment variables..." -ForegroundColor Yellow
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env file from .env.example" -ForegroundColor Green
    Write-Host "⚠️  Please edit .env file with your database credentials!" -ForegroundColor Yellow
} else {
    Write-Host "ℹ️  .env file already exists" -ForegroundColor Blue
}

# Install dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes...`n" -ForegroundColor Gray
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ All dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Summary
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "✨ Setup Complete!" -ForegroundColor Green
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your MySQL database credentials" -ForegroundColor White
Write-Host "2. Create database: mysql -u root -p < database_setup.sql" -ForegroundColor White
Write-Host "3. Run development server: python run_dev.py" -ForegroundColor White
Write-Host "4. Open API docs: http://localhost:8000/docs`n" -ForegroundColor White

Write-Host "Quick Commands:" -ForegroundColor Yellow
Write-Host "  Start server:  python run_dev.py" -ForegroundColor White
Write-Host "  Run tests:     python -m pytest (if tests added)" -ForegroundColor White
Write-Host "  Deploy:        vercel --prod`n" -ForegroundColor White

Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  Quick Start:   QUICKSTART.md" -ForegroundColor White
Write-Host "  Full Docs:     README.md" -ForegroundColor White
Write-Host "  Deploy Guide:  DEPLOYMENT.md" -ForegroundColor White
Write-Host "  Summary:       PROJECT_SUMMARY.md`n" -ForegroundColor White

Write-Host "Happy coding! 🚀" -ForegroundColor Cyan
