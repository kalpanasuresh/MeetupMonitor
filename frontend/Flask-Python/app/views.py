from flask import render_template,Flask, jsonify
#from app import app, host, port, user, passwd, db
#from app.helpers.database import con_db
import happybase
import collections

app = Flask(__name__)

# To create a database connection, add the following
# within your view functions:
# con = con_db(host, port, user, passwd, db)
connection = happybase.Connection('ip-172-31-2-26')

# ROUTING/VIEW FUNCTIONS

@app.route('/meetup/top10groups')
def groups():
    table = connection.table('top10groups')
    rows = table.scan()
    data ={}
    datakey=[]
    datavalue=[]
    for key,value  in rows:
                    #print key
                #print value
        data[key]=int(value['cf:$1'])
        key=key.replace("'","")
    #        value = int(value)
              #    print key
        datavalue.append(int(data[key]))
    for key, value in sorted(data.iteritems(), key=lambda (k,v): (v,k),  reverse=True):
        print key
        print value
        datakey.append(key)
    return render_template('top10groups.html',data =datakey)

@app.route('/meetup/top20Topics')
def nothing():
    table = connection.table('top20Topics')
    rows = table.scan()
    data ={}
    datakey=[]
    datavalue=[]
    for key,value  in rows:
              #print key
                   #print value
        data[key]=int(value['cf:$1'])
        key=key.replace("'","")
                                  #        value = int(value)
    #    print key
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
        #print key
        #print value
        data[key]=int(value['cf:$1'])
        key=key.replace("'","")
        #        value = int(value)
#        print key
        i=25
    #    datavalue.append(int(data[key]))
    for key, value in sorted(data.iteritems(), key=lambda (k,v): (v,k),  reverse=True): 
        print key
        print value
        datakey.append(key)
        if i == 10:
            datavalue.append(10)
        else:
            datavalue.append(int(i*2))
            i=i-1
#        print "%s: %s" % (key, value)
    # Renders index.html.
    print datakey
    print datavalue
    return render_template('top100City.html',datakey=datakey,datavalue=datavalue)

@app.route('/home')
def home():
    # Renders home.html.
    return render_template('home.html')

@app.route('/slides')
def about():
    # Renders slides.html.
    return render_template('slides.html')

@app.route('/author')
def contact():
    # Renders author.html.
    return render_template('author.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

#@app.errorhandler(500)
#def internal_error(error):
#    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run("0.0.0.0" , debug = True)

