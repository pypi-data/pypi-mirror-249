import sys
from imppkg.harmonic_mean import harmonic_mean
import termcolor


def _get_measurements(args: list[str]) -> list[float]:
    try:
        return [float(v) for v in args]
    except ValueError:
        pass
    return []


def _get_mean_unsafe(measurements: list[float]) -> float:
    try:
        return harmonic_mean(measurements)
    except ZeroDivisionError:
        pass
    return 0.0


def main() -> None:
    measurements = _get_measurements(sys.argv[1:])
    result = _get_mean_unsafe(measurements)
    tc_result = termcolor.colored(
        str(result), "red", "on_cyan", attrs=["bold"]
    )
    print(tc_result)
