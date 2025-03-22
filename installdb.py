import csv

def create_database(conn):
    conn.execute("DROP TABLE IF EXISTS Aircraft")
    conn.execute("DROP TABLE IF EXISTS Airport")
    conn.execute("DROP TABLE IF EXISTS Flight")
    conn.execute("DROP TABLE IF EXISTS Pilot")
    conn.execute("DROP TABLE IF EXISTS PilotSchedule")
    conn.execute("DROP TABLE IF EXISTS Status")

    conn.execute("CREATE TABLE 'Aircraft' (AircraftId INTEGER PRIMARY KEY UNIQUE, RegistrationId VARCHAR(255), AircraftMakeModel VARCHAR(255), CountryOfRegistration VARCHAR(3), Capacity INTEGER, Range INTEGER)")
    conn.execute("CREATE TABLE 'Airport' (AirportId INTEGER PRIMARY KEY UNIQUE, AirportCode VARCHAR(3), City VARCHAR(255), Country VARCHAR(255))")
    conn.execute("CREATE TABLE 'Flight' (FlightId INTEGER PRIMARY KEY UNIQUE, AircraftId INTEGER, DepartureAirportId INTEGER, DepartureDatetime TEXT, ArrivalAirportId INTEGER, ArrivalDatetime TEXT, StatusId INTEGER, " + 
            "FOREIGN KEY(AircraftId) REFERENCES Aircraft(AircraftId), " +
            "FOREIGN KEY(DepartureAirportId) REFERENCES Airport(AirportId), " + 
            "FOREIGN KEY(ArrivalAirportId) REFERENCES Airport(AirportId), " +
            "FOREIGN KEY(StatusId) REFERENCES Status(StatusId))")
    conn.execute("CREATE TABLE 'Pilot' (PilotId INTEGER PRIMARY KEY UNIQUE, LicenseNo INTEGER, FirstName VARCHAR(255), LastName VARCHAR(255), Address TEXT, Telephone TEXT)")
    conn.execute("CREATE TABLE 'PilotSchedule' (FlightId INTEGER, PilotId INTEGER, " +
            "FOREIGN KEY(FlightId) REFERENCES Flight(FlightId), " +
            "FOREIGN KEY(PilotId) REFERENCES Pilot(PilotId))")
    conn.execute("CREATE TABLE 'Status' (StatusId INTEGER PRIMARY KEY UNIQUE, StatusText VARCHAR(255))")
    
def create_data(conn):
    conn.execute("INSERT INTO Airport VALUES (1, 'LHR', 'London', 'United Kingdom')")
    conn.execute("INSERT INTO Airport VALUES (2, 'YHZ', 'Halifax', 'Canada')")
    conn.execute("INSERT INTO Airport VALUES (3, 'AMS', 'Amsterdam', 'Netherlands')")
    conn.execute("INSERT INTO Airport VALUES (4, 'BKK', 'Buenos Aires', 'Argentina')")
    conn.execute("INSERT INTO Airport VALUES (5, 'EZE', 'Bangkok', 'Thailand')")
    conn.execute("INSERT INTO Airport VALUES (6, 'KBL', 'Kabul', 'Afghanistan')")
    conn.execute("INSERT INTO Airport VALUES (7, 'SYD', 'Sydney', 'Australia')")
    conn.execute("INSERT INTO Airport VALUES (8, 'NDJ', 'NDjamena', 'Chad')")
    conn.execute("INSERT INTO Airport VALUES (9, 'HEL', 'Helsinki', 'Finland')")
    conn.execute("INSERT INTO Airport VALUES (10, 'SSH', 'Sharm El Sheikh', 'Egypt')")

    conn.execute("INSERT INTO Flight VALUES (1, 2, 1, '2025-03-24 09:00:00 UTC', 2, '2025-03-23 15:00:00 UTC', 4)")
    conn.execute("INSERT INTO Flight VALUES (2, 9, 2, '2025-03-24 10:00:00 UTC', 10, '2025-03-24 14:00:00 UTC', 1)")
    conn.execute("INSERT INTO Flight VALUES (3, 3, 3, '2025-03-24 17:00:00 UTC', 1, '2025-03-24 19:00:00 UTC', 2)")
    conn.execute("INSERT INTO Flight VALUES (4, 6, 1, '2025-03-25 14:00:00 UTC', 8, '2025-03-25 22:00:00 UTC', 6)")

    conn.execute("INSERT INTO Status (StatusText) VALUES ('Gate Closed')")
    conn.execute("INSERT INTO Status (StatusText) VALUES ('Gate Open')")
    conn.execute("INSERT INTO Status (StatusText) VALUES ('Boarding')")
    conn.execute("INSERT INTO Status (StatusText) VALUES ('Delayed')")
    conn.execute("INSERT INTO Status (StatusText) VALUES ('Cancelled')")
    conn.execute("INSERT INTO Status (StatusText) VALUES ('On Time')")
    
    cursor = conn.cursor()

    file = open('data/Aircraft.csv')
    contents = csv.reader(file)
    
    cursor.executemany("INSERT INTO Aircraft (RegistrationId, AircraftMakeModel, CountryOfRegistration, Capacity, Range) VALUES(?, ?, ?, ?, ?)", contents)

    file = open('data/Pilot.csv')
    contents = csv.reader(file)
    
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO Pilot (LicenseNo, FirstName, LastName, Address, Telephone) VALUES(?, ?, ?, ?, ?)", contents)
    
    file = open('data/PilotSchedule.csv')
    contents = csv.reader(file)
    
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO PilotSchedule (FlightId, PilotId) VALUES(?, ?)", contents)

    conn.commit()