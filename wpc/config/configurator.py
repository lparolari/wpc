from configparser import ConfigParser


class Configurator(object):

    _cfg = None

    def __init__(self) -> None:
        super().__init__()
        self._cfg = ConfigParser()
        self._cfg.read('config.ini')

        self._make_defaults()

    @property
    def customer(self):
        self._read()
        return self._cfg.get("session", "customer.id")

    @customer.setter
    def customer(self, value):
        self._read()
        self._do_section("session")
        self._cfg.set("session", "customer.id", value)
        self._save()

    @property
    def dateformat(self):
        self._read()
        return self._cfg.get("common", "dateformat")

    @dateformat.setter
    def dateformat(self, value):
        self._read()
        self._do_section("common")
        self._cfg.set("common", "dateformat", value)
        self._save()

    def _save(self):
        with open('config.ini', 'w') as configfile:
            self._cfg.write(configfile)

    def _read(self):
        self._cfg.read('config.ini')

    def _make_defaults(self, force=False):
        """
        Creates default values if does not exist or if ``force`` is true.
        :param force: If true, restores the default values.
        """
        if force or not self._cfg.has_option("common", "dateformat"):
            self.dateformat = str("%%d/%%m/%%Y")

    def _do_section(self, value):
        """
        Creates a section if it does not exist.
        :param value: The section to create.
        """
        if not self._cfg.has_section(value):
            self._cfg.add_section(value)


configurator = Configurator()
