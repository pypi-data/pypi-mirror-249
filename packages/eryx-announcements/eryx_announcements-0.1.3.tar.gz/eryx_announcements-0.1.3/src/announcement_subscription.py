class AnnouncementSubscription:
    """
    The subscription is a single entry in a SubscriptionRegistry.
    """

    def __init__(self, announcer, announcement_class, action, subscriber=None):
        self._announcer = announcer
        self._announcement_class = announcement_class
        self._action = action
        self._subscriber = subscriber

    @classmethod
    def new_with(cls, announcer, announcement_class, action, subscriber=None):
        return cls(announcer, announcement_class, action, subscriber)

    def deliver(self, announcement):
        """
        Deliver an announcement to receiver.
        """
        if self.handles(announcement):
            self._execute_action(announcement)

    def _execute_action(self, announcement):
        self._action(announcement)

    def handles(self, an_announcement):
        """
        Return true if self.announcementClass can handle it
        """
        return self._announcement_class.handles(an_announcement.__class__)

    def action(self):
        return self._action
