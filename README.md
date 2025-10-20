# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more details.

## Team Member

[Amira Adum](https://github.com/amiraadum)  
[Amy Liu](https://github.com/Amyliu2003)  
[Jean Marck](https://github.com/Jeanmarck12)  
[Kylie Lin](https://github.com/kylin1209)  
[Mojin Yuan](https://github.com/Mojin-Yuan)  


## Product vision statement

> CasaConnect connects college students through smart matching. From roommates to resources,  making campus living simpler, safer, and more social.  
> Our vision is to create a world where finding a home, a roommate, or what you need feels effortless and connected.

## User stories

**[See issues](https://github.com/swe-students-fall2025/2-web-app-ctrl-squad/issues)**

## Steps necessary to run the software

### Prerequisites
- Python 3.8 or higher
- Git
- Modern web browser (Chrome, Firefox, Edge, etc.)

### Setup Instructions

#### 1. Clone the repository
```bash
git clone https://github.com/swe-students-fall2025/2-web-app-ctrl-squad.git
cd 2-web-app-ctrl-squad
```

#### 2. Set up and start the Flask backend
```bash
# Navigate to the python_backend directory
cd python_backend

# Install dependencies directly (this is how the application was developed)
pip install -r requirements.txt
```

**Note**: If you're working on multiple Python projects and want to avoid dependency conflicts, you can optionally use a virtual environment:

```bash
# Optional: Create and use a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### Create .env file (if not already present)
#### Create a file named .env with the following content:
```bash
MONGODB_URI=mongodb+srv://kylie_lin_nyu:nHNeQssUVF331TFa@ctrl-squad-nyu-swe.9nfst5t.mongodb.net/ctrl-squad-db?retryWrites=true&w=majority
#SECRET_KEY=c1050c4a8cc3d6ea4d625c7af7c9bed4961971c6b5d1a3d39f05848b62ce7922
PORT=5000



export MONGODB_URI="mongodb+srv://kylie_lin_nyu:nHNeQssUVF331TFa@ctrl-squad-nyu-swe.9nfst5t.mongodb.net/ctrl-squad-db?retryWrites=true&w=majority"

```

```bash
# Set environment variables and run Flask
# On Windows PowerShell:
$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"
flask run
```

```bash
# On Windows Command Prompt:
set FLASK_APP=app
set FLASK_ENV=development
flask run

# On macOS/Linux:
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

You should see output indicating that the Flask server is running at http://127.0.0.1:5000

#### 3. Access the application
Once the Flask server is running, you can access the application by opening the following URL in your browser:

[http://127.0.0.1:5500/src/frontend/login.html](http://127.0.0.1:5500/src/frontend/login.html)

If the above link doesn't work (which might happen if you're not using Live Server with the default port 5500), you can simply open the file directly in your browser:

1. Navigate to the project directory
2. Open the file `src/frontend/login.html` in your web browser
3. If you do have Live Server, you can right-click on login.html in the frontend folder and open it with Live Server.

### Troubleshooting

1. **Flask server issues:**
   - Make sure you're in the `python_backend` directory
   - Check that all dependencies are installed (`pip install -r requirements.txt`)
   - Ensure the `.env` file exists with the correct MongoDB connection string

2. **Frontend connectivity issues:**
   - The Flask server must be running at port 5000
   - CORS is enabled on the backend, so requests from other origins should work
   - Check browser console (F12) for any errors related to API requests

3. **Database connection issues:**
   - Verify the MongoDB connection string in your `.env` file
   - Check if you have a proper internet connection to reach MongoDB Atlas

## Task boards

### **[Sprint 1](https://github.com/orgs/swe-students-fall2025/projects/5)**


### **[Sprint 2](https://github.com/orgs/swe-students-fall2025/projects/54)**


