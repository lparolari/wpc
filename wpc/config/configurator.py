from configparser import ConfigParser


class Configurator(object):

    _cfg = None

    SEC_SESSION = 'session'
    OPT_CUSTOMER_ID = 'customer.id'

    SEC_COMMON = 'common'
    OPT_DATEFORMAT = 'dateformat'
    OPT_DEBUG = 'debug'

    def __init__(self) -> None:
        super().__init__()
        self._cfg = ConfigParser()
        self._cfg.read('config.ini')

        self._make_defaults()

    @property
    def customer(self):
        self._read()
        return self._cfg.get(self.SEC_SESSION, self.OPT_CUSTOMER_ID)

    @customer.setter
    def customer(self, value):
        self._read()
        self._do_section(self.SEC_SESSION)
        self._cfg.set(self.SEC_SESSION, self.OPT_CUSTOMER_ID, value)
        self._save()

    @property
    def dateformat(self):
        self._read()
        return self._cfg.get(self.SEC_COMMON, self.OPT_DATEFORMAT)

    @dateformat.setter
    def dateformat(self, value):
        self._read()
        self._do_section(self.SEC_COMMON)
        self._cfg.set(self.SEC_COMMON, self.OPT_DATEFORMAT, value)
        self._save()

    @property
    def debug(self):
        self._read()
        return self._cfg.getboolean(self.SEC_COMMON, self.OPT_DEBUG)

    @debug.setter
    def debug(self, value):
        self._read()
        self._do_section(self.SEC_COMMON)
        self._cfg.set(self.SEC_COMMON, self.OPT_DEBUG, str(value))
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
        if force or not self._cfg.has_option(self.SEC_COMMON, self.OPT_DATEFORMAT):
            self.dateformat = str("%%d/%%m/%%Y")
        if force or not self._cfg.has_option(self.SEC_COMMON, self.OPT_DEBUG):
            self.debug = str(False)

    def _do_section(self, value):
        """
        Creates a section if it does not exist.
        :param value: The section to create.
        """
        if not self._cfg.has_section(value):
            self._cfg.add_section(value)


configurator = Configurator()
