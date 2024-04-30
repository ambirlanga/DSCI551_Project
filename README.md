# DSCI551_Project
Implementation of a scalable friebase database into an Administrator Interface and an User Website.

University of Southern California - DSCI551 Project (Spring 2024)

## Execute Restaurant App
### Option 1
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
  - Admin_Interface (Files used for Login and Admin Grphical Interface)
    - Foody.py (Tkinter Login and Admin GUI)
    - Manager.py (External modules for Admin GUI)
    - 5235253.ico (Icon for Tkinter)

  - Exe
    - Foody.exe (Alternative option to start the application)

  - Website (User Website files)
    - App.jsx (Website Implementation)
   
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
