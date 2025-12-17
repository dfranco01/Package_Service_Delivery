#Truck class
class Truck:
    #defining all the desired attributes for our trucks
    def __init__(self, capacity, speed, load, packages, mileage, address, depart_time):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time
    #This is the equivalent to Java's toString() method, this is how we want the object printed out
    def __str__(self):
        return f"{self.capacity}{self.speed}{self.load}{self.packages}{self.mileage}{self.address}{self.depart_time}"
