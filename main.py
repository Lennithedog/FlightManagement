import sqlite3
import pandas as pd
import installdb as db

"""Debug flag to output actual SQL query"""
DEBUG = 0

def print_data(sql, conn):
    """Helper function for reading from sqlite and printing to screen"""
    if DEBUG:
        print(sql)
    data = pd.read_sql_query(sql, conn)
    print(data)

def view_flights(conn):
    """ main view of flight schedule connecting all the relevant tables """
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
            query += " WHERE dp.City='" + airport_code + "'"
        case '2':
            status = input("Status: ")
            query += " WHERE s.StatusText LIKE '" + status + "'"
        case '3':
            departure_date = input("Departure Date: ")
            query += " WHERE dp.DepartureDatetime LIKE '" + departure_date + "*'"
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
    print_data("SELECT * from v_pilot_schedule", conn)

def view_reports(conn):
    """view flight information aggregated by a criteria"""
    print("[1] Number of flights by destination")
    print("[2] Number of flights by pilot")
    print("[0] Return to main menu")
    criteria = input(": ");
    query = "SELECT Departure,COUNT(*) as [Number of Flights] FROM (SELECT * FROM v_pilot_schedule)"
    match criteria:
        case '1':
            query = query + " GROUP BY Departure"
        case '2':
            query = query + " GROUP BY PilotId"
        case '0':
            return
        case _:
            print("Invalid option")
            view_reports(conn)

    print_data(query, conn)

def update_destination(conn):
    """update destination information and commit to database if successful, else rollback the transaction"""
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
    """update pilot schedule and commit to database if successful, else rollback the transaction"""
    flight_id = input("Flight Id: ")
    pilot_id = input("Pilot Id: ")
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PilotSchedule VALUES (?,?)", (flight_id, pilot_id))
    except Exception as e:
        print("Unable to assign pilot ")
        print(e)
        conn.rollback()       
    view_pilot_schedule(conn)

def delete_destination(conn):
    """delete destination"""
    airport_id = input("AirportId: ")
    data = pd.read_sql_query("SELECT * FROM Airport WHERE AirportId=" + airport_id, conn)
    if(len(data.index) > 0):
           cursor = conn.cursor()
           cursor.execute("DELETE FROM Airport WHERE AirportId=?", airport_id)
           view_destinations(conn)
    else:
        print("Invalid AirportId")
        return

def update_flight(conn):
    """update flight information and commit to database if successful, else rollback the transaction"""
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

    try:
        query = "UPDATE Flight SET " + column + "=" + value + " WHERE FlightId=" + flight_id
        if DEBUG:
            print(query)
        conn.execute(query)
    except Exception as e:
        print("Unable to update flight ")
        print(e)
        conn.rollback()
        
    view_flights(conn)

def add_flight(conn):
    """add flight and commit to database if successful, else rollback the transaction"""
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
    """helper function print main menu"""
    print("\n")
    print("[1] Add a New Flight")
    print("[2] View Flights by Criteria")
    print("[3] Update Flight Information")
    print("[4] Assign Pilot to Flight")
    print("[5] View Pilot Schedule")
    print("[6] View Destination Information")
    print("[7] Update Destination Information")
    print("[8] Delete Destination Information")
    print("[9] Reports")
    print("[0] Exit")

def main():
    """connect to the database and call installdb.py libraries to create database schema and populate data"""
    """in production this would only be called once at installation"""
    conn = sqlite3.connect('FlightManagement')
    db.create_database(conn)
    db.create_data(conn)
    db.create_views(conn)
    
    selection = '-1'
    while selection != '0':
        """entry point for the application, print main menu and """
        """then called function based on user selection"""
        """return to the main menu until the user exits"""
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
            case '8':
                delete_destination(conn)
            case '9':
                view_reports(conn)
            case '0':
                return
            case _:
                print("Invalid option")
    """close connection to the database upon exit"""
    conn.close()

if __name__ == "__main__":
    main()