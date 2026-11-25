def assess_item(assessment):

    item = assessment["Item"]
    working = assessment["Working condition"]
    damage = assessment["Visible damage"]
    battery = assessment["Battery condition"]

    # Battery safety
    if battery == "Yes":
        return {
            "status": "SAFETY WARNING",
            "recommendation": "Professional Battery Handling",
            "message": (
                "Do not charge, use, puncture or dismantle "
                "a swollen or leaking battery. Seek professional help."
            )
        }

    if battery == "Not sure":
        return {
            "status": "SAFETY CHECK REQUIRED",
            "recommendation": "Get Battery Inspected",
            "message": (
                "Battery condition is uncertain. Do not charge "
                "or use the device until it has been inspected."
            )
        }

    # Damaged charger
    if item == "Charger / Adapter" and damage != "No visible damage":
        return {
            "status": "SAFETY WARNING",
            "recommendation": "Stop Using the Charger",
            "message": (
                "Stop using the damaged charger. "
                "Get it checked by a qualified technician."
            )
        }

    # Other visible damage
    if damage != "No visible damage":
        return {
            "status": "ASSESSMENT NEEDED",
            "recommendation": "Professional Inspection",
            "message": (
                "Get the item inspected by a qualified technician "
                "before deciding whether it can be repaired or reused."
            )
        }

    # Working item
    if working == "Yes":
        return {
            "status": "POTENTIALLY REUSABLE",
            "recommendation": "Reuse the Electronic Item",
            "message": (
                "The item is reported to be working with no visible "
                "damage. Consider continued use or responsible reuse."
            )
        }

    # Non-working item
    if working == "No":
        return {
            "status": "REPAIR ASSESSMENT",
            "recommendation": "Consider Professional Repair",
            "message": (
                "Get a professional repair assessment. If repair is "
                "not practical, use an authorised e-waste collection channel."
            )
        }

    # Uncertain condition
    return {
        "status": "MORE INFORMATION NEEDED",
        "recommendation": "Confirm Item Condition",
        "message": (
            "The working condition is uncertain. Confirm the condition "
            "or seek professional assessment."
        )
    }