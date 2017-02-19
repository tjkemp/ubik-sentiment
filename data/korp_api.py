import json
import requests

def collect_data():

  #  https://korp.csc.fi/cgi-bin/korp.cgi?command=query&defaultcontext=1+text&defaultwithin=text&show=sentence,paragraph,lemma&show_struct=text_title,text_date,text_time,text_sect,text_sub,text_user,sentence_id,text_urlmsg,text_urlboard&start=0&end=9&corpus=S24&cqp=%5Blemma+%3D+%22Ruotsi%22%5D&cqp1=%5Blemma+%3D+%22Suomi%22%5D&indent=2

    cqp_query='([word = "\:\)"]|[word = "\:\("])' # :, ( and ) characters are escaped with \

    extra='&defaultcontext=1+sentence&defaultwithin=sentence&show=sentence,paragraph,lemma,pos&show_struct=sentence_id&start=0&end=100000'

    url="https://korp.csc.fi/cgi-bin/korp.cgi?command={command}{extra_param}&corpus={corpus}&cqp={cqp}".format(command="query",extra_param=extra,corpus="S24",cqp=cqp_query)

    #print(url)
  
    returns=requests.get(url)

    data=returns.json()
   # print(data["kwic"][0]['tokens'])
    sent_ids=set()

    if "kwic" not in data:
        print("No results...")
        return
    for sent in data["kwic"]:
        idx=sent["structs"]["sentence_id"]
        if idx in sent_ids:
            continue
        sent_ids.add(idx) # print only unique hits
        print(" ".join(token["word"] for token in sent['tokens'] if token["word"] is not None).encode('utf-8'))
        #print("")
    #print(url)
    #print(len(sent_ids),"unique sentences")


collect_data()

