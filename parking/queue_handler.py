# =====================================================
# WAITING QUEUE
# =====================================================

waiting_queue = []


# =====================================================
# ADD VEHICLE TO QUEUE
# =====================================================

def add_to_queue(vehicle_number):

    if vehicle_number not in waiting_queue:
        waiting_queue.append(vehicle_number)


# =====================================================
# REMOVE FIRST VEHICLE
# =====================================================

def get_next_vehicle():

    if waiting_queue:
        return waiting_queue.pop(0)

    return None