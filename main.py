import os
import sqlite3
import pandas as pd
import installdb as db

def print_data(sql, conn):
    data = pd.read_sql_query(sql, conn)
    print(data)

def view_flights(conn):
    print("View Flight By:")
    print("[1] Destination")
    print("[2] Status")
    print("[3] Departure Date")
    print("[4] All")
    print("[0] Return to main menu")
    query = "SELECT f.FlightId,a.AircraftMakeModel,dep.City as Departure,f.DepartureDatetime as Departing,arr.City as Arrival,s.StatusText as Status " \
            "FROM Flight f " \
            "LEFT JOIN Aircraft a ON f.AircraftId=a.AircraftId " \
            "LEFT JOIN Airport dep ON f.DepartureAirportId=dep.AirportId " \
            "LEFT JOIN Airport arr ON f.ArrivalAirportId=arr.AirportId " \
            "LEFT JOIN Status s ON f.StatusId=s.StatusId"
    criteria = input(": ");
    where = ""
    match criteria:
        case '1':
            airport_code = input("Airport Code: ")
            query + " WHERE dp.City=" + airport_code
        case '2':
            status = input("Status: ")
            query + " WHERE f.StatusText" + status
        case '3':
            departure_date = input("Departure Date: ")
            query + " WHERE dp.DepartureDateime LIKE " + departure_date + "*"
        case '4':
            query
        case '0':
            return
        case _:
            print("Invalid option")
            view_flights(conn)

    print_data(query, conn)

def view_destinations(conn):
    print_data("SELECT * FROM Airport", conn)

def view_pilot_schedule(conn):
    print_data("SELECT p.FirstName, p.LastName as Name, a.City as Departure, DepartureDatetime as Departing FROM Pilot p "
                "INNER JOIN PilotSchedule s on p.PilotId=s.PilotId "
                "LEFT JOIN Flight f on s.FlightId=f.FlightId "
                "LEFT JOIN Airport a on a.AirportId=f.DepartureAirportId", conn)

def update_destination(conn):
    airport_code = input("Airport Code: ")
    city = input("City: ");
    country = input("Country: ");
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Airport SET City=?, Country=? WHERE AirportCode=?", (city, country, airport_code))
    except Exception as e:
        print("Unable to update destination")
        print(e)
        conn.rollback()
        
    view_destinations(conn)

def update_pilot_schedule(conn):
    flight_id = input("Flight Id: ")
    pilot_id = input("Pilot Id: ")
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PilotSchedule VALUES (?,?)", (flight_id, pilot_id))
    except Exception as e:
        print("Unable to assign pilot")
        print(e)
        conn.rollback()
        
    view_pilot_schedule(conn)

def update_flight(conn):
    print("Update flight:")
    print("[1] Departure Datetime")
    print("[2] Status")
    print("[0] Return to main menu")
    
    field = input(": ")
    flight_id = input("FlightId: ")

    match field:
        case '1':
            value = input("New Departure Datetime: ")
            column = 'DepartureDatetime'
        case '2':
            # TODO: print values here
            value = input("StatusId: ")
            column = 'StatusId'
        case '0':
            return
        case _:
            print("Invalid option")
    
    view_flights(conn)

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE Flight SET "+column+"=? WHERE FlightId=?", (value, flight_id))
    except Exception as e:
        print("Unable to update flight")
        print(e)
        conn.rollback()
        
    view_flights(conn)

def add_flight(conn):
    # TODO: make this more user-friendly by allowing inputs other than fk id
    aircraft_id = input("AircraftId: ")
    departure_id = input("DepartureId: ")
    departure_datetime = input("Departure Datetime: ")
    arrival_id = input("ArrivalId: ")
    arrival_datetime = input("Arrival Datetime: ")
    try:
        insert = "INSERT INTO Flight (AircraftId, DepartureAirportId, DepartureDatetime, ArrivalAirportId, ArrivalDatetime) VALUES (?, ?, ?, ?, ?)"
        conn.execute(insert, (aircraft_id, departure_id, departure_datetime, arrival_id, arrival_datetime))
        conn.commit()     
    except Exception as e:
        print("Unable to add flight")
        print(e)
        conn.rollback()

def print_menu():
    print("\n")
    print("[1] Add a New Flight")
    print("[2] View Flights by Criteria")
    print("[3] Update Flight Information")
    print("[4] Assign Pilot to Flight")
    print("[5] View Pilot Schedule")
    print("[6] View Destination Information")
    print("[7] Update Destination Information")
    print("[0] Exit")

def main():
    conn = sqlite3.connect('FlightManagement')
    db.create_database(conn)
    db.create_data(conn)
    
    selection = '-1'
    #TODO: change to case
    while selection != '0':        
        print_menu()
        selection = input(": ")
        match selection:
            case '1':
                add_flight(conn)
            case '2':
                view_flights(conn)
            case '3':
                update_flight(conn)
            case '4':
                update_pilot_schedule(conn)
            case '5':
                view_pilot_schedule(conn)
            case '6':
                view_destinations(conn)
            case '7':
                update_destination(conn)
            case '0':
                return
            case _:
                print("Invalid option")

    conn.close()

if __name__ == "__main__":
    main()