from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape


class Doc(object):

    _doc = Document('basic')

    def doc_structure(self):
        with self._doc.create(Section('A second section')):
            self._doc.append('Some text.')

    def content(self):
        with self._doc.create(Section('A section')):
            self._doc.append('Some regular text and some ')
            self._doc.append(italic('italic text. '))

            with self._doc.create(Subsection('A subsection')):
                self._doc.append('Also some crazy characters: $&#{}')
        #raise NotImplementedError


    def generate(self, file):
        self._doc.generate_pdf('basic_maketitle2', clean_tex=False)
