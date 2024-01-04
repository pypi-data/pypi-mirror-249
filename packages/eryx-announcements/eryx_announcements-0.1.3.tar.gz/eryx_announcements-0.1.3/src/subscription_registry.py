class SubscriptionRegistry:
    """
    The subscription registry is an storage for the subscriptions to an Announcer.
    """

    def __init__(self):
        super().__init__()
        self._subscriptions = set()

    @classmethod
    def new(cls):
        return cls()

    def __len__(self):
        return len(self._subscriptions)

    def reset(self):
        self._subscriptions = set()

    def add(self, subscription):
        # because self._subscriptions is a set, this automatically ignores duplicates
        self._subscriptions.add(subscription)
        return subscription

    def remove(self, subscription):
        if subscription in self._subscriptions:
            self._subscriptions.remove(subscription)

    def remove_action(self, action):
        subscriptions = list(self._subscriptions)
        for subscription in subscriptions:
            if subscription.action() == action:
                self._subscriptions.remove(subscription)

    def deliver(self, announcement):
        for each_subscription in self._subscriptions:
            each_subscription.deliver(announcement)
