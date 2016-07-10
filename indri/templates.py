from string import Template


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
