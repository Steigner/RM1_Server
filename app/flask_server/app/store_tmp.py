# store classes:
#   input: none
# Note: This clasees is used as simple approach how to store some identificator,
# across all app and routes

# store id for search patient in database
class StoreID:
    id = 0

    def __init__(self):
        pass


# store IP adress, for acces to data's from robot
class StoreIP:
    ip = "none"

    def __init__(self):
        pass


# store Camera plugin
class StoreCam:
    cam = "none"

    def __init__(self):
        pass


# store Validation for identification in FaceID
class Validation:
    val = False

    def __init__(self):
        pass


# store counter, just for how many times, is reload menu route
# Note: No neccesary
class Counter:
    counter = 0

    def __init__(self):
        pass


# Point to save searched point in 3D reconstruction
class Point:
    point = []

    def __init__(self):
        pass


# Point to save searched point in 3D reconstruction
class Sim:
    sim = False

    def __init__(self):
        pass

class DoneP:
    done = False

    def __init__(self):
        pass
