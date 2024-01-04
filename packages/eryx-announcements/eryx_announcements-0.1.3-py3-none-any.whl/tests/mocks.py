from src.announcements import Announcement


class Announced:
    def __init__(self):
        super().__init__()
        self._announcements = []

    def do_something(self, an_announcement):
        self._announcements.append(an_announcement)

    def announcements(self):
        return self._announcements


class AnnouncementMockA(Announcement):
    pass


class AnnouncementMockB(Announcement):
    pass
