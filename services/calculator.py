def calculate_construction(area, floors, wage, cost):
    # Convert floors like G+2 → 3 floors
    if "+" in floors:
        total_floors = int(floors.split("+")[1]) + 1
    else:
        total_floors = int(floors)

    total_area = area * total_floors

    # Worker estimation
    workers = max(5, int(total_area / 200))

    # Worker breakdown
    masons = int(workers * 0.3)
    helpers = int(workers * 0.4)
    steel_workers = int(workers * 0.1)
    carpenters = int(workers * 0.1)
    supervisors = workers - (masons + helpers + steel_workers + carpenters)

    # Duration estimation
    duration_days = int(total_area / workers)

    # Cost estimation
    labor_cost = workers * wage * duration_days
    material_cost = total_area * cost
    total_cost = labor_cost + material_cost

    # Material breakdown
    cement = int(total_area * 0.4)   # bags
    steel = int(total_area * 4)      # kg
    sand = int(total_area * 0.5)     # tons
    bricks = int(total_area * 8)     # pieces

    return {
        "workers": workers,
        "worker_breakdown": {
            "masons": masons,
            "helpers": helpers,
            "steel_workers": steel_workers,
            "carpenters": carpenters,
            "supervisors": supervisors
        },
        "duration_days": duration_days,
        "labor_cost": labor_cost,
        "material_cost": material_cost,
        "total_cost": total_cost,
        "materials": {
            "cement_bags": cement,
            "steel_kg": steel,
            "sand_tons": sand,
            "bricks": bricks
        },
        "explanations": {
            "workers": f"{workers} workers are estimated based on total built-up area of {total_area} sq yards, assuming 1 worker per 200 sq yards.",
            "duration": f"Project duration is estimated as {duration_days} days based on worker productivity and total area.",
            "labor_cost": f"Labor cost is calculated using {workers} workers × ₹{wage} per day × {duration_days} days.",
            "material_cost": f"Material cost is based on total area ({total_area} sq yards) × ₹{cost} per sq yard.",
            "total_cost": "Total cost is the sum of material and labor costs."
        }
    }
