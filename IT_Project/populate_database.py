import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_project.settings')

import django
django.setup()

import random
from locations.models import Vehicle, VehicleType


# Populate virtual data into our database.
# num: Data Amount. 
def populateDB(num):
    vcost = [20, 10, 5]  # Car: 20, Motorcycle: 10, Bike: 5 (per minute in cent).
    car_data = createData('Car', num)
    moto_data = createData('Motorcycle', num)
    bike_data = createData('Bike', num)
    
    database = {'Car': {'data': car_data},
                'Motorcycle': {'data': moto_data},
                'Bike': {'data': bike_data} }
    
    for db_key, db_value in database.items():
        if db_key == 'Car': 
            vcost_index = 0
        elif db_key == 'Motorcycle': 
            vcost_index = 1
        elif db_key == 'Bike':
            vcost_index = 2

        vtype = addVtype(db_key, vtype_cost=vcost[vcost_index])
        for vdata in db_value['data']:
            addVehicle(vtype)
    
    for type in VehicleType.objects.all():
        for vehicle in Vehicle.objects.filter(type=type):
            print(f'- {type}: {vehicle}')


# Add vehicles into our database.
# vtype: Vehicle Type.
def addVehicle(vtype):
    vdata = Vehicle.objects.get_or_create(type=vtype)[0]
    vdata.save()

    return vdata


# Add vehicle types into our database.
# vtype_name: Vehicle Type.  # vtype_cost: Cost when User Books the Vehicle Type.
def addVtype(vtype_name, vtype_cost):
    vtype = VehicleType.objects.get_or_create(name=vtype_name)[0]
    vtype.cost_per_minute_in_cent = vtype_cost
    vtype.save()

    return vtype


# Create license plate number for our vehicles (e.g, AAAABBB).
# AAAA: Denotes Vehicle Type.  # BBB: Denotes Vehicle Number.
# vtype: Vehicle Type.
def createPlate(vtype):
    number = [int(i) for i in range(0, 1000, 1)]
    number_tag = random.choice(number)

    if number_tag < 10: 
        number_tag = ''.join(['00', str(number_tag)])
    elif 10 <= number_tag < 100: 
        number_tag = ''.join(['0', str(number_tag)])
    elif 100 <= number_tag < 1000:
        number_tag = str(number_tag)

    if vtype == 'Car': 
        plate = ''.join(['AUTO-', number_tag])
    elif vtype == 'Motorcycle': 
        plate = ''.join(['MOTO-', number_tag])
    elif vtype == 'Bike': 
        plate = ''.join(['BIKE-', number_tag])
    
    return plate


# Create virtual data for our database.
# vtype: Vehicle Type.  # num: Data Amount.
def createData(vtype, num): 
    vlist = []

    for i in range(0, num, 1): 
        data = {}
        data['name'] = createPlate(vtype)
        vlist.append(data)

    return vlist


# Test the createPlate() function.
# num: Iteration Amount.
def testCreatePlate(num):
    vtype_list = ['Car', 'Motorcycle', 'Bike']

    for vtype in vtype_list: 
        for i in range(0, num, 1): 
            print(vtype, createPlate(vtype))


# Test the createData() function.
# num: Data Amount.
def testCreateData(num): 
    car_data = createData('Car', num)

    for index in range(0, num, 1):
        print("Car", car_data[index]['name'])


if __name__ == '__main__':
    # testCreatePlate(10)
    # testCreateData(5)
    print('Start to execute populate_database script...')
    populateDB()
