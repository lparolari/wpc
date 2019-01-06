import re

from num2words import num2words

from doc.doc_tex import DocTex


class InvoiceTexDoc(DocTex):

    def __init__(self) -> None:
        super().__init__()
        self.gross = 0
        self.gross_words = 0
        self.tax = 0
        self.net = 0
        self.date = None
        self.reason = None
        self.progressive = 0

    # const to replace in template.
    GROSS = 'GROSS'
    TAX = 'TAX'
    NET = 'NET'
    GROSS_WORDS = 'GROSSWORDS'
    REASON = 'INVOICEREASON'
    PROGRESSIVE = 'PROGRESSIVE'
    DATE = 'DATE'

    # dict for data to replace in template.
    _data = {
        GROSS: 0,
        TAX: 0,
        NET: 0,
        GROSS_WORDS: 'zero/00',
        REASON: None,
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
        self._data[self.GROSS_WORDS] = num2words(int(round(float(value), 0)), lang='it')

    @property
    def reason(self):
        return self._data[self.REASON]

    @reason.setter
    def reason(self, value):
        self._data[self.REASON] = value

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

    def set_invoice(self, gross, tax, net, datetime, reason, prog):
        self.gross = gross
        self.gross_words = gross
        self.tax = tax
        self.net = net
        self.date = datetime
        self.reason = reason
        self.progressive = prog

    def set_invoice_from(self, invoice):
        self.set_invoice(invoice.gross, invoice.tax, invoice.net, invoice.emitted_at, invoice.reason, invoice.prog)

    @property
    def date_file(self):
        return self._data[self.DATE].strftime('%Y%m%d-%H%M%S')

    def replace(self, filedata):

        filedata = super()._replace_whole(self.GROSS, self.gross, filedata)
        filedata = super()._replace_whole(self.TAX, self.tax, filedata)
        filedata = super()._replace_whole(self.NET, self.net, filedata)
        filedata = super()._replace_whole(self.REASON, self.reason, filedata)
        filedata = super()._replace_whole(self.PROGRESSIVE, self.progressive, filedata)
        filedata = super()._replace_whole(self.DATE, self.date, filedata)
        filedata = super()._replace_whole(self.GROSS_WORDS, self.gross_words, filedata)

        return filedata
