"""
generate indri files
"""


from string import Template
import codecs

def gene_indri_query_file(file_path,queries,index,count,run_id="Infolab"):

    """
    generate indri query
    """

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

    query_body = ""
    for qid in queries:
        query_body+=query_template.substitute(qid=qid,q_string=queries[qid].lower())

     with codecs.open(file_path, 'w','utf-8') as f:
        f.write(structure_template.substitute(query_body=query_body,index=index,run_id=run_id,count=str(count)))




def gene_indri_text_file(file_path,texts):
    
    """
    generate indri text file
    """

    text_template = Template("""
    <DOC>
        <DOCNO>$did</DOCNO>
        <TEXT>$text</TEXT>
    </DOC>
    """)

    with codecs.open(file_path, 'w','utf-8') as f:
        for did in texts:
            text = texts[did].lower()
            f.write(text_template.substitute(did=did,text=text))
