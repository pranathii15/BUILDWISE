import matplotlib
matplotlib.use('Agg')   # prevents GUI/thread errors

import matplotlib.pyplot as plt
import os

def generate_floorplan(total_area):
    """
    Creates a box-style floor plan with room names and dimensions.
    """

    # Assume rectangular house
    side = total_area ** 0.5

    # Room layout grid (2 rows)
    layout = [
        [("Living Room", 0.30), ("Bedroom", 0.25)],
        [("Kitchen", 0.20), ("Bathroom", 0.10), ("Corridor", 0.15)]
    ]

    fig, ax = plt.subplots(figsize=(5, 5))

    y_offset = side

    for row in layout:
        row_height = side / len(layout)
        y_offset -= row_height

        x_offset = 0
        total_ratio = sum(r[1] for r in row)

        for room, ratio in row:
            width = side * (ratio / total_ratio)

            # Draw room box
            rect = plt.Rectangle(
                (x_offset, y_offset),
                width,
                row_height,
                fill=False,
                edgecolor="black",
                linewidth=2
            )
            ax.add_patch(rect)

            # Calculate dimensions
            room_area = total_area * ratio
            room_width = int(width)
            room_height = int(row_height)

            # Add label + dimensions
            ax.text(
                x_offset + width / 2,
                y_offset + row_height / 2,
                f"{room}\n{room_width} x {room_height}",
                ha="center",
                va="center",
                fontsize=8
            )

            x_offset += width

    ax.set_xlim(0, side)
    ax.set_ylim(0, side)
    ax.axis("off")

    os.makedirs("static", exist_ok=True)
    path = "static/floorplan.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()

    return path


