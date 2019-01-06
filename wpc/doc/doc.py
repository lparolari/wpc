import os
import subprocess
from pathlib import Path

from config.configurator import Configurator

configurator = Configurator()


class Doc(object):

    GROSS = 'GROSS'
    TAX = 'TAX'
    NET = 'NET'
    GROSS_WORDS = 'GROSSWORDS'
    INVOICE_REASON = 'INVOICEREASON'
    PROGRESSIVE = 'PROGRESSIVE'
    DATE = 'DATE'

    _template = None
    _data = {
        GROSS: 0,
        TAX: 0,
        NET: 0,
        GROSS_WORDS: 'zero/00',
        INVOICE_REASON: None,
        PROGRESSIVE: 0,
        DATE: None
    }

    @property
    def gross(self):
        return str(round(self._data[self.GROSS], 2))

    @gross.setter
    def gross(self, value):
        self._data[self.GROSS] = value

    @property
    def tax(self):
        return str(round(self._data[self.TAX], 2))

    @tax.setter
    def tax(self, value):
        self._data[self.TAX] = value

    @property
    def net(self):
        return str(round(self._data[self.NET], 2))

    @net.setter
    def net(self, value):
        self._data[self.NET] = value

    @property
    def gross_words(self):
        return self._data[self.GROSS_WORDS]

    @gross_words.setter
    def gross_words(self, value):
        self._data[self.GROSS_WORDS] = value

    @property
    def invoice_reason(self):
        return self._data[self.INVOICE_REASON]

    @invoice_reason.setter
    def invoice_reason(self, value):
        self._data[self.INVOICE_REASON] = value

    @property
    def progressive(self):
        return str(self._data[self.PROGRESSIVE])

    @progressive.setter
    def progressive(self, value):
        self._data[self.PROGRESSIVE] = value

    @property
    def date(self):
        return self._data[self.DATE].strftime('%d/%m/%Y')

    @date.setter
    def date(self, value):
        self._data[self.DATE] = value

    @property
    def date_file(self):
        return self._data[self.DATE].strftime('%Y%m%d-%H%M%S')

    # TODO: add template management.

    def ext_src(self):
        # TODO: implement in latex impl.
        return 'tex'

    def ext_out(self):
        # TODO: implement in latex impl.
        return 'pdf'

    def template(self):
        # TODO: implement in latex impl.
        return os.path.join(os.getcwd(), 'res', 'templates', 'tex', 'default', 'invoice', 'invoice.tex')

    def _generate_doc(self, out_dir, out_file):
        # TODO: implement in latex impl.
        try:
            from subprocess import DEVNULL  # py3k
        except ImportError:
            DEVNULL = open(os.devnull, 'wb')

        if configurator.debug:
            proc = subprocess.Popen(['pdflatex', '-output-directory', out_dir, out_file])
        else:
            proc = subprocess.Popen(['pdflatex', '-output-directory', out_dir, out_file], stdout=DEVNULL,
                                    stderr=subprocess.STDOUT)
        proc.communicate()
        return proc.returncode

    def generate(self):
        for x in self._data.values():
            if x is None:
                raise ValueError

        home_path = str(Path.home())
        out_dir = os.path.join(home_path, 'wpc-invoices')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        out_fn = os.path.join(out_dir, 'invoice_' + self.date_file)
        out_src_file = out_fn + '.' + self.ext_src()
        out_compiled_file = out_fn + '.' + self.ext_out()

        template_fn = self.template()

        with open(template_fn, 'r') as i:
            filedata = i.read()

        # replaces data.
        filedata = filedata.replace(self.GROSS, self.gross)
        filedata = filedata.replace(self.TAX, self.tax)
        filedata = filedata.replace(self.NET, self.net)
        filedata = filedata.replace(self.GROSS_WORDS, self.gross_words)
        filedata = filedata.replace(self.INVOICE_REASON, self.invoice_reason)
        filedata = filedata.replace(self.PROGRESSIVE, self.progressive)
        filedata = filedata.replace(self.DATE, self.date)

        # write out template to compile.
        with open(out_src_file, 'w') as o:
            o.write(filedata)

        if self._generate_doc(out_dir, out_src_file) == 0:
            return out_compiled_file
        else:
            return False
