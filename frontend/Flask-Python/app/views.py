from flask import render_template,Flask, jsonify
import happybase
import collections
import os

app = Flask(__name__)

#HBase Connections
connection = happybase.Connection('ip-172-31-2-26')

# ROUTING/VIEW FUNCTIONS

@app.route('/meetup/top10groups')
def groups():
    table = connection.table('top10groups')
    rows = table.scan()
    rowData ={}
    sortedData=[]
    for key,value  in rows:
       
        key = key.replace("(","").replace(")","")
       
        rowData[key]=int(value['cf:$1'])
        
    for key, value in sorted(rowData.iteritems(), key=lambda (k,v): (v,k),  reverse=True):
        sortedData.append(key)
    return render_template('top10groups.html',data =sortedData)

@app.route('/meetup/top20Topics')
def Topics():
    table = connection.table('top20Topics')
    rows = table.scan()
    rowData ={}
    sortedData=[]
    
    for key,value  in rows:
        
        key = key.replace("(","").replace(")","")
        
        rowData[key]=int(value['cf:$1'])

    for key, value in sorted(rowData.iteritems(), key=lambda (k,v): (v,k),  reverse=True):
        sortedData.append(key)
    
    return render_template('top20Topics.html',data =sortedData)

@app.route('/meetup/<string:taskName>')
def indexi(taskName):
    table = connection.table(taskName)
    data ={}
    rows =table.scan()
    datakey =[]
    datavalue=[]
    for key,value  in rows:
        key = key.replace("(","").replace(")","")
        data[key]=int(value['cf:$1'])
        key=key.replace("'","")
    #set font size for word cloud
        i=25
    for key, value in sorted(data.iteritems(), key=lambda (k,v): (v,k),  reverse=True): 
        datakey.append(key)
        if i == 10:
            datavalue.append(10)
        else:
            datavalue.append(int(i*2))
            i=i-1
    return render_template('top100City.html',datakey=datakey,datavalue=datavalue)


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
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5007')), debug=False, threaded=True)

