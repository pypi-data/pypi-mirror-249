def harmonic_mean(measurements: list[float]) -> float:
    # Executive decision: discard zero values to avoid
    # DivideByZero
    non_zeros = [m for m in measurements if m != 0.0]
    num_measurements = len(non_zeros)

    denom = sum(1.0 / m for m in non_zeros)
    return num_measurements / denom
