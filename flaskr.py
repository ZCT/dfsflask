#coding:utf-8
import sqlite3
import os,sys
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_file,send_from_directory
from flask.ext.paginate import Pagination
#from
from contextlib import closing
from search import sphinx_search

reload(sys)
sys.setdefaultencoding('utf-8')
PROJECT_DIR = os.getcwd()
downloadfile_url='http://222.201.139.210:8888/group1/M00'
#configuration
DATABASE = PROJECT_DIR + '/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
RESULTS_PER_PAGE = 10

#create our app
app = Flask(__name__)
app.add_url_rule('/templates'+'/<path:filename>',endpoint='templates',view_func=app.send_static_file)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    pass


@app.teardown_request
def teardown_request(exception):
    pass


@app.route('/show')
def show_entries():
    keyword = request.form['Text']
    entries = dict(title=keyword, text=keyword)
    return render_template('show_entries.html', entries=entries)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged_in')
            return render_template('show_entries.html', show_result=False)
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/result',methods=['GET'])
def showresult(entries):
    try:
        page=int(request.args.get('page',1))
    except ValueError:
        page=1
    pagination=Pagination(page=page, total=len(entries), search=False, css_framework='foundation')
    return render_template('show_entries.html', entries=entries, pagination=pagination,show_result=True)

entries=[]

def get_entry_for_page(page,length,entries):
    entry_page=[]
    for i in range(10):
        index= page*10-10+i
        if index < len(entries):
            entry_page.append(entries[index])
    return entry_page

def download(filename):
    global downloadfile_url
    file_url=downloadfile_url
    index1=filename.find("dirname=")
    index2=filename.find(",",index1)
    file_url+=filename[index1+8:index2]
    index1=filename.find("storagename=")
    index2=filename.find(",",index1)
    file_url+=filename[index1+12:index2]
    index1=filename.find("format=")
    index2=filename.find(",",index1)
    file_url+=filename[index1+7:index2]
    index1=filename.find("abstract=")
    index2=filename.find(",",index1)
    abstract=filename[index1+9+3:index2]

    print abstract
    #print filename_2
    #return app.send_file("1.txt")
    #return send_from_directory(app.static_folder,filename_2)
    #print url_for('templates', filename='style.css')
    #print downloadfile_url
    return tuple((abstract,file_url))
    #return redirect(downloadfile_url)
    #return send_from_directory('/home/t-mac/code/coreseek/coreseek-4.1-beta/testpack/etc/pysource/test_mmseg/',filename=filename_2)
    #return redirect(url_for('templates', filename='flaskr.db'))
    #return redirect(url_for('/home/t-mac/code/coreseek/coreseek-4.1-beta/testpack/etc/pysource/test_mmseg/', filename=filename_2))

@app.route('/search', methods=['GET','POST'])
def search():
    global entries
    page=1
    if not session.get('logged_in'):
        abort(401)
    if request.method=='POST':
        entries=[]

        keyword = request.form['Text']
        flash('The matched result for   '+  keyword  +'   is:')
        entries = sphinx_search(keyword)
    else:
        try:
            page=int(request.args.get('page',1))
        except ValueError:
            page=1
    page_entries=get_entry_for_page(page,10,entries)
    #print page_entries
    pagination=Pagination(page=page, total=len(entries), search=False, record_name='result')
    url_file=[]
    for entry in page_entries:
        #print download(entry)
        url_file.append(download(entry))
    return render_template('show_entries.html', entries=url_file, pagination=pagination,show_result=True)





#app.add_url_rule('/home/t-mac/code/coreseek/coreseek-4.1-beta/testpack/etc/pysource/test_mmseg/'+'<path:filename>',view_func=app.send_static_file)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33506))
    app.run(host='0.0.0.0', port=port)
