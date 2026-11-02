
import math


def distance(p1, p2):
    """Tinh khoang cach giua hai diem."""
    return math.hypot(
        p1[0] - p2[0],
        p1[1] - p2[1]
    )


def cluster_points(points, threshold=0.15, min_points=3):
    """Gom cac diem LiDAR lien tiep thanh cum."""

    if not points:
        return []

    clusters = []
    current_cluster = [points[0]]

    for point in points[1:]:

        previous = current_cluster[-1]

        if distance(previous, point) <= threshold:
            current_cluster.append(point)

        else:
            if len(current_cluster) >= min_points:
                clusters.append(current_cluster)

            current_cluster = [point]

    if len(current_cluster) >= min_points:
        clusters.append(current_cluster)

    return clusters


def calculate_centroid(cluster):
    """Tinh toa do trung binh cua cum."""

    x = sum(p[0] for p in cluster) / len(cluster)
    y = sum(p[1] for p in cluster) / len(cluster)

    return (x, y)
