# Setup Documentation

This folder contains all setup-related files for the Platform Engineering API.

## 📁 Files Overview

### **Installation Scripts**
- `install.py` - Main installation script for all dependencies
- `test_api.py` - Test suite and API server for verification
- `setup.py` - Legacy setup script (alternative to install.py)
- `setup_database.py` - Database initialization script

### **Configuration**
- `env.example` - Environment variables template

### **Documentation**
- `SETUP_GUIDE.md` - Main setup guide
- `SETUP_STEP_BY_STEP.md` - Detailed step-by-step instructions
- `FREE_TIER_SETUP.md` - Free tier setup guide
- `COST_OPTIMIZATION_GUIDE.md` - Cost optimization strategies

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
python setup/install.py
```

### **2. Test Installation**
```bash
python setup/test_api.py
```

### **3. Run the API**
```bash
python -m uvicorn setup.test_api:app --reload
```

## 📋 Setup Options

### **Option 1: Simple Setup (Recommended)**
1. Run `python setup/install.py`
2. Run `python setup/test_api.py`
3. Start the API with `python -m uvicorn setup.test_api:app --reload`

### **Option 2: Full Setup with Database**
1. Follow `SETUP_GUIDE.md`
2. Run `python setup/setup_database.py`
3. Configure environment variables using `env.example`

### **Option 3: Free Tier Setup**
1. Follow `FREE_TIER_SETUP.md` for zero-cost setup
2. Use local tools instead of cloud services

### **Option 4: Cost-Optimized Setup**
1. Follow `COST_OPTIMIZATION_GUIDE.md`
2. Minimize AWS costs while maintaining functionality

## 🔧 Environment Configuration

Copy the environment template and configure it:
```bash
cp setup/env.example .env
# Edit .env with your actual values
```

## 📚 Documentation

- **`SETUP_GUIDE.md`** - Main setup guide with troubleshooting
- **`SETUP_STEP_BY_STEP.md`** - Detailed instructions for complete setup
- **`FREE_TIER_SETUP.md`** - How to set up everything for free
- **`COST_OPTIMIZATION_GUIDE.md`** - Cost optimization strategies

## 🎯 Next Steps

After setup, you can:
1. Explore the API at http://localhost:8000/docs
2. Create services using the platform
3. Set up CI/CD pipelines
4. Configure monitoring and alerts

---

**Note**: All setup scripts are designed to work with Python 3.11+ and handle compatibility issues automatically.
