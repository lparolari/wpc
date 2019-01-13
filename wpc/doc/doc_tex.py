import os

from .doc import Doc


class DocTex(Doc):

    def ext_src(self):
        return 'tex'

    def template(self):
        return os.path.join(os.getcwd(), 'res', 'templates', 'tex', 'default', 'invoice', 'invoice.tex')
