# DSCI551_Project

## Excute Restaurant App
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
  - Finally execute "Foody.py" (in same folder as "Manager.py" and .io)
```shell
python Foody.py
```
### Option 2 (Windows)
  - Downloade the .exe (in the Exe folder) and execute it (Unavialable in MacOs) (Not Tested in Linux)

## File Structure
DSCI551Project
  - Admin_Interface (Files used for Login and Admin Grphical Interface)
    - Foody.py
    - Manager.py
  - Website (User Website files)
  - Exe
    - Foody.exe 
  - requirements.txt
  - README.md


## Work Division
### Chuanzhou(Austin) Zhang:
  -Manager.py: modules(delete_restaurant)
  -Website: Complete implementation (in collaboration with Kenneth)

### Kenneth Chan:
  -Manager.py: modules(add_restaurant)
  -Website: Complete implementation (in collaboration with Austin)

### Ariel Martinez Birlange:
  -Manager.py: modules(simpleHash, modify_restaurant, hash_Restaurant, filter_restaurant)
  -Foody.py: Complete implementation*
