import json

class Sammlung:
    def __init__(self, alben=None):
        self.alben = alben if alben is not None else []

    def add_album(self, album):
        if not isinstance(self.alben, list):
            self.alben = []
        self.alben.append(album)

    def remove_album(self, album):
        self.alben.remove(album)

    def total_time_to_play(self):
        total = sum(album.get_total_play_time_in_seconds() for album in self.alben)
        return self.seconds_to_time(total)

    def printInformation(self):
        info = []
        for album in self.alben:
            info.append(f"Album: {album.title} \nVon: {album.interpret} \nLänge: {album.get_total_time_to_play()}")
        return "\n\n".join(info)

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump([album.to_dict() for album in self.alben], file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    self.alben = [Album.from_dict(album_data) for album_data in data]
                else:
                    self.alben = []
        except (FileNotFoundError, json.JSONDecodeError):
            self.alben = []

    @staticmethod
    def seconds_to_time(seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f'{h:02}:{m:02}:{s:02}'

class Album:
    def __init__(self, title, interpret, tracks=None):
        self.title = title
        self.interpret = interpret
        self.tracks = tracks if tracks is not None else []

    def add_track(self, track):
        self.tracks.append(track)

    def remove_track(self, track):
        self.tracks.remove(track)

    def get_total_play_time_in_seconds(self):
        return sum(track.get_duration_in_seconds() for track in self.tracks)

    def get_total_time_to_play(self):
        total_seconds = self.get_total_play_time_in_seconds()
        return Sammlung.seconds_to_time(total_seconds)

    def printInformation(self):
        track_list = "\n".join(f"Track: {track.title}, MP3: {track.MP3}, Duration: {track.duration}" for track in self.tracks)
        return f"Album: {self.title}\nVon: {self.interpret}\nLänge: {self.get_total_time_to_play()}\n{track_list}"

    def to_dict(self):
        return {
            'title': self.title,
            'interpret': self.interpret,
            'tracks': [track.to_dict() for track in self.tracks]
        }

    @classmethod
    def from_dict(cls, data):
        tracks = [Track(track_data['title'], track_data['mp3'], track_data['duration']) for track_data in data['tracks']]
        return cls(data['title'], data['interpret'], tracks)

class Track:
    def __init__(self, title, MP3, duration):
        self.title = title
        self.MP3 = MP3
        self.duration = duration

    def __str__(self):
        return f"{self.title} ({self.duration})"

    def get_duration_in_seconds(self):
        h, m, s = map(int, self.duration.split(':'))
        return h * 3600 + m * 60 + s

    def to_dict(self):
        return {
            'title': self.title,
            'mp3': self.MP3,
            'duration': self.duration
        }
