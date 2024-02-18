from .base_mixins import BaseLoggingMixin


class LoggingMixin(BaseLoggingMixin):

    def handle_log(self):
        print(self.log)
