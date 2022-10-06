# Python weekend entry task

**This scrip solve partially the task entry provided by Kiwi.com to attend python weekend in BCN**

### Description
Data provided have the following columns:
- `flight_no`: Flight number.
- `origin`, `destination`: Airport codes.
- `departure`, `arrival`: Dates and times of the departures/arrivals.
- `base_price`, `bag_price`: Prices of the ticket and one piece of baggage.
- `bags_allowed`: Number of allowed pieces of baggage for the flight.

To be able to run this script, you should provide some inputs

| Argument name | type    | Description              | Notes                        |
|---------------|---------|--------------------------|------------------------------|
| `path_to_data`| string  | Path to csv data         |                              |
| `origin`      | string  | Origin airport code      |                              |
| `destination` | string  | Destination airport code |                              |
| `bags`        | int     | Number of luggages       | optional (default = 0)       |
| `return`      | boolean | Is it a return flight?   | optional (default = false)   |

##### How to run the script
This is a script that works as a module:

```
python3 -m solution example/example0.csv RFZ WIW --bags=1 -return
```
will perform a search RFZ -> WIW -> RFZ for flights which allow at least 1 piece of baggage.

#### Output
The output will be a json-compatible structured list of trips sorted by price. The trip has the following schema:
| Field          | Description                                                   |
|----------------|---------------------------------------------------------------|
| `flights`      | A list of flights in the trip according to the input dataset. |
| `origin`       | Origin airport of the trip.                                   |
| `destination`  | The final destination of the trip.                            |
| `bags_allowed` | The number of allowed bags for the trip.                      |
| `bags_count`   | The searched number of bags.                                  |
| `total_price`  | The total price for the trip.                                 |
| `travel_time`  | The total travel time.                                        |



```bash
python3 -m solution example/example0.csv WIW ECV --bags=1
```
and get the following result:

```json
[
    {"flights": 
        {
         "flight_no": "ZH151",
         "origin": "WIW", 
         "destination": "ECV", 
         "departure": "2021-09-11T07:25:00", 
         "arrival": "2021-09-11T12:35:00", 
         "base_price": "245.0", 
         "bag_price": "12", 
         "bags_allowed": "2"
         }, 

         "bags_allowed": 2, 
         "bags_count": 1, 
         "destination": "ECV", 
         "origin": "WIW", 
         "total_price": 257.0, 
         "travel_time": "5:10:00"
    }
]
```
#### Runing a flight with return 
```bash
python3 -m solution example/example0.csv WIW ECV --bags=1 -return
```
and get the following result:

```json

[
    {"go": 
        {"flights": 
            {
                "flight_no": "ZH151", 
                "origin": "WIW", 
                "destination": "ECV", 
                "departure": "2021-09-11T07:25:00", 
                "arrival": "2021-09-11T12:35:00", 
                "base_price": "245.0", 
                "bag_price": "12", 
                "bags_allowed": "2"
            }, 
            "bags_allowed": 2, 
            "bags_count": 1, 
            "destination": "ECV", 
            "origin": "WIW", 
            "total_price": 257.0, 
            "travel_time": "5:10:00"
        }, 
    "back": 
        {"flights": 
            {
                "flight_no": "ZH151", 
                "origin": "ECV", 
                "destination": "WIW", 
                "departure": "2021-09-11T15:35:00", 
                "arrival": "2021-09-11T20:45:00", 
                "base_price": "245.0", 
                "bag_price": "12", 
                "bags_allowed": "2"
            }, 
            "bags_allowed": 2, 
            "bags_count": 1, 
            "destination": "ECV", 
            "origin": "WIW", 
            "total_price": 257.0, 
            "travel_time": "5:10:00"
        }
    }
]
```
#### Aditional things
- If you give bad data, the code will return (`Data path is not valid or doesnt exist`)
- If you provide a origin or destination which is not in data, the code will return a message telling about that (`Your origin fligth WIW or destination ECVA is not in data`)