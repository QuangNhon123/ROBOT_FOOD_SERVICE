
import math


def scan_to_points(scan):
    """Chuyen du lieu LaserScan thanh cac diem (x, y)."""

    points = []

    for i, distance in enumerate(scan.ranges):

        # Bo cac khoang cach khong hop le
        if not math.isfinite(distance):
            continue

        if distance < scan.range_min or distance > scan.range_max:
            continue

        # Tinh goc cua tia laser thu i
        angle = scan.angle_min + i * scan.angle_increment

        # Chuyen tu khoang cach + goc sang X, Y
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)

        points.append((x, y))

    return points
