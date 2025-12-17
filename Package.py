#Package class
class Package:
    #defining needed attributes
    def __init__(self, ID, address, city, state, zipcode, Deadline_time, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.Deadline_time = Deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
    #formatting string representation of object
    def __str__(self):
        return f"{self.ID}{self.address}{self.city}{self.state}{self.zipcode}{self.Deadline_time}{self.weight}{self.delivery_time}{self.status}"
    #comparing passed in time to delivered and depart times to return the appropriate status
    def update_status(self, convert_timedelta):
        if self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time > convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"
