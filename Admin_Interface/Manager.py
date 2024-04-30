
# CREDITS
# Ariel: simpleHash, modify_restaurant, Hash_Restaurant, filter_restaurant
# Keneth: add_restaurant
# Austin: delete_restaurant


# IMPORT LIBRARIES
import json
import requests
import sys

# Firebase Database URLs (Replace these URLs with your actual Firebase URLs)
DATABASE_URLS = {
    0: "https://asi1-99476-default-rtdb.firebaseio.com",
    1: "https://asi1b-5445c-default-rtdb.firebaseio.com"
}

## Define any global methods

#Hash by ascii value of first letter
#An elif will be added for every extra database, and in case there is at least 1 database per letter (lowercase 97-122), we will start analyzing the ascii value of the second character
def simpleHash(name):
    if ord(name[0].lower()) > 109:
        return 1
    else:
        return 0
    #return len(name)%2


def add_restaurant(name, type_of_food, location):
    # Construct the restaurant JSON data including the name
    restaurant_data = {
        "Name": str(name),  # Add the restaurant name here
        "Score": {
            "Stars": 0.0,
            "Likes": 0,
            "Dislikes": 0,
            "Num of score": 0
        },
        "Type of food": str(type_of_food),
        "Location": str(location)
    }
    # Convert restaurant data to JSON
    restaurant_json = json.dumps(restaurant_data)

    # Determine the database index based on the location
    database_index = simpleHash(str(name))
    # change the URL as needed
    database_url = f"{DATABASE_URLS[database_index]}/restaurants.json"

    # Make the HTTP PUT request
    response = requests.post(database_url, data=restaurant_json)
    if response.status_code == 200:
        ide = response.json()['name']
    else:
        ide = 0
    return response.status_code, ide


def delete_restaurant(id,name):
    db = simpleHash(name)
    url = f"{DATABASE_URLS[db]}/restaurants/{id}.json"
    response = requests.delete(url)
    return response.status_code

#def delete_restaurant_id(i):
#    for v in DATABASE_URLS.values():
#        try:
#            response = requests.delete(f"{v}/restaurants/{i}.json")
#            print(f"Restaurant with ID {i} deleted successfully from {v}.")
#             return response.status_code
#        except requests.exceptions.RequestException as e:
#            print(f"Error deleting restaurant  with ID {i} from {v}: {e}")
#            return -1


def modify_restaurant(id, name, type, location, oldname, star, li, di, nu):

    restaurant_data = {
        "Name": str(name),  
        "Score": {
            "Stars": float(star),
            "Likes": int(li),
            "Dislikes": int(di),
            "Num of score": int(nu)
        },
        "Type of food": str(type),
        "Location": str(location)
    }

    # Convert restaurant data to JSON
    db = simpleHash(str(name))
    db2 = simpleHash(str(oldname))
    if db == db2:
        restaurant_json = json.dumps(restaurant_data)
        url = f"{DATABASE_URLS[db]}/restaurants/{id}.json"
        ans = requests.patch(url, restaurant_json)
        return ans.status_code, id
    else:
        url = f"{DATABASE_URLS[db2]}/restaurants/{id}/Score.json"
        ans0 = requests.get(url)
        restaurant_data["Score"] = json.loads(json.dumps(ans0.json()))
        restaurant_json = json.dumps(restaurant_data)
        url = f"{DATABASE_URLS[db]}/restaurants/{id}.json"
        ans = requests.put(url, restaurant_json)
        url = f"{DATABASE_URLS[db2]}/restaurants/{id}.json"
        ans2 = requests.delete(url)
        if ans.status_code == 200: ide = id
        else: ide = 0
        return ans.status_code, ide
    
#Re-hash uncorrectly hashed rows (useful when adding new databases that will change the hash values of existing data)
def hash_restaurant(id, name, type, location, star, li, di, nu):

    restaurant_data = {
        "Name": str(name),  
        "Score": {
            "Stars": float(star),
            "Likes": int(li),
            "Dislikes": int(di),
            "Num of score": int(nu)
        },
        "Type of food": str(type),
        "Location": str(location)
    }

    # Ifcorrect database patch, if other database delete
    db = simpleHash(str(name))
    for k in DATABASE_URLS.keys():
        if k != db:
            restaurant_json = json.dumps(restaurant_data)
            url = f"{DATABASE_URLS[k]}/restaurants/{id}.json"
            ans = requests.get(url, restaurant_json)
            if ans.json() != None:
                ans = requests.delete(url)
                url = f"{DATABASE_URLS[db]}/restaurants/{id}.json"
                res = requests.put(url, restaurant_json)
    return


#Filter restaurants given an action (equalTo,startAt...) and their respective value
#If filter by name and equalTo 
def filter_restaurant(b,name,path):
    res = []
    if b:
        db = simpleHash(name)
        url = f"{DATABASE_URLS[db]}/restaurants" + path
        ans=requests.get(url)
        if ans.status_code == 200:
            res.append(ans.json())
    else:
        for v in DATABASE_URLS.values():
            url = f"{v}/restaurants" + path
            ans=requests.get(url)
            if ans.status_code == 200:
                res.append(ans.json())
    return res, ans.status_code
        


# Used to test code at the start of the project
if __name__ == "__main__":
    operation = sys.argv[1].lower()
    if operation == "modify":
        result = modify_restaurant(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        print(result)
    elif operation == "add":
        result = add_restaurant(sys.argv[2], sys.argv[3], sys.argv[4])
        print(result)
