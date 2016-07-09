"""
generate indri files
"""


from string import Template
from other import get_stopwords
import langid
import codecs
import re


query_template = Template("""
<query>
\t<number>$qid</number>
\t<text>$q_string</text>
</query>
""")


structure_template = Template("""
<parameters>
<index>$index</index>
<trecFormat>true</trecFormat>
<runID>$run_id</runID>
<count>$count</count>
$query_body
$rule
$stopper
</parameters>""")

index_para_template = Template("""
<parameters>
<index>$index_path</index>
<memory>$memory</memory>
$corpora
<stemmer><name>$stemmer</name></stemmer>
$fields
$stopper
</parameters>""")

corpus_template = Template("""
<corpus>
\t<path>$path</path>
\t<class>trectext</class>
</corpus>
""")

text_template = Template("""
<DOC>
\t<DOCNO>$did</DOCNO>
\t<TEXT>$text</TEXT>$fields
</DOC>""")

class IndriQueryFactory(object):
    """Take in query related parameters for indri and
    generate indri query file
    """
    def __init__(self,count,rule=None,
            use_stopper=False,date_when=None,
            numeric_compare=None):

        self._count,self._rule,self._use_stopper = 
                count,rule,use_stopper

        

        if date_when:
            if date_when not in ["dateafter","datebefore", "datebetween"]:
                raise ValueError("When value %s is not supported" %(date_when))

        if numeric_compare is not None:
            if numeric_compare not in ["less","greater","between","equals"]:
                raise ValueError("Compare value %s is not supported" %(numeric_compare))


        self._date_when,self._numeric_compare = 
                date_when,numeric_compare


    def _gene_query(self,file_path,queries,index,
                date_value=None,numeric_value=None,
                numeric_field_name=None):

        query_body = ""
        if self._rule is None:
            rule = ""
        else:
            rule = "<rule>%s</rule>" %self._rule

        if self._use_stopper:
            stopper = "<stopper>\n"
            stopwords = get_stopwords()
            for stopword in stopwords:
                stopper += "<word>%s</word>\n" %stopword 
            stopper += "</stopper>"
        else:
            stopper = ""

        for qid in queries:

            sinlge_query_data = queries[qid]
            if isinstance(sinlge_query_data,str):
                q_string = sinlge_query_data.lower()
                q_string = "#combine(%s)" %(q_string)

            elif isinstance(sinlge_query_data,list):
                q_string = " ".join(sinlge_query_data)
                q_string = "#combine(%s)" %(q_string)
            
            elif isinstance(sinlge_query_data,dict):
                q_string = ""
                for term in sinlge_query_data:
                    weight = sinlge_query_data[term]
                    q_string += "%f %s " %(weight,term)

                q_string = "#weight(%s)" %(q_string)
            else:
                raise TypeError("unsupported value type %s for query data" %type(sinlge_query_data))

            q_string = re.sub("[^\w]"," ",q_string)
            if self._date_when:
                q_string = "#filrej(#%s(%s) %s)" %(self._date_when,date_value,
                                                        q_string)
            
            if self._numeric_compare is not None:
                q_string = "#filrej(#%s(%s %d) %s)" %(self._numeric_compare,
                                            numeric_field_name,numeric_value,q_string)

            query_body+=query_template.substitute(
                qid=qid,q_string=q_string)

        with codecs.open(file_path, 'w','utf-8') as f:
            f.write(structure_template.substitute(query_body=query_body,index=index,
                                                  run_id=run_id,count=str(count),
                                                  rule=rule,stopper=stopper))


    def gene_query_with_date_filter(self,file_path,queries,index,
                date_value):

        self._gene_query(file_path,queries,index,date_value=date_value)


    def gene_query_with_numeric_filter(self,file_path,queries,index,
            numeric_value,numeric_field_name):

        self._gene_query(file_path,queries,index,,numeric_value=numeric_value,
                numeric_field_name=numeric_field_name)


