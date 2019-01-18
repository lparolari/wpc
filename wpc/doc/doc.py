import wpc
import glob
import os
import re
import subprocess
from pathlib import Path


class Doc(object):

    _configurator = wpc.config.Configurator()

    # configurations.
    _clear_sources = True
    _debug = False

    _data = {}

    def __init__(self) -> None:
        super().__init__()
        self._debug = self._configurator.debug
        self._clean_sources = self._configurator.clear_sources

    def ext_src(self):
        """
        :return: The file extension of source to compile.
        """
        raise NotImplementedError("This method should be implemented")

    def ext_out(self):
        """
        :return: The file extension of the output.
        """
        return 'pdf'

    def template(self):
        """
        :return: The template filename.
        """
        raise NotImplementedError("This method should be implemented")

    @property
    def date_file(self):
        """
        :return: The formatted datetime for filename.
        """
        raise NotImplementedError("This method should be implemented")

    def _generate_doc(self, out_dir, out_file):
        # TODO: implement in latex impl.
        try:
            from subprocess import DEVNULL  # py3k
        except ImportError:
            DEVNULL = open(os.devnull, 'wb')

        if self._debug:
            proc = subprocess.Popen(['pdflatex', '-output-directory', out_dir, out_file])
        else:
            proc = subprocess.Popen(['pdflatex', '-output-directory', out_dir, out_file], stdout=DEVNULL,
                                    stderr=subprocess.STDOUT)
        proc.communicate()
        return proc.returncode

    @staticmethod
    def _replace_whole(key, val, filedata):
        return re.sub(r'\b%s\b' % re.escape(key), val, filedata)

    def replace(self, filedata):
        """
        Search and replaces the keys with their values in template.

        :param filedata: A string containing the template data.
        :return: A string with replaced data in template.
        """
        raise NotImplementedError("This method should be implemented")

    def generate(self):
        """
        Generates the document from the template, replacing keys with their values.
        :return: Compiled filename if success, False otherwise.
        """
        for key, val in self._data.items():
            # print(key + ": " + str(val))
            if val is None:
                raise ValueError('Cannot generate a document: %s is None' % key)

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
        filedata = self.replace(filedata)

        # write out template to compile.
        with open(out_src_file, 'w') as o:
            o.write(filedata)

        if self._generate_doc(out_dir, out_src_file) == 0:
            if self._clear_sources:
                cleanup_files = glob.glob(out_fn + '.*')
                cleanup_files.remove(out_compiled_file)
                [os.remove(file) for file in cleanup_files]

            return out_compiled_file
        else:
            return False
