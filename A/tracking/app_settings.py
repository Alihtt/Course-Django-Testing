class AppSetting:
    def __init__(self, prefix) -> None:
        self.prefix = prefix

    def _setting(self, name, default):
        from django.conf import settings

        return getattr(settings, self.prefix + name, default)

    @property
    def PATH_LENGTH(self):
        return self._setting("PATH_LENGTH", 200)

    @property
    def DECODE_REQUEST_BODY(self):
        return self._setting("DECODE_REQUEST_BODY", True)


app_settings = AppSetting("DRF_TRACKING_")
