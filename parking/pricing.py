# =====================================================
# DYNAMIC PRICING
# =====================================================

def calculate_price(total_slots, occupied_slots):

    occupancy = (occupied_slots / total_slots) * 100

    # High congestion
    if occupancy >= 80:
        return 150

    # Medium congestion
    elif occupancy >= 50:
        return 100

    # Low congestion
    return 50