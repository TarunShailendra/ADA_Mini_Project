from flask import Flask, render_template, request

from parking.allocation import (
    all_slots,
    available_slots,
    parked_vehicles,
    park_vehicle,
    remove_vehicle,
    search_vehicle
)

from parking.queue_handler import (
    waiting_queue,
    add_to_queue
)

from parking.pricing import calculate_price

app = Flask(__name__)


# =====================================================
# HOME PAGE
# =====================================================

@app.route('/')
def home():

    occupied_slots = len(parked_vehicles)

    total_slots = occupied_slots + len(available_slots)

    parking_price = calculate_price(
        total_slots,
        occupied_slots
    )

    return render_template(
        'dashboard.html',
        all_slots=all_slots,
        available_slots=available_slots,
        parked_vehicles=parked_vehicles,
        waiting_queue=waiting_queue,
        parking_price=parking_price,
        message=None,
        alert_type=None
    )


# =====================================================
# PARK VEHICLE
# =====================================================

@app.route('/park', methods=['POST'])
def park():

    vehicle_number = request.form['vehicle_number'].upper()

    result = park_vehicle(vehicle_number)

    # Duplicate vehicle
    if result == "ALREADY_PARKED":

        message = f"{vehicle_number} is already parked!"
        alert_type = "danger"

    # Parking full
    elif result is None:

        add_to_queue(vehicle_number)

        message = f"Parking Full! {vehicle_number} added to waiting queue."
        alert_type = "warning"

    # Success
    else:

        message = f"{vehicle_number} allocated Slot {result}"
        alert_type = "success"

    occupied_slots = len(parked_vehicles)

    total_slots = occupied_slots + len(available_slots)

    parking_price = calculate_price(
        total_slots,
        occupied_slots
    )

    return render_template(
        'dashboard.html',
        all_slots=all_slots,
        available_slots=available_slots,
        parked_vehicles=parked_vehicles,
        waiting_queue=waiting_queue,
        parking_price=parking_price,
        message=message,
        alert_type=alert_type
    )


# =====================================================
# REMOVE VEHICLE
# =====================================================

@app.route('/remove/<vehicle_number>')
def remove(vehicle_number):

    removed_slot = remove_vehicle(vehicle_number)

    if removed_slot:

        message = f"{vehicle_number} removed from Slot {removed_slot}"
        alert_type = "info"

    else:

        message = f"{vehicle_number} not found!"
        alert_type = "danger"

    # Auto allocate from queue
    if waiting_queue and available_slots:

        next_vehicle = waiting_queue.pop(0)

        slot = park_vehicle(next_vehicle)

        message += f" | {next_vehicle} allocated Slot {slot}"

    occupied_slots = len(parked_vehicles)

    total_slots = occupied_slots + len(available_slots)

    parking_price = calculate_price(
        total_slots,
        occupied_slots
    )

    return render_template(
        'dashboard.html',
        all_slots=all_slots,
        available_slots=available_slots,
        parked_vehicles=parked_vehicles,
        waiting_queue=waiting_queue,
        parking_price=parking_price,
        message=message,
        alert_type=alert_type
    )


# =====================================================
# SEARCH VEHICLE
# =====================================================

@app.route('/search', methods=['POST'])
def search():

    vehicle_number = request.form['vehicle_number'].upper()

    result = search_vehicle(vehicle_number)

    if result:

        message = f"Vehicle {vehicle_number} is parked at Slot {result}"
        alert_type = "success"

    elif vehicle_number in waiting_queue:

        position = waiting_queue.index(vehicle_number) + 1

        message = f"{vehicle_number} is in Waiting Queue (Position {position})"
        alert_type = "warning"

    else:

        message = f"{vehicle_number} not found!"
        alert_type = "danger"

    occupied_slots = len(parked_vehicles)

    total_slots = occupied_slots + len(available_slots)

    parking_price = calculate_price(
        total_slots,
        occupied_slots
    )

    return render_template(
        'dashboard.html',
        all_slots=all_slots,
        available_slots=available_slots,
        parked_vehicles=parked_vehicles,
        waiting_queue=waiting_queue,
        parking_price=parking_price,
        message=message,
        alert_type=alert_type
    )


# =====================================================
# RUN APP
# =====================================================

if __name__ == '__main__':
    app.run(debug=True)