def gene_indri_query_file(file_path,queries,index,count,
        run_id="Infolab",rule=None,use_stopper=False,
        date=None,numeric=None):

    """
    generate indri query
    saved for backward comparability
    use IndriQueryFactory instead
    """



    query_body = ""
    if rule is None:
        rule = ""
    else:
        rule = "<rule>%s</rule>" %rule

    if use_stopper:
        stopper = "<stopper>\n"
        stopwords = get_stopwords()
        for stopword in stopwords:
            stopper += "<word>%s</word>\n" %stopword 
        stopper += "</stopper>"
    else:
        stopper = ""

    for qid in queries:
        q_string = queries[qid].lower()
        q_string = re.sub("[^\w]"," ",q_string)
        if date:
            when = date["when"]
            if when not in ["dateafter","datebefore", "datebetween"]:
                raise ValueError("When value %s is not supported" %(when))
            
            date_value = date["value"]
            q_string = "#filrej(#%s(%s) #combine(%s))" %(when,date_value,q_string)
        if numeric is not None:
            compare = numeric["compare"]
            if compare not in ["less","greater","between","equals"]:
                raise ValueError("Compare value %s is not supported" %(compare))
            numeric_field_name = numeric["numeric_field_name"]
            numeric_value = numeric["value"]
            q_string = "#filrej(#%s(%s %d) #combine(%s))" %(compare,numeric_field_name,
                                                numeric_value,q_string)

        query_body+=query_template.substitute(
            qid=qid,q_string=q_string)

    with codecs.open(file_path, 'w','utf-8') as f:
        f.write(structure_template.substitute(query_body=query_body,index=index,
                                              run_id=run_id,count=str(count),
                                              rule=rule,stopper=stopper))


def gene_indri_index_para_file(corpora_list,file_path,index_path,memory='2G',stemmer='porter',use_stopper=False,field_data=None):

    
    
    if isinstance(memory,int):
        memory = str(memory)+'G'
    if isinstance(memory,str):
        if memory.isdigit():
            memory+='G'


    corpora = ""
    if isinstance(corpora_list,str):
        corpora = corpus_template.substitute(path=corpora_list)
    else:
        for corpus_path in corpora_list:
            corpora += corpus_template.substitute(path=corpus_path)
    if use_stopper:
        stopper = "<stopper>\n"
        stopwords = get_stopwords()
        for stopword in stopwords:
            stopper += "<word>%s</word>\n" %stopword 
        stopper += "</stopper>"
    else:
        stopper = ""

    fields = ""
    if field_data:
        for field in field_data:
            single_field = ""
            for tag in field:
                single_field += "\t<%s>%s</%s>\n" %(tag,field[tag],tag)
            single_field = "<%s>\n%s</%s>\n" %("field",single_field,"field")
            fileds += single_field

    with codecs.open(file_path, 'w','utf-8') as f:
        f.write(index_para_template.substitute(
                index_path=index_path,
                memory=memory,corpora=corpora,
                stemmer=stemmer,stopper=stopper,
                fields=fields))



def gene_single_indri_text(did,original_text,extra_fields=None,
        field_data=None):
    """generate a text piece for a single document

    """
    
    field_template = Template("\t<$field_name>$field_text</$field_name>\n")
    original_text = original_text.lower()
    lan = langid.classify(original_text)[0]
    if lan != 'en':
        return None
    else:    
        if extra_fields is None:
            fields = ""
        else:
            
            fields = "\n"
            for field_name in extra_fields:       
                field_text = field_data[field_name]
                fields += field_template.substitute(field_name=field_name,
                                    field_text=field_text)
        single_text = text_template.substitute(did=did,text=original_text,fields=fields)
        return single_text



def gene_indri_text_file(file_path,texts,extra_fields=None,
        field_data=None):
    
    """
    generate indri text file
    """


    with codecs.open(file_path, 'w','utf-8') as f:
        for did in texts:
            if extra_fields is None:
                single_text = gene_single_indri_text(did,texts[did])
            else:
                single_text = gene_single_indri_text(did,texts[did],extra_fields,field_data[did])
            if single_text is not None:
                f.write(single_text+"\n")