def calculate_construction(area, floors, wage, cost):
    # Convert floors like G+2 → 3 floors
    if "+" in floors:
        total_floors = int(floors.split("+")[1]) + 1
    else:
        total_floors = int(floors)

    total_area = area * total_floors

    # Base worker estimation
    workers = max(6, int(total_area / 180))

    # Role-based allocation
    masons = max(1, int(workers * 0.25))
    helpers = max(2, int(workers * 0.30))
    steel_workers = max(1, int(workers * 0.15))
    carpenters = max(1, int(workers * 0.10))
    electricians = max(1, int(workers * 0.05))
    plumbers = max(1, int(workers * 0.05))

    assigned = (
        masons
        + helpers
        + steel_workers
        + carpenters
        + electricians
        + plumbers
    )

    supervisors = max(1, workers - assigned)

    # Duration estimation
    duration_days = int(total_area / workers)

    # Cost estimation
    labor_cost = workers * wage * duration_days
    material_cost = total_area * cost
    total_cost = labor_cost + material_cost

    # Material breakdown
    cement = int(total_area * 0.4)
    steel = int(total_area * 4)
    sand = int(total_area * 0.5)
    bricks = int(total_area * 8)

    # ---------------- WEEKLY SCHEDULE ----------------
    weekly_schedule = [
        {
            "week": 1,
            "task": "Site clearing and excavation",
            "materials": "Sand, water",
            "workers": helpers + supervisors
        },
        {
            "week": 2,
            "task": "Foundation work",
            "materials": "Cement, sand, steel",
            "workers": masons + steel_workers + helpers
        },
        {
            "week": 3,
            "task": "Column and beam casting",
            "materials": "Cement, steel, concrete",
            "workers": masons + steel_workers + carpenters
        },
        {
            "week": 4,
            "task": "Slab casting",
            "materials": "Concrete, steel",
            "workers": masons + carpenters + helpers
        },
        {
            "week": 5,
            "task": "Brickwork for walls",
            "materials": "Bricks, cement, sand",
            "workers": masons + helpers
        },
        {
            "week": 6,
            "task": "Electrical and plumbing rough-ins",
            "materials": "Pipes, wires",
            "workers": electricians + plumbers + helpers
        },
        {
            "week": 7,
            "task": "Plastering and finishing",
            "materials": "Cement, sand",
            "workers": masons + helpers
        },
        {
            "week": 8,
            "task": "Final fixtures and inspection",
            "materials": "Fixtures, paint",
            "workers": electricians + plumbers + supervisors
        }
    ]
    # -------------------------------------------------

    # Generate floorplan
    floorplan_path = generate_floorplan(total_area)

    # ---------------- ALTERNATIVE PLANS ----------------
    plan_variants = [
        {
            "name": "Fast Track Plan",
            "worker_factor": 1.3,
            "cost_factor": 1.15
        },
        {
            "name": "Balanced Plan",
            "worker_factor": 1.0,
            "cost_factor": 1.0
        },
        {
            "name": "Budget Saver Plan",
            "worker_factor": 0.8,
            "cost_factor": 0.9
        },
        {
            "name": "High Quality Plan",
            "worker_factor": 1.1,
            "cost_factor": 1.2
        }
    ]

    alternative_plans = []

    for plan in plan_variants:
        p_workers = max(4, int(workers * plan["worker_factor"]))
        p_duration = int(total_area / p_workers)

        p_labor_cost = p_workers * wage * p_duration
        p_material_cost = int(material_cost * plan["cost_factor"])
        p_total = p_labor_cost + p_material_cost

        alternative_plans.append({
            "name": plan["name"],
            "workers": p_workers,
            "duration": p_duration,
            "total_cost": p_total
        })
    # ---------------- SUSTAINABILITY OPTIONS ----------------
    sustainability_options = [
        {
            "material": "Fly Ash Bricks",
            "impact": "Reduces CO₂ emissions by 25%",
            "cost_change": "-5% material cost"
        },
        {
            "material": "Recycled Steel",
            "impact": "Reduces CO₂ emissions by 30%",
            "cost_change": "+3% material cost"
        },
        {
            "material": "Low-carbon Cement",
            "impact": "Reduces CO₂ emissions by 40%",
            "cost_change": "+8% material cost"
        }
    ]
    # ---------------- MATERIAL DELIVERY PLANNER ----------------
    material_delivery = [
        {
            "week": 1,
            "materials": f"Sand: {int(sand * 0.25)} tons, Water: Initial supply",
            "note": "For site clearing and excavation"
        },
        {
            "week": 2,
            "materials": f"Cement: {int(cement * 0.30)} bags, Steel: {int(steel * 0.40)} kg",
            "note": "Foundation and structural base"
        },
        {
            "week": 3,
            "materials": f"Steel: {int(steel * 0.30)} kg, Cement: {int(cement * 0.20)} bags",
            "note": "Columns and beams"
        },
        {
            "week": 4,
            "materials": f"Cement: {int(cement * 0.25)} bags, Steel: {int(steel * 0.20)} kg",
            "note": "Slab casting"
        },
        {
            "week": 5,
            "materials": f"Bricks: {int(bricks * 0.80)}, Cement: {int(cement * 0.15)} bags",
            "note": "Wall construction"
        },
        {
            "week": 6,
            "materials": "Pipes, wires, electrical fittings",
            "note": "Plumbing and electrical setup"
        },
        {
            "week": 7,
            "materials": f"Cement: {int(cement * 0.10)} bags, Sand: {int(sand * 0.30)} tons",
            "note": "Plastering and finishing"
        },
        {
            "week": 8,
            "materials": "Paint, fixtures, final fittings",
            "note": "Final finishing and inspection"
        }
    ]

    # ---------------- PROJECT TIMELINE ----------------
    timeline = [
        {"phase": "Planning", "duration": 7, "color": "#6a6fd1"},
        {"phase": "Foundation", "duration": 14, "color": "#7b4fb5"},
        {"phase": "Structure", "duration": 45, "color": "#5a8dee"},
        {"phase": "Brickwork", "duration": 30, "color": "#39b54a"},
        {"phase": "Electrical & Plumbing", "duration": 20, "color": "#ff9f43"},
        {"phase": "Finishing", "duration": 25, "color": "#e74c3c"},
        {"phase": "Final Inspection", "duration": 7, "color": "#2c3e50"}
    ]

    return {
        "workers": workers,
        "worker_breakdown": {
            "masons": {
                "count": masons,
                "duty": "Brickwork, plastering, structural masonry."
            },
            "helpers": {
                "count": helpers,
                "duty": "Material handling, mixing, and general support."
            },
            "steel_workers": {
                "count": steel_workers,
                "duty": "Rebar cutting, bending, and structural reinforcement."
            },
            "carpenters": {
                "count": carpenters,
                "duty": "Formwork, shuttering, and wooden fittings."
            },
            "electricians": {
                "count": electricians,
                "duty": "Wiring, switches, lighting, and electrical setup."
            },
            "plumbers": {
                "count": plumbers,
                "duty": "Water pipelines, drainage, and fixtures."
            },
            "supervisors": {
                "count": supervisors,
                "duty": "Site coordination, quality checks, and scheduling."
            }
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
        "weekly_schedule": weekly_schedule,
        "floorplan": floorplan_path,
	"alternative_plans": alternative_plans,
"sustainability_options": sustainability_options,
"material_delivery": material_delivery,
"timeline": timeline,


        "explanations": {
            "workers": f"{workers} workers estimated for {total_area} sq yards considering standard productivity.",
            "duration": f"{duration_days} days estimated based on workforce and area.",
            "labor_cost": f"Labor cost = {workers} workers × ₹{wage} × {duration_days} days.",
            "material_cost": f"Material cost = {total_area} sq yards × ₹{cost}.",
            "total_cost": "Total = Labor + Material."
        }
    }
