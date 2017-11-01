"""
parse an HTML file to clean text or sentences
"""

#from goose import Goose, Configuration
from ..misc import do_stem
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
import lxml
import re



class Html_parser(object):
    """
    use goose to parse raw html and
    """
    def __init__(self,need_stem):
        self._need_stem = need_stem

    def get_text(self,file_path):
        raw_html = ""
        with open(file_path) as f:
            raw_html = f.read()

        if not raw_html:
            return None
        try:
            soup = BeautifulSoup(raw_html,"lxml")
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            text = re.sub("\s+"," ",soup.get_text())
        except lxml.etree.ParserError as e:
            return None

        else:
            if self._need_stem:
                text = re.sub("\w+",do_stem,text)
                #words = re.findall("\w+",text,re.MULTILINE)
                #w = map(stem,words)
                #text = " ".join(w)
        return text

    def get_sentences(self,file_path):
        text = self.get_text(file_path)
        return sent_tokenize(text)
