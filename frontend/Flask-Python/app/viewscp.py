
# -*- coding: utf-8 -*-
from flask import render_template,Flask, jsonify
import happybase
import collections
import os
import sys



reload(sys)
sys.setdefaultencoding("utf-8")


app = Flask(__name__)

#HBase Connections
connection = happybase.Connection('ip-172-31-2-26')




@app.route('/meetup')
def index():

    groupstable = connection.table('top10groups')
    groupsrows = groupstable.scan()
    groupsrowData ={}
    groupssortedData=[]
    results = []
    entrykey=[]
    entrykey.append('Name')
    entrykey.append('count')
    results.append(entrykey)
    for key,value  in groupsrows:
        entrykey=[]
        entrykey.append(key)
        entrykey.append(int(value['cf:$1']))
        results.append(entrykey)
        
        
        
        key = key.replace("(","").replace(")","")
        groupsrowData[key]=value['cf:$1']
    for key, value in sorted(groupsrowData.iteritems(), key=lambda (k,v): (v,k),  reverse=True):
        groupssortedData.append(key+','+value)
    datagroups =results
    print datagroups

    topicstable = connection.table('top20Topics')
    topicsrows = topicstable.scan()
    topicsrowData ={}
    topicssortedData=[]
    for key,value  in topicsrows:
        key = key.replace("(","").replace(")","")
        topicsrowData[key]=int(value['cf:$1'])
    for key, value in sorted(topicsrowData.iteritems(), key=lambda (k,v): (v,k),  reverse=True):
        topicssortedData.append(key)

    

    citytable = connection.table('top100City')
    citydata ={}
    cityrows =citytable.scan()                                     
    citydatakey=[]
    citydatavalue=[]
    
    for key,value  in cityrows:
        key = key.replace("(","").replace(")","")
        citydata[key]=int(value['cf:$1'])
        key=key.replace("'","")
        #set font size for word cloud
        i=25
    for key, value in sorted(citydata.iteritems(), key=lambda (k,v): (v,k),  reverse=True): 
        citydatakey.append(key)
        if i == 10:
           citydatavalue.append(10)
        else:
           citydatavalue.append(int(i*2))
           i=i-1
    return render_template('top10groups.html',datakey=citydatakey,datavalue=citydatavalue,datagroups=datagroups,datatopics=topicssortedData)




@app.route('/meetup/topicBycity/<string:taskName>')
def indexCity(taskName):
        topics=""
        table = connection.table('topicBycity')

        rows =table.row(taskName)
        topics =rows['topics:topic']
        # print topics
        #topics = rows[taskName]
        topics.replace("{","")
        topics.replace("}","")
        topics.replace("(","")
        topics.replace(")","")
        print topics
        return render_template('topicBycity.html',data =topics)
#        return stringify(rows['cf1:$1'])



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5007')), debug=True, threaded=True)

