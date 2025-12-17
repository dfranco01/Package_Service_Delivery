#Package class
import Truck
from typing import Literal
class Package:
    #defining needed attributes
    def __init__(self, ID, address, city, state, zipcode, Deadline_time, weight, notes):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.Deadline_time = Deadline_time
        self.weight = weight
        self.notes = notes
        #self.status = Literal["In transit", "at hub" "En route", "delivered"] = "At hub"
        self.status = "at hub"
        self.departure_time = None #time the package left the hub
        self.delivery_time = None 
        self.arrival_time = None #time the packages arrived at the hub (the late packages)
        self.truck_id = None #truck assigned to deliver this package
    #formatting string representation of object
    def __str__(self):
        return f"PACKAGE ID: {self.ID}, ADDRESS: {self.address}, CITY: {self.city}, STATE: {self.state}, ZIP: {self.zipcode}, DEADLINE TIME: {self.Deadline_time}, WEIGHT: {self.weight}, NOTES: {self.notes} DELIVERY TIME: {self.delivery_time}, STATUS: {self.status}"
    
   
