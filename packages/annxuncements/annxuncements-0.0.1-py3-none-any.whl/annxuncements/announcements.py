import inspect


class Announcement:
    """This class is the superclass for events that someone might want to
    announce, such as a button click or an attribute change. Typically you
    create subclasses for your own events you want to announce.
    """

    @classmethod
    def handles(cls, an_announcement_class):
        return an_announcement_class is cls or issubclass(an_announcement_class, cls)

    @staticmethod
    def as_announcement(an_announcement_or_class):
        """
        We can't make a class and an instance method with the same name.
        """
        if inspect.isclass(an_announcement_or_class):
            return an_announcement_or_class()
        else:
            return an_announcement_or_class
