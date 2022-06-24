# Angular, Flask, Python, Sqlite App

## Setup
1. Instal Sqlite from [here](https://www.sqlite.org/download.html)
2. Install pyenv from [here](https://github.com/pyenv/pyenv) and install latest python3
3. Install nvm from [here](https://nodejs.org/en/download/package-manager/#nvm) and install node 16
4. In app folder, install package dependencies and build the app:
   ```
   npm install
   npx ng build
   ```
5. In root folder, install Python dependencies
   ```
   pip3 install -r requirements.txt
   ```
6. Run the backend in root folder<br>
   For Mac:
   ```
   FLASK_APP=run.py flask run
   FLASK_DEBUG=1 FLASK_APP=run.py flask run # For debug
   ```
   For Windows:
   ```
   set FLASK_DEBUG=1 # For debug
   set FLASK_APP=run.py
   flask run
   ```
7. Use default admin account to add cleaners: check seed.py to get username/password
8. Register as new user to book cleaners on certain dates