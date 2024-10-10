import threading
import time
import logging
from nut2 import PyNUTClient
from webnut.notifiers.notifier import NotificationDirector
from webnut.notifiers.telegram import TelegramBuilder
from webnut.notifiers.email import EmailBuilder
from . import config

class WebNUTClient(PyNUTClient):
    def __init__(self, *args, **kwargs):
        """
         Initializes the WebNUTClient class.
        :param event_check_interval: Time interval (in seconds) between each UPS event check.
        """
        super(WebNUTClient, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self._notification_thread = None
        self._last_status = None
        self._last_battery_charge = None
        self._battery_difference = int(config.battery_difference)
        self.notifiers = []
        self.ups_dict = self.list_ups()
        self._event_check_interval = int(config.polling_interval)
        self._set_notifiers()
        self._connect()

    def start_event_listener(self):
        """
        Starts the event listener in a separate thread.
        """
        logging.info("Starting event listener thread...")
        self._notification_thread = threading.Thread(target=self._listen_for_events)
        self._notification_thread.start()

    def stop_event_listener(self):
        """
        Stops the event listener thread gracefully.
        """
        logging.info("Stopping event listener thread...")
        self._stop_event.set()
        if self._notification_thread:
            self._notification_thread.join()

    def _listen_for_events(self):
        """
        Thread method that continuously polls UPS variables for changes (events).
        """
        logging.info("Listening for UPS events...")
        while not self._stop_event.is_set():
            try:
                # Poll UPS variables periodically
                while not self._stop_event.is_set():
                    if self._srv_handler is not None:
                        for ups in self.ups_dict:
                            ups_status = self._get_variable(ups, "ups.status")
                            battery_charge = self._get_variable(ups, "battery.charge")

                            self._handle_ups_status(ups, ups_status)

                            self._handle_battery_charge(ups, battery_charge)
                    
                    time.sleep(self._event_check_interval)
            except Exception as e:
                logging.error(f"Error while listening for UPS events: {e}")
                time.sleep(5)
                logging.info("Reconnecting to NUT server...")
                self._connect()
                continue

    def _handle_ups_status(self, ups, ups_status):
         """
         Handles UPS status changes.
         Handles UPS status changes and avoids redundant messages when the UPS is still online (status includes "OL").
         """
         is_current_online = "OL" in ups_status
         was_last_online = "OL" in self._last_status if self._last_status else False
 
         if is_current_online and was_last_online:
             return
 
         if ups_status != self._last_status:
             if "OL" in ups_status:
                 event_message = "UPS is online"
             elif "OB" in ups_status:
                 event_message = "UPS is on battery"
             else:
                 event_message = f"UPS status changed from {self._last_status} to {ups_status}"
             
             logging.info(f"{ups}: {event_message}")
             self._forward_event(f"{ups}: {event_message}")
 
             self._last_status = ups_status

    def _handle_battery_charge(self, ups, battery_charge):
        """
        Handles battery charge changes.
        """
        battery_charge = int(battery_charge)
        self._last_battery_charge = self._last_battery_charge or battery_charge
        if battery_charge and self._last_battery_charge and abs(battery_charge - self._last_battery_charge) >= self._battery_difference:
            event_message = f"Battery charge dropped to {battery_charge}%"
            logging.info(f"{ups}: {event_message}")
            self._forward_event(f"{ups}: {event_message}")
            self._last_battery_charge = battery_charge

    def _get_variable(self, ups, varname):
        """Fetch a specific UPS variable from the NUT server."""
        try:
            ups_vars = self.list_vars(ups)
            return ups_vars.get(varname, None)
        except Exception as e:
            logging.error(f"Failed to get UPS variable {varname}: {e}")
            return None

    def _set_notifiers(self):
        """
        Sets up the notifiers for sending notifications.
        """
        telegram_bot_token = config.telegram_bot_token
        telegram_chat_id = config.telegram_chat_id

        # Use the Telegram notification builder
        telegram_builder = TelegramBuilder(telegram_bot_token, telegram_chat_id)
        if telegram_builder.is_valid():
            self.notifiers.append(telegram_builder)
            logging.info("Telegram notifier is set up.")

        # Use the Email notification builder
        email_builder = EmailBuilder(config.smtp_server, config.smtp_port, config.smtp_email, config.smtp_receiver, config.smtp_password, config.smtp_protocol)
        if email_builder.is_valid():
            self.notifiers.append(email_builder)
            logging.info("Email notifier is set up.")

    def _forward_event(self, message):
        """
        Sends a notification using the Notification system.
        You can use the previously implemented NotificationDirector and builders here.
        """
        for notifier in self.notifiers:
            director = NotificationDirector(notifier)
            director.construct_notification(message)
