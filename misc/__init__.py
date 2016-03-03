import requests
import urllib
from string import Template
import codecs

__all__ = ["crawl_url", "gene_indri_query_file", "gene_indri_text_file"]

_query_template = Template("""
<query>
    <number>$qid</number>
    <text>$q_string</text>
</query>
""")

_structure_template = Template("""
    <parameters>
    <index>$index</index>
    <trecFormat>true</trecFormat>
    <runID>$run_id</runID>
    <count>$count</count>
    $query_body
    </parameters>
""")

_text_template = Template("""
<DOC>
    <DOCNO>$did</DOCNO>
    <TEXT>$text</TEXT>
</DOC>
""")


def crawl_url(end_point,params={}):
    #time.sleep(5)
    headers = {
      # 'authority':'www.google.com',
      # 'scheme':'https',
      #'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'upgrade-insecure-requests':'1',
      #'Accept-encoding':'gzip, deflate, sdch',
      #'avail-dictionary':'IbMfuVbz,NcBB4MrI',
      'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4'
      #'upgrade-insecure-requests':'1',
      #'x-client-data':'CKO2yQE='
      #'referer':'http://www.google.com/search?q=nepal%2Bearthquake&tbm=nws&tbs=cdr%3A1%2Ccd_min%3A4%2F25%2F2015%2Ccd_max%3A04%2F29%2F2015&gws_rd=ssl'

    }
    try:
        r=requests.get(end_point,params=params,headers=headers)
        if r.status_code != requests.codes.ok:
          r.raise_for_status()
        # else:
        #   print "got url %s" %r.url
        #print r.url
        #print r.request.headers
        #print r.headers
    except requests.exceptions.HTTPError as error:
        print "http erro occur when the url is:", r.url
        print error
        return r.url, None

    except Exception as e:
        print "other exceptions"
        print e
        url = end_point
        params_list = []
        for p in params:
          params_list.append(p+"="+params[p])
        url += "&".join(params_list)
        url = urllib.unquote(url)
        return url, None
    else:
        return None,r.text



def gene_indri_query_file(file_path,queries,index,count,run_id="Infolab"):

    """
    generate indri query
    """
    

    query_body = ""
    for qid in queries:
        query_body+=_query_template.substitute(qid=qid,q_string=queries[qid].lower())

    with codecs.open(file_path, 'w','utf-8') as f:
        f.write(_structure_template.substitute(query_body=query_body,index=index,run_id=run_id,count=str(count)))




def gene_indri_text_file(file_path,texts):
    
    """
    generate indri text file
    """


    with codecs.open(file_path, 'w','utf-8') as f:
        for did in texts:
            text = texts[did].lower()
            f.write(_text_template.substitute(did=did,text=text))