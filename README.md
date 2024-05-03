# DSCI551_Project
Implementation of a scalable friebase database into an Administrator Interface and an User Website.

University of Southern California - DSCI551 Project (Spring 2024)

## Log In Options

When executing the app you can use the following existing identification parameters to Log In as an User (Website) and Admin (UI):

  - User 
    - Username: aaa
    - Password: bbb
  - Admin
    - Username: Ariel
    - Password: 1234

## Execute Restaurant App
### Option 1 (Recommended)
  - Python3 must be installed.
  - Download requirements.txt and the Admin_interface folder.
  - Install requirements ('pip' must be previously installed):
```shell
pip install -r requirements.txt
```
  - If on windows tkinter should already be installed, if using Linux/Mac/Similar:
```shell
sudo apt-get install python3-tk
```
  - Finally execute "Foody.py" (in same folder as "Manager.py" and .ico)
```shell
python Foody.py
```
### Option 2 (Windows)
  - Downloade the .exe (in the Exe folder) and execute it (Unavialable in MacOs) (Not Tested in Linux)

## File Structure
  - *Admin_Interface* (Files used for Login and Admin Grphical Interface)
    - Foody.py (Tkinter Login and Admin GUI)
    - Manager.py (External modules for Admin GUI)
    - 5235253.ico (Icon for Tkinter)

  - *Exe*
    - Foody.exe (Alternative option to start the application)

  - *Website* (Files used for Web App: https://dsci551projecttesting.netlify.app)
    - firebase.db1.config.js (Sets connection to restaurant database 1)
    - firebase.db2.config.js (Sets connection to restaurant database 2)
    - index.html (Web application Entry Point)
    - package-lock.json (Snapshot for dependencies and versions required - Ensures consistency across enviroments)
    - package.json (Snapshot for dependencies and versions required - Ensures consistency across enviroments)
    - postcss.config.js (PostCSS configuration file - tool for transforming CSS with JS plugins)
    - tailwind.config.js
    - vite.config.js
    - *src*
      - App.jsx (Main application logic, handles frontend actions and web interaction)
      - App.css (Website stylesheet - Visuals & Layout)
      - Index.css (Website stylesheet - Visuals & Layout)
      - main.jsx (Initialize React app and sets the root element where application will be rendered)
      - utils.js
      - *assets*
        . reacts.svg
    - *public*
      - vite.svg (Web icon)
   
  - README.md
      
  - requirements.txt (Libraries required to execute Admin_Interface files)
    



## Work Division
### Chuanzhou(Austin) Zhang:
  - Manager.py: modules(delete_restaurant)
  - Website: Complete implementation (in collaboration with Kenneth)

### Kenneth Chan:
  - Manager.py: modules(add_restaurant)
  - Website: Complete implementation (in collaboration with Austin)

### Ariel Martinez Birlanga:
  - Manager.py: modules(simpleHash, modify_restaurant, hash_Restaurant, filter_restaurant)
  - Foody.py: Complete implementation
