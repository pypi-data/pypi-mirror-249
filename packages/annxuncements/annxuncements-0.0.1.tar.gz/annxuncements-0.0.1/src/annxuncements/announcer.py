from .announcement_subscription import AnnouncementSubscription
from .subscription_registry import SubscriptionRegistry


class Announcer:
    """
    The code is based on the announcements as described by Vassili Bykov in
    http://www.cincomsmalltalk.com/userblogs/vbykov/.
    """

    def __init__(self):
        super().__init__()
        self.registry = SubscriptionRegistry.new()

    @classmethod
    def new(cls):
        return cls()

    def announce(self, announcement):
        announcement = announcement.as_announcement(announcement)
        self.registry.deliver(announcement)
        return announcement

    def subscribe(self, an_announcement_class, callable):
        """
        Declare that when announcement_class is raised, the callable method is called.
        """
        subscription = AnnouncementSubscription.new_with(
            announcer=self, announcement_class=an_announcement_class, action=callable
        )
        return self.add_subscription(subscription)

    def add_subscription(self, subscription):
        # This is public because a subscription may be created outside the announcer
        return self.registry.add(subscription)

    def unsubscribe(self, action):
        return self.registry.remove_action(action)
