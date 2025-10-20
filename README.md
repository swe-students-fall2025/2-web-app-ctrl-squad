# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

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

### **[Sprint 1](https://github.com/swe-students-fall2025/2-web-app-ctrl-squad/issues)**

- [ ] As a student, I want to be able to register and login an account on CasaConnect, so that I can review my exchange history and other personal information. (see [#1](/../../issues/1))

- [ ] As a student, I want to have a logout option, so that I can safely navigate out of the application. (see [#5](/../../issues/5))

- [ ] As a student, I want to make/edit/delete a post, so that I can notify others I have supplies to exchange. (see [#4](/../../issues/4))

- [ ] As a student, I want to make/edit/delete a post, so that I can find other people's supplies I might need. (see [#8](/../../issues/8))

- [ ] As a student, I want be able to search and find the textbook from a student that no longer needs it, so that I don’t purchase a new one. (see [#2](/../../issues/2))

- [ ] As a student, I want to see trading confirmations, so that I know I completed an exchange. (see [#12](/../../issues/12))

- [ ] As a student, I want to be able to create a profile with information I want to share about myself, so that other students can learn more about me. (see [#9](/../../issues/9))

- [ ] As a student, I want to be able to see my past posts, exchanges and matches, so that I can keep track of the movements I make within the platform. (see [#5](/../../issues/6))

- [ ] As a student, I want to be able see a post with a product's status (exchanged or available), so that I can save time searching. (see [#10](/../../issues/10))

- [ ] As a student, I want to have a thorough description of the ideal roommate I look for in my profile, so that appropriate matches can be made for a potential candidate. (see [#19](https://github.com/swe-students-fall2025/2-web-app-ctrl-squad/issues/19))

### Sprint 2

- [ ] Example User Story (see [#x](/../../issues/x))

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

# Create .env file (if not already present)
# Create a file named .env with the following content:
# MONGODB_URI=mongodb+srv://kylie_lin_nyu:nHNeQssUVF331TFa@ctrl-squad-nyu-swe.9nfst5t.mongodb.net/ctrl-squad-db?retryWrites=true&w=majority
# SECRET_KEY=c1050c4a8cc3d6ea4d625c7af7c9bed4961971c6b5d1a3d39f05848b62ce7922
# PORT=5000

# Set environment variables and run Flask
# On Windows PowerShell:
$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"
flask run

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
3. If you do have Live Server, you can right click on login.html in the frontend folder and open with Live Server.

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
   - Check if you have proper internet connection to reach MongoDB Atlas

## Task boards

### **[Sprint 1](https://github.com/orgs/swe-students-fall2025/projects/5)**


