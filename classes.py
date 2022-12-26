import inflect
p = inflect.engine()
from datetime import datetime, timezone


class BaseActivity():
    def __init__(self, activity):
        self.users = [] 
        self.activity = activity
    
    def add_user(self, user):
        self.users.append(user)

    def get_field(self, verb, emoji):
        count = len(self.users)
        users_str = ""
        for user in self.users:
            users_str += user.get_summary_str()

        return {
            "name": f"{emoji} {count} {p.plural('person', count)} {p.plural_verb('is', count)} {verb} {self.activity}",
            "value": users_str
        }
    
    def __repr__(self):
        return f"Activity({self.users}, {self.activity})"


class BaseUser():
    def __init__(self, name):
        self.name = name
    
    def get_summary_str(self):
        return f"**{self.name}**\n"

    def __repr__(self):
        return f"User({self.name})"
    

class ArtistActivity(BaseActivity):
    def get_field(self):
        return super().get_field("listening to", ":headphones:")
    
    def add_user(self, user, song):
        super().add_user(Listener(user, song))

    def __repr__(self):
        return "Artist" + super().__repr__()


class Listener(BaseUser):
    def __init__(self, name, song):
        super().__init__(name)
        self.song = song
    
    def get_summary_str(self):
        return f"**{self.name}:** {self.song}\n"

    @staticmethod
    def format_user_str(song, artist):
        return f":headphones: {song} by {artist}\n"

    @staticmethod
    def format_user_details(duration, start, url):
        progress_str = ""
        if start is not None:
            elapsed_total = (datetime.now(timezone.utc) - start).total_seconds()
            song_total = duration.total_seconds()

            elapsed_min, elapsed_sec = divmod(elapsed_total, 60)
            song_min, song_sec = divmod(song_total, 60)

            passed = min(int((elapsed_total / song_total) * 10), 10)
            progress_str = f"{int(elapsed_min)}:{int(elapsed_sec):02} {'─' * passed}●{'─' * (10 - passed)} {int(song_min)}:{int(song_sec):02}"
        return f"{progress_str} [▶ Spotify]({url})"

    def __repr__(self):
        return f"Listener({self.name}, {self.song})"


class GameActivity(BaseActivity):
    def get_field(self):
        return super().get_field("playing", ":video_game:")

    def add_user(self, user, time=None, details=None):
        super().add_user(Gamer(user, time, details))

    def __repr__(self):
        return "Game" + super().__repr__()
    

class Gamer(BaseUser):
    def __init__(self, name, time=None, details=None):
        super().__init__(name)
        self.time = time
        self.details = details

    def get_summary_str(self):
        summary_str = f"**{self.name}:**"
        if self.details:
            summary_str += f" *{self.details}*"
        if self.time:
            summary_str += f" {self.time}"
        return f"{summary_str}\n"

    @staticmethod
    def format_user_str(game):
        return f":video_game: {game}\n"

    @staticmethod
    def format_user_details(time, details):
        user_details = ""
        if details is not None:
            user_details += f"*{details}*"
        if time is not None:
            user_details += f" {time}"
        return user_details

    def __repr__(self):
        return f"Gamer({self.name}, {self.time}, {self.details})"


class StreamActivity(BaseActivity):
    def get_field(self):
        return super().get_field("streaming", ":red_circle:")

    def add_user(self, user, url, platform=None, title=None):
        super().add_user(Streamer(user, url, platform, title))

    def __repr__(self):
        return "Stream" + super().__repr__()


class Streamer(BaseUser):
    def __init__(self, name, url, platform=None, title=None):
        super().__init__(name)
        self.url = url
        self.platform = platform
        self.title = title
    
    def get_summary_str(self):
        summary_str = f"**{self.name}**"
        if self.title:
            summary_str += f": {self.title}"
        if self.url:
            summary_str += f" {self.url}"
        return f"{summary_str}\n"

    @staticmethod
    def format_user_str(game, platform=None):
        return f":red_circle: streaming {game} on {platform}\n"

    @staticmethod
    def format_stream_details(url, title=None):
        return f"{title} {url}"

    def __str__(self):
        return f"Streamer({self.name}, {self.url}, {self.platform}, {self.title})"
