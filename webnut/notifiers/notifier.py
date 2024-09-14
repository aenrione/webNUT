from abc import ABC, abstractmethod

# Abstract Builder class
class NotificationBuilder(ABC):
    @abstractmethod
    def set_message(self, message):
        pass

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def is_valid(self):
        pass


# Abstract Director class for managing the notification
class NotificationDirector:
    def __init__(self, builder: NotificationBuilder):
        self._builder = builder

    def construct_notification(self, message):
        if self._builder.is_valid():
            self._builder.set_message(message)
            self._builder.send()

