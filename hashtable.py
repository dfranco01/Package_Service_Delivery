
class HashTable:
    #initialize constructor
    def __init__(self, initial_capacity=20):
        self.list = []
        for i in range(initial_capacity):
            self.list.append([])

    
    def insert(self, key, item):
        #using built in hash function to create bucket 
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

       #checking if key already exists to update its value
        for kv in bucket_list:  
            if kv[0] == key:
                kv[1] = item
                return True

        #If this is a new key, create a new slot for this bucket
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    #search function
    def lookup(self, key):
        #hashing the passed in key
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        #comparing it with the available buckets for a match
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None  

    #create removal function
    def hash_remove(self, key):
        #hashing the passed in key
        slot = hash(key) % len(self.list)
        destination = self.list[slot]

        #comparing the hash with current buckets for a removal
        if key in destination:
            destination.remove(key)
