# macros 😋 (Macronutrient Food-Finder API)
Full-Stack 'IIFYM' Food Finder REST API + Frontend for Ombre

## Installation and Setup 

1. Clone Repository
2. Create and spin a virtual environment in main directory
```
python3 -m venv venv
source ./venv/bin/activate
```
3. Install the requirements
```
pip install -r requirements.txt
```
4. Run the server
```
cd restserver (necessary for relative database path)
./main.py
```
5. (Optional) Run the client (in a different window)
```
todo
```

## Rest API Documentation (for standalone usage or curiosity purposes)

`BASE_URI = '/api/v1.0'`

### Endpoints:

| Endpoint | Parameters | Response (JSON) |
| --------------- | --------------- | --------------- |
| `/foods` | none | all foods in the database |
| `/foods/<int:fid>` | food ID | food in database matching ID  |
| `/foods/query/...` | see below | foods matching entered parameters |

#### Query String

Example Usage: "foods over 3 grams of protein and 3 grams of sugar."

`URL = BASE_URI + /foods/query/?prt=gt-3&sgr=gt-3`

Response preview:
 ```json
 [
    {
        "id": 9032,
        "name": "Apricots, dried, sulfured, uncooked",
        "weight": 130.0,
        "serving": "1.0 cup, halves",
        "protein": 4.41,
        "fat": 0.66,
        "carbs": 81.43,
        "sugar": 69.47
    },
    {
        "id": 20001,
        "name": "Amaranth grain, uncooked",
        "weight": 193.0,
        "serving": "1.0 cup",
        "protein": 26.17,
        "fat": 13.55,
        "carbs": 125.93,
        "sugar": 3.26
    }
]
 ```
 
 ### Query String Options
| Macronutrient |
| --------------- | 
| Carbs: 'crb'  |
| Protein: 'prt' |
| Fat: 'fat' |
| Sugar: 'sgr'|

| Operation |
| --------------- | 
| greater than : 'gt'  |
| equal to : 'eq' |
| less than : 'lt' |

Format:
```
BASE_URI + '/foods/query/' + ?{macronutrient}={operation}-{numerical value}&...
```

## Technologies Used
- Python
- Flask
- SQLite (w/ SQLAlchemy)
- Bootstrap
