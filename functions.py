def validate_inputs(pwm_entry, time_entry, volume_entry, cycle_entry, cycle_time_value):

    pwm_value = pwm_entry.get().strip()
    time_value = time_entry.get().strip()
    volume_value = volume_entry.get().strip()
    cycle_value = cycle_entry.get()

    missing_inputs = []
    bad_inputs = []

    if not pwm_value:
        missing_inputs.append("PWM Value")
    if not time_value:
        missing_inputs.append("Reaction Time")
    if not volume_value:
        missing_inputs.append("Solid Volume")
    if missing_inputs:
        raise ValueError(f"Missing required inputs: {', '.join(missing_inputs)}")

    # Validate PWM
    try:
        pwm_value = int(pwm_value)
        if pwm_value <= 0 or pwm_value > 255:
            bad_inputs.append("PWM Value")
    except ValueError:
        bad_inputs.append("PWM Value")

    # Validate Reaction Time
    try:
        time_value = int(time_value)
        if time_value <= 0:
            bad_inputs.append("Reaction Time")
    except ValueError:
        bad_inputs.append("Reaction Time")

    # Validate Solid Volume
    try:
        volume_value = int(volume_value)
        if volume_value <= 0:
            bad_inputs.append("Solid Volume")
    except ValueError:
        bad_inputs.append("Solid Volume")

    try:
        if cycle_time_value <= 0:  # Default to 30 if value is invalid
            raise ValueError
    except ValueError:
        cycle_time_value = 30

    # Validate Cleaning Cycles
    try:
        cycle_value = int(cycle_value)
        if cycle_value <= 0:
            bad_inputs.append("Cleaning Cycles")
    except ValueError:
        bad_inputs.append("Cleaning Cycles")

    if bad_inputs:
        raise ValueError(f"Invalid inputs: {', '.join(bad_inputs)}")

    # Return validated values
    return pwm_value, time_value, volume_value, cycle_value, cycle_time_value
