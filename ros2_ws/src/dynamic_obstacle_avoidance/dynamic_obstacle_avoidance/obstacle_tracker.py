
import math


class ObstacleTracker:
    """
    Theo doi vat can qua nhieu lan quet LiDAR.
    Dau vao phai la toa do trong cung mot he quy chieu,
    du kien la odom.
    """

    def __init__(
        self,
        max_match_distance=0.5,
        max_missed_frames=3
    ):
        self.tracks = {}
        self.next_id = 1

        self.max_match_distance = max_match_distance
        self.max_missed_frames = max_missed_frames

    def calculate_distance(self, p1, p2):
        """Tinh khoang cach giua hai vi tri."""
        return math.hypot(
            p1[0] - p2[0],
            p1[1] - p2[1]
        )

    def update(self, detections, timestamp):
        """
        Cap nhat danh sach vat can.

        detections: [(x, y), (x, y), ...]
        timestamp: thoi gian tinh bang giay
        """

        matched_ids = set()
        matched_detections = set()

        # Buoc 1: Tim cap vat can gan nhau nhat
        candidates = []

        for track_id, track in self.tracks.items():

            for index, detection in enumerate(detections):

                distance = self.calculate_distance(
                    track["position"],
                    detection
                )

                if distance <= self.max_match_distance:
                    candidates.append(
                        (distance, track_id, index)
                    )

        # Uu tien cac cap co khoang cach nho nhat
        candidates.sort(key=lambda item: item[0])

        # Buoc 2: Gan ID cho cac vat can da tim thay
        for distance, track_id, index in candidates:

            if track_id in matched_ids:
                continue

            if index in matched_detections:
                continue

            track = self.tracks[track_id]

            old_x, old_y = track["position"]
            new_x, new_y = detections[index]

            dt = timestamp - track["timestamp"]

            if dt > 0:
                vx = (new_x - old_x) / dt
                vy = (new_y - old_y) / dt
            else:
                vx = 0.0
                vy = 0.0

            track["position"] = (new_x, new_y)
            track["velocity"] = (vx, vy)
            track["timestamp"] = timestamp
            track["missed"] = 0

            matched_ids.add(track_id)
            matched_detections.add(index)

        # Buoc 3: Tao ID moi cho vat can chua duoc gan
        for index, detection in enumerate(detections):

            if index in matched_detections:
                continue

            track_id = self.next_id
            self.next_id += 1

            self.tracks[track_id] = {
                "position": detection,
                "velocity": (0.0, 0.0),
                "timestamp": timestamp,
                "missed": 0
            }

            matched_ids.add(track_id)

        # Buoc 4: Danh dau vat can khong con duoc nhin thay
        for track_id in list(self.tracks.keys()):

            if track_id not in matched_ids:
                self.tracks[track_id]["missed"] += 1

                if (
                    self.tracks[track_id]["missed"]
                    > self.max_missed_frames
                ):
                    del self.tracks[track_id]

        # Chi tra ve cac vat can duoc nhan dien trong lan quet nay
        results = []

        for track_id in matched_ids:
            track = self.tracks[track_id]

            results.append({
                "id": track_id,
                "position": track["position"],
                "velocity": track["velocity"],
                "speed": math.hypot(
                    track["velocity"][0],
                    track["velocity"][1]
                )
            })

        return sorted(results, key=lambda item: item["id"])
