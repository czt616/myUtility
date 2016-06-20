"""
generate indri files
"""


from string import Template
import langid
import codecs

query_template = Template("""
<query>
    <number>$qid</number>
    <text>$q_string</text>
</query>
""")

structure_template = Template("""
<parameters>
<index>$index</index>
<trecFormat>true</trecFormat>
<runID>$run_id</runID>
<count>$count</count>
$query_body
</parameters>
""")

index_para_template = Template("""
<parameters>
<index>$index_path</index>
<memory>$memory</memory>
$corpora
<stemmer><name>$stemmer</name></stemmer>
</parameters>
""")

corpus_template = Template("""
<corpus>
  <path>$path</path>
  <class>trectext</class>
</corpus>
""")

text_template = Template("""
<DOC>
    <DOCNO>$did</DOCNO>
    <TEXT>$text</TEXT>$fields
</DOC>
""")

def gene_indri_query_file(file_path,queries,index,count,run_id="Infolab"):

    """
    generate indri query
    """



    query_body = ""
    for qid in queries:
        query_body+=query_template.substitute(qid=qid,q_string=queries[qid].lower())

    with codecs.open(file_path, 'w','utf-8') as f:
        f.write(structure_template.substitute(query_body=query_body,index=index,run_id=run_id,count=str(count)))


def gene_indri_index_para_file(corpora,file_path,index_path,memory='2G',stemmer='porter'):

    
    
    if isinstance(memory,int):
        memory = str(memory)+'G'
    if isinstance(memory,str):
        if memory.isdigit():
            memory+='G'


    corpora = ""
    for corpus_path in corpora:
        corpora += corpus_template.substitute(path=corpus_path)

    with codecs.open(file_path, 'w','utf-8') as f:
        f.write(index_para_template.substitute(index_path=index_path,
            memory=memory,corpora=corpora,stemmer=stemmer))



def gene_single_indri_text(did,original_text,extra_fields=None,
        field_data=None):
    """generate a text piece for a single document

    """
    
    field_template = Template("\t<$field_name>$field_text</$field_name>\n")
    original_text = original_text.lower()

    if extra_fields is None:
        fields = ""
    else:
        text = texts[did].lower()
        lan = langid.classify(text)[0]
        if lan != 'en':
            return None
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
