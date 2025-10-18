# Backend Setup Instructions

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## Setup Steps

1. Create a virtual environment:
```bash
# Navigate to the python_backend directory
cd python_backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
Create a file named `.env` in the `python_backend` directory with the following content:
```
MONGODB_URI=mongodb+srv://kylie_lin_nyu:nHNeQssUVF331TFa@ctrl-squad-nyu-swe.9nfst5t.mongodb.net/ctrl-squad-db?retryWrites=true&w=majority
SECRET_KEY=c1050c4a8cc3d6ea4d625c7af7c9bed4961971c6b5d1a3d39f05848b62ce7922
PORT=5000
```

4. Run the Flask application:
```bash
# On Windows PowerShell:
$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"
flask run

# On macOS/Linux:
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

The application should now be running at http://localhost:5000 / http://127.0.0.1:5000

## Troubleshooting

1. If you see "No module named 'app'":
   - Make sure you're in the `python_backend` directory
   - Make sure you've activated the virtual environment
   - Make sure you've installed all requirements
   - Make sure you're using `flask run` and not running Python files directly

2. If you see MongoDB connection errors:
   - Make sure you've created the `.env` file with the correct MongoDB URI
   - Make sure you're in the correct directory when running the application

3. If your virtual environment isn't working:
   - Delete the `venv` folder
   - Create a new virtual environment following the steps above