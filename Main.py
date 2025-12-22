# Student ID: 012435854
#David Franco
import csv
from datetime import timedelta
import Truck
from builtins import ValueError

from hashtable import HashTable
from Package import Package

#First, we read in all of our csv files using csv module
with open("CSV/Distance_File.csv") as csvfile:
    CSV_Distance = csv.reader(csvfile)
    CSV_Distance = list(CSV_Distance)


with open("CSV/Address_File.csv") as csvfile1:
    CSV_Address = csv.reader(csvfile1)
    CSV_Address = list(CSV_Address)


with open("CSV/Package_File.csv") as csvfile2:
    CSV_Package = csv.reader(csvfile2)
    CSV_Package = list(CSV_Package)


#this function uses package csv file to initialize a packages object, then place them into data structure
def initialize_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline_time = package[5]
            pWeight = package[6]
            pNotes = package[7]

            
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pNotes)
            
            package_hash_table.insert(pID, p)


#finding distance between two points
def distance_in_between_points(x_value, y_value):
    distance = CSV_Distance[x_value][y_value]
    if distance == '':
        distance = CSV_Distance[y_value][x_value]

    return float(distance)


#extracting address number from the adress string literal
def extract_address_number(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])


#Manually Loading Trucks
truck1 = Truck.Truck(1, 16, 18, None, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                     timedelta(hours=8))


truck2 = Truck.Truck(2, 16, 18, None, [3, 6, 9, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                     "4001 South 700 East", timedelta(hours=10, minutes=20))


truck3 = Truck.Truck(3, 16, 18, None, [2, 4, 5, 6, 7, 8, 12, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
                     timedelta(hours=9, minutes=5))

#instantiating a hash table
package_hash_table = HashTable()

# calling function and loading packages into data structure
initialize_package_data("CSV/Package_File.csv", package_hash_table)


#Assigning truck IDs to the packages
trucks = [truck1, truck2, truck3]
for truck in trucks:
    for packageid in truck.packages:
        package = package_hash_table.lookup(packageid)
        if package:
            package.truck_id = truck.id

#Formatting and printing all needed package info
def print_pack_info(package):
    print("=" * 50)
    print("PACKAGE ID: " + str(package.ID))
    print("ADDRESS: " + package.address)
    print("CITY: " + package.city)
    print("STATE: " + package.state)
    print("ZIP: " + package.zipcode)
    print("DEADLINE: " + package.Deadline_time)
    print("WEIGHT: " + package.weight)
    print("STATUS: " + package.status)
    print("DEPART TIME: " + str(package.departure_time))
    print("DELIVERY TIME: " + str(package.delivery_time))
    print("TRUCK ID: " + str(package.truck_id))
    print("=" * 50)

#comparing query time to delivered and depart times to return the appropriate status
def update_status(convert_timedelta, package):

    if package.ID == 9 and convert_timedelta >= timedelta(hours=10, minutes=20):
        package.address = "410 S State St"
        package.city = "Salt Lake City"
        package.state = "UT"
        package.zip = "84111"
    if package.delivery_time < convert_timedelta:
        package.status = "Delivered"
    elif package.arrival_time and package.arrival_time > convert_timedelta:
        package.status = "delayed"
    elif package.departure_time > convert_timedelta:
            package.status = "En route"
    else:
        package.status = "At Hub"

    return package



def execute_delivery(truck):
    #intitializing an empty array of not delivered packages
    not_delivered = []
    for packageID in truck.packages:
        package = package_hash_table.lookup(packageID)
        not_delivered.append(package)
    #clear the truck packages so we can rearrange them into truck using nearest neighbor
    truck.packages.clear()


    #this function continues executing as long as there are still packages needing to be delivered
    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None
        #implementing nearest neighbor
        for package in not_delivered:
            if distance_in_between_points(extract_address_number(truck.address), extract_address_number(package.address)) <= next_address:
                next_address = distance_in_between_points(extract_address_number(truck.address), extract_address_number(package.address))
                next_package = package
            # Packages 6, 25, 28, 32 are delayed and arrive at 9:05 AM
            if package.ID in [6, 25, 28, 32]:
                package.arrival_time = timedelta(hours=9, minutes=5)
                package.status = "delayed"  # Package is in transit, not at hub yet
            


        #rearranging the truck's packages array, placing the next closest one first
        truck.packages.append(next_package.ID)
        #removing that same package from the pending array
        not_delivered.remove(next_package)
        #logging truck's miles and next destination to be visited
        truck.mileage += next_address
        truck.address = next_package.address
        #logging the next package's tracking info
        truck.time += timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time


#loading process commencement
execute_delivery(truck1)
execute_delivery(truck2)
#constraint added to ensure third truck does not take off until either of the previous two trucks have completed
truck3.depart_time = min(truck1.time, truck2.time)
execute_delivery(truck3)


class Main:
    #introduction of user interface
    print("*" * 50)
    print("Western Governors University Parcel Service (WGUPS)")
    print("*" * 50)
    print("The mileage for the route is:")
    print(truck1.mileage + truck2.mileage + truck3.mileage)  
    
    text = input("To start please type the word 'time' (All else will cause the program to quit).")
    
    if text == "time":
        try:
            #the user is asked to enter a specific time in a specific format
            user_time = input("Please enter a time to check status of package(s). Use the following format, HH:MM:SS")
            (h, m, s) = user_time.split(":")
            convert_timedelta = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            #the user may check the status of one package or of all of them
            second_input = input("To view the status of an individual package please type 'solo'. For a rundown of all"
                                 " packages please type 'all'.")
            #here the user picks one package, the user may then look it up by ID
            if second_input == "solo":
                try:
                    solo_input = input("Enter the numeric package ID")
                    package = package_hash_table.lookup(int(solo_input))
                    package = update_status(convert_timedelta, package)
                    print_pack_info(package)
                except ValueError:
                    print("Entry invalid. Closing program.")
                    exit()
            #here the user selects to view the status of all packages
            elif second_input == "all":
                try:
                    for packageID in range(1, 41):
                        package = package_hash_table.lookup(packageID)
                        package = update_status(convert_timedelta, package)
                        print_pack_info(package)
                #value errors included so that the program may exit gracefully in all cases of invalid input
                except ValueError:
                    print("Entry invalid. Closing program.")
                    exit()
            else:
                exit()
        except ValueError:
            print("Entry invalid. Closing program.")
            exit()
    elif input != "time":
        print("Entry invalid. Closing program.")
        exit()
