from flask import render_template,Flask, jsonify
import happybase
import collections

app = Flask(__name__)

#HBase Connections
connection = happybase.Connection(<HBase IP Addr>)

# ROUTING/VIEW FUNCTIONS

@app.route('/meetup/top10groups')
def groups():
    table = connection.table('top10groups')
    rows = table.scan()
    data ={}
    datakey=[]
    datavalue=[]
    for key,value  in rows:
        data[key]=int(value['cf:$1'])
        key=key.replace("'","")
        datavalue.append(int(data[key]))
    for key, value in sorted(data.iteritems(), key=lambda (k,v): (v,k),  reverse=True):
        datakey.append(key)
    return render_template('top10groups.html',data =datakey)

@app.route('/meetup/top20Topics')
def Topics():
    table = connection.table('top20Topics')
    rows = table.scan()
    data ={}
    datakey=[]
    datavalue=[]
    for key,value  in rows:
        data[key]=int(value['cf:$1'])
        key=key.replace("'","")
        datavalue.append(int(data[key]))
    for key, value in sorted(data.iteritems(), key=lambda (k,v): (v,k),  reverse=True):
        print key
        print value
        datakey.append(key)
    return render_template('top20Topics.html',data =datakey)

@app.route('/meetup/<string:taskName>')
def indexi(taskName):
    table = connection.table(taskName)
    data ={}
    rows =table.scan()
    datakey =[]
    datavalue=[]
    for key,value  in rows:
        data[key]=int(value['cf:$1'])
        key=key.replace("'","")
    #set font size
        i=25
    for key, value in sorted(data.iteritems(), key=lambda (k,v): (v,k),  reverse=True): 
        datakey.append(key)
        if i == 10:
            datavalue.append(10)
        else:
            datavalue.append(int(i*2))
            i=i-1
    return render_template('top100City.html',datakey=datakey,datavalue=datavalue)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run("0.0.0.0" , debug = True)

