# all the imports
import sqlite3
import os
from werkzeug import secure_filename
import os.path
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash,Response
import json
import re

# configuration
DATABASE = 'project.db'
DEBUG = True
SECRET_KEY = 'development key'
visited = 0


USERNAME1 = 'sullivan'
PASSWORD1 = 'sullivan'
USERNAME2 = 'warzoski'
PASSWORD2 = 'warzoski'
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == app.config['USERNAME1'] and request.form['password'] == app.config['PASSWORD1']:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('homepage'))
        elif request.form['username'] == app.config['USERNAME2'] and request.form['password'] == app.config['PASSWORD2']:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('homepage'))
        else:
            error='invalid password or username'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('homepage'))


@app.route('/')
def homepage():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    data=[]
    a = g.db.execute('SELECT * FROM professor')
    a = a.fetchall()
    data.append(len(a))
    a = g.db.execute('SELECT * FROM monsterstudent')
    a = a.fetchall()
    data.append(len(a))
    a = g.db.execute('SELECT * FROM course')
    a = a.fetchall()
    data.append(len(a))
    a = g.db.execute('SELECT * FROM seminar')
    a = a.fetchall()
    data.append(len(a))
    return render_template('home.html',data=data)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++picture upload
app.config['UPLOAD_FOLDER'] = 'static/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/addprofessor', methods=['POST'])
def upload():
    a = g.db.execute('SELECT * FROM professor')
    a = a.fetchall()
    num=len(a)+1
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = "professor"+str(num)+os.path.splitext(secure_filename(file.filename))[1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       # return redirect(url_for('/professor'))

    g.db.execute('insert into professor (name, research, professorid, title) values (?, ?,?)',
                 [request.form['name'], request.form['research'], num,request.form['title']])
    g.db.commit()
    #f = request.files['the_file']
    #f.save('/1.jpg')
    flash('New professor was successfully posted')
    return redirect(url_for('show_professor'))
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.route('/professor')
def show_professor():
    area=request.args.get('area')
    prof=request.args.get('prof')
    order=request.args.get('order')
    order=str(order)
    professors = g.db.execute('SELECT Name, Research,professorid FROM professor')
    professors = professors.fetchall()
    if area or prof:
        if not area:
            if not order:
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where name='%s'" %request.args.get('prof'))
                professors = professors.fetchall()
            elif order=="Descending by Name":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where name='%s' order by name desc" %request.args.get('prof'))
                professors = professors.fetchall()
            elif order=="Descending by Research":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where name='%s' order by research desc" %request.args.get('prof'))
                professors = professors.fetchall()
            elif order=="Ascending by Name":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where name='%s' order by name" %request.args.get('prof'))
                professors = professors.fetchall()
            elif order=="Ascending by Research":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where name='%s' order by research" %request.args.get('prof'))
                professors = professors.fetchall()

        elif not prof:
            if not order:
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where research='%s'" %request.args.get('area'))
                professors = professors.fetchall()
            elif order=="Descending by Name":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where research='%s' order by name desc" %request.args.get('area'))
                professors = professors.fetchall()
            elif order=="Descending by Research":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where research='%s' order by research desc" %request.args.get('area'))
                professors = professors.fetchall()
            elif order=="Ascending by Name":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where research='%s' order by name" %request.args.get('area'))
                professors = professors.fetchall()
            elif order=="Ascending by Research":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where research='%s' order by research" %request.args.get('area'))
                professors = professors.fetchall()
        else:
            if not order:
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where research='%s' and name='%s'" %(request.args.get('area'),request.args.get('prof')))
                professors = professors.fetchall()
            elif order=="Descending by Name":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where research='%s' and name='%s' order by name desc" %(request.args.get('area'),request.args.get('prof')))
                professors = professors.fetchall()
            elif order=="Descending by Research":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where research='%s' and name='%s' order by research desc" %(request.args.get('area'),request.args.get('prof')))
                professors = professors.fetchall()
            elif order=="Ascending by Name":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where research='%s' and name='%s' order by name" %(request.args.get('area'),request.args.get('prof')))
                professors = professors.fetchall()
            elif order=="Ascending by Research":
                professors = g.db.execute("SELECT Name, Research,professorid FROM professor where research='%s' and name='%s' order by research" %(request.args.get('area'),request.args.get('prof')))
                professors = professors.fetchall()
            
        research = g.db.execute("SELECT distinct Research FROM professor")
        research = research.fetchall()
        names = g.db.execute("SELECT distinct name FROM professor")
        names = names.fetchall()
    else:
        if not order:
            professors = g.db.execute('SELECT Name, Research,professorid FROM professor')
            professors = professors.fetchall()
        elif order=="Descending by Name":
            professors = g.db.execute('SELECT Name, Research,professorid FROM professor order by name desc')
            professors = professors.fetchall()
        elif order=="Descending by Research":
            professors = g.db.execute('SELECT Name, Research,professorid FROM professor order by research desc')
            professors = professors.fetchall()
        elif order=="Ascending by Name":
            professors = g.db.execute('SELECT Name, Research,professorid FROM professor order by name')
            professors = professors.fetchall()
        elif order=="Ascending by Research":
            professors = g.db.execute('SELECT Name, Research,professorid FROM professor order by research')
            professors = professors.fetchall()

        research = g.db.execute("SELECT distinct Research FROM professor")
        research = research.fetchall()
        names = g.db.execute("SELECT distinct name FROM professor")
        names = names.fetchall()

    return render_template('show_professor.html', professors=professors, research=research,names=names)

@app.route('/deleteprofessor', methods=['POST'])
def delete_prof():
    a=request.form.getlist("delete")
    for i in a:
        g.db.execute('delete from professor where professor.name = ?',[i])
    g.db.commit()
    flash('successfully deleted')
    return redirect(url_for('show_professor'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        return render_template('search_homepage.html')

    elif request.method == "POST":
        search_str = request.form['searchbox']

        query = '''SELECT Professor.Name FROM
                        Professor WHERE
                        (Professor.name LIKE '%s' OR
                            Professor.Research LIKE '%s' OR
                            Professor.Title LIKE '%s'OR
                            Professor.Teaching LIKE '%s');''' % (search_str, search_str,search_str, search_str)

        found_professor = g.db.execute(query)
        found_professor = found_professor.fetchall()
        if len(found_professor) == 0:
            flag = 0
            #search_str = re.IGNORECASE(search_str)
            name_sets = g.db.execute('SELECT Name From professor').fetchall()
            name_sets2 = g.db.execute('SELECT DISTINCT Title From professor').fetchall()
            name_sets3 = g.db.execute('SELECT DISTINCT Teaching From professor').fetchall()
            name_sets = name_sets+name_sets2;
            name_sets = name_sets+name_sets3;
            for str in name_sets:
                #print str
                #print re.match(search_str,str[0])
                if re.match(search_str,str[0],re.I):
                    #print str[0]
                    #print 'wen'
                    found_professor.append(str[0])
        else:
            flag = 1

        return render_template('search_homepage.html', found_professor=found_professor, flag = flag )

@app.route('/search/<str>')
def search2(str):

    search_str = str

    query = '''SELECT Professor.Name FROM
                        Professor WHERE
                        (Professor.name LIKE '%s' OR
                            Professor.Research LIKE '%s' OR
                            Professor.Title LIKE '%s'OR
                            Professor.Teaching LIKE '%s');''' % (search_str, search_str,search_str, search_str)

    found_professor = g.db.execute(query)
    found_professor = found_professor.fetchall()

    flag = 1

    return render_template('search_homepage.html', found_professor=found_professor, flag = flag )



@app.route('/student')
def show_student():
    students = g.db.execute('SELECT Name, IndexOfScary  FROM MonsterStudent ')
    students = students.fetchall()
    #pdb.set_trace()
    return render_template('show_student.html', students=students)

@app.route('/addstudent', methods=['POST'])
def add_stud():
    g.db.execute('insert into MonsterStudent (Name,Major,IndexofScary) values (?, ?,?)',
                 [request.form['name'], request.form['major'],request.form['IndexOfScary']])
    g.db.commit()
    f = request.files['the_file']
    f.save('/1.jpg')
    flash('New student was successfully added')
    return redirect(url_for('show_student'))

@app.route('/deletestudent', methods=['POST'])
def delete_stud():
    a=request.form.getlist("delete")
    for i in a:
        g.db.execute('delete from MonsterStudent where student.Name = ?',[i])
    g.db.commit()
    flash('successfully deleted')
    return redirect(url_for('show_student'))

@app.route('/student/<student_name>')
def show_student_name(student_name):
    students = g.db.execute('SELECT * FROM MonsterStudent WHERE Name="%s"' %student_name )
    # the result will be a query object containing the (presumably!) single element
    # that corresponds to the artist we want
    students = students.fetchall()
    fraternity = g.db.execute('SELECT Name FROM Fraternity WHERE FraternityId = "%d"' %students[0][7])
    fraternity = fraternity.fetchall()[0]
    #students[0][7] = fraternity;
    return render_template('show_one_student.html', students=students,fraternity=fraternity)


@app.route('/gpacalculator', methods=['GET', 'POST'])
def gpacalculator():    
    sid = request.form['studentidforscore']
    datacal = g.db.execute('SELECT coursename, credit, grade FROM CourseScore WHERE studentid = "%s"' %sid)
    datacal = datacal.fetchall()
    lendata = len(datacal)
    if lendata >=1 :   
        return render_template('gpacal.html', datacal = datacal, lendata = lendata)
    else:
        return render_template('gpahome.html')  

@app.route('/gpahome', methods=['GET', 'POST'])#+++++++++++++++++++++++++++++++++----------
def gpahome():
    return render_template('gpahome.html')

@app.route('/autocompletelist')
def autocompletelist():
    return_list = list()
    name_sets = g.db.execute('SELECT Name From professor').fetchall()
        #print(name_sets)

    for name_set in name_sets:
        name_set = str(name_set)
        return_list.append(name_set[3:len(name_set)-3])
        print name_set[3:len(name_set)-3]
       # return_dic = {"nameList" , return_list}
    #self.response.headers['Content-Type'] = 'application/json'
    return_list.sort()
    #return_list = json.dumps(return_list)
    #return jsonify(return_list)
    return Response(json.dumps(return_list),  mimetype='application/json')

#---------------------------------------------------------

@app.route('/fraternity')
def show_fraternity():
    fraternities = g.db.execute('SELECT Name, Slogan, fraternityid FROM fraternity')
    fraternities = fraternities.fetchall()
    return render_template('show_fraternity.html', fraternities=fraternities)

@app.route('/addfraternity', methods=['POST'])
def add_fraternity():
    g.db.execute('insert into fraternity (name, slogan) values (?, ?)',
                 [request.form['name'], request.form['slogan']])
    g.db.commit()
    f = request.files['the_file']
    f.save('/1.jpg')
    flash('New fraternity was successfully posted')
    return redirect(url_for('show_fraternity'))

@app.route('/deletefraternity', methods=['POST'])
def delete_fraternity():
    a=request.form.getlist("delete")
    for i in a:
        g.db.execute('delete from fraternity where fraternity.name = ?',[i])
    g.db.commit()
    flash('successfully deleted')
    return redirect(url_for('show_fraternity'))

@app.route('/fraternity/<fraternity_name>')
def show_fraternity_name(fraternity_name):
    frat = g.db.execute('SELECT * FROM fraternity where Name="%s"' % fraternity_name)
    frat = frat.fetchall()
    return render_template('show_one_fraternity.html', frat=frat)
#--------------------------------------------------------------------------------------

@app.route('/club')
def show_club():
    clubs = g.db.execute('SELECT clubid, Name FROM club')
    clubs = clubs.fetchall()
    return render_template('show_club.html', clubs=clubs)

@app.route('/club/<club_name>')
def show_club_name(club_name):
    clubb = g.db.execute('SELECT * FROM club where Name="%s"' % club_name)
    clubb = clubb.fetchall()
    return render_template('show_one_club.html', clubb=clubb)

#---------------------------------------------------------------------------------------

@app.route('/activity')
def show_activity():
    activities = g.db.execute('SELECT activityid, Name FROM campusactivity')
    activities = activities.fetchall()
    return render_template('show_activity.html', activities=activities)

@app.route('/activity/<activity_name>')
def show_activity_name(activity_name):
    activityy = g.db.execute('SELECT * FROM campusactivity where Name="%s"' % activity_name)
    activityy = activityy.fetchall()
    return render_template('show_one_activity.html', activityy=activityy)


# professor comment==================================================

@app.route('/professor/<professor_name>')
def show_professr_name(professor_name):
    professors = g.db.execute("SELECT * FROM professor WHERE name = '%s'" %professor_name)
    professors = professors.fetchall()
    cur = g.db.execute("select title, content,name from professorcomment where professorname='%s' order by commentid desc" %professor_name)
    entries = [dict(title=row[0], text=row[1], name=row[2]) for row in cur.fetchall()]


    return render_template('show_one_professor.html', professors=professors, entries=entries)

@app.route('/add/<professor_name>', methods=['POST'])
def add_entry(professor_name):
    g.db.execute('insert into professorcomment (title, content,name,professorname) values (?,?,?, ?)',
                 [request.form['title'], request.form['text'],request.form['name'],professor_name] )
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect("/professor/%s" %professor_name)

# course part======================================================
@app.route('/course')
def show_course():
    courses = g.db.execute('SELECT course.Name,course.schedule,professor.name FROM course,professor where course.professorid = professor.professorid')
    courses = courses.fetchall()
    #pdb.set_trace()
    return render_template('show_courses.html', courses=courses)

@app.route('/addcourse', methods=['POST'])
def add_course():
    cou=g.db.execute("select * from course")
    cou=cou.fetchall()
    numprof=g.db.execute("select * from professor")
    numprof=numprof.fetchall()
    pro = g.db.execute("select * from professor where name='%s'" %request.form['professor'])
    pro=pro.fetchall()
    if len(pro)==0:
        g.db.execute('insert into professor (name, professorid) values (?, ?)',
                 [request.form['professor'], len(numprof)+1])
        g.db.execute('insert into course (courseid,name, schedule, professorid) values (?, ?,?,?)',
                 [len(cou)+1,request.form['name'], request.form['research'], len(numprof)+1])
    else:
        g.db.execute('insert into course (courseid,name, schedule, professorid) values (?, ?,?,?)',
                 [len(cou)+1,request.form['name'], request.form['research'], pro[0][0]])
        g.db.execute("UPDATE Professor SET teaching = '%s' WHERE professorid = %d" %(request.form['name'],pro[0][0]))
    g.db.commit()
    flash('New course was successfully added')
    return redirect('/course')

@app.route('/deletecourse', methods=['POST'])
def delete_course():
    a=request.form.getlist("delete")
    for i in a:
        g.db.execute('delete from course where course.name = ?',[i])
    g.db.commit()
    flash('successfully deleted')
    return redirect(url_for('show_course'))

# course comment==================================================

@app.route('/course/<course_name>')
def show_course_name(course_name):
    courses = g.db.execute("SELECT course.Name,course.schedule,professor.name  FROM course,professor where course.professorid = professor.professorid and course.name='%s'" % course_name)
    courses = courses.fetchall()
    cur = g.db.execute("select title, content,name from coursecomment where coursename='%s' order by commentid desc" %course_name)
    entries = [dict(title=row[0], text=row[1], name=row[2]) for row in cur.fetchall()]

    return render_template('show_one_course.html', courses=courses,entries=entries)

@app.route('/addd/<course_name>', methods=['POST'])
def add_courseentry(course_name):
    g.db.execute('insert into coursecomment (title, content,name,coursename) values (?,?,?, ?)',
                 [request.form['title'], request.form['text'],request.form['name'],course_name] )
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect("/course/%s" %course_name)


    # seminar part======================================================

@app.route('/seminar')
def show_seminar():
    seminars = g.db.execute('SELECT seminar.Name,speaker.name FROM seminar,speaker where seminar.speakerid = speaker.speakerid')
    seminars = seminars.fetchall()
    #pdb.set_trace()
    return render_template('show_seminars.html', seminars=seminars)

@app.route('/addseminar', methods=['POST'])
def add_seminar():
    cou=g.db.execute("select * from seminar")
    cou=cou.fetchall()
    numprof=g.db.execute("select * from speaker")
    numprof=numprof.fetchall()
    pro = g.db.execute("select * from speaker where name='%s'" %request.form['speaker'])
    pro=pro.fetchall()
    if len(pro)==0:
        g.db.execute('insert into speaker (name, speakerid) values (?, ?)',
                 [request.form['speaker'], len(numprof)+1])
        g.db.execute('insert into seminar (seminarid,name, speakerid) values (?, ?,?)',
                 [len(cou)+1,request.form['name'], len(numprof)+1])
    else:
        g.db.execute('insert into seminar (seminarid,name, speakerid) values (?, ?,?)',
                 [len(cou)+1,request.form['name'], pro[0][0]])
    g.db.commit()
    flash('New seminar was successfully added')
    return redirect('/seminar')

@app.route('/deleteseminar', methods=['POST'])
def delete_seminar():
    a=request.form.getlist("delete")
    for i in a:
        g.db.execute('delete from seminar where seminar.name = ?',[i])
    g.db.commit()
    flash('successfully deleted')
    return redirect(url_for('show_seminar'))

@app.route('/seminar/<seminar_name>')
def show_seminar_name(seminar_name):
    seminars = g.db.execute("SELECT seminar.Name,speaker.name,speaker.title  FROM seminar,speaker where seminar.speakerid = speaker.speakerid and seminar.name='%s'" % seminar_name)
    seminars = seminars.fetchall()
    return render_template('show_one_seminar.html', seminars=seminars)

#  dinning part======================================================

@app.route('/dining')
def show_dinning():
    dinnings = g.db.execute('SELECT * FROM dining')
    dinnings = dinnings.fetchall()
    #pdb.set_trace()
    return render_template('show_dinnings.html', dinnings=dinnings)

@app.route('/adddinning', methods=['POST'])
def add_dinning():
    g.db.execute('insert into dining (name, typeoffood,location) values (?, ?, ?)',
                 [request.form['name'], request.form['research'],request.form['location']])
    g.db.commit()
    flash('New dinning was successfully added')
    return redirect('/dinning')

@app.route('/deletedinning', methods=['POST'])
def delete_dinning():
    a=request.form.getlist("delete")
    for i in a:
        g.db.execute('delete from dining where dining.name = ?',[i])
    g.db.commit()
    flash('successfully deleted')
    return redirect(url_for('show_dinning'))

@app.route('/dinning/<dinning_name>')
def show_dinning_name(dinning_name):
    dinnings = g.db.execute("SELECT * FROM dining where dining.name='%s'" % dinning_name)
    dinnings = dinnings.fetchall()
    return render_template('show_one_dinning.html', dinnings=dinnings)

#  housing part======================================================

@app.route('/housing')
def show_housing():
    housings = g.db.execute('SELECT * FROM housing')
    housings = housings.fetchall()
    #pdb.set_trace()
    return render_template('show_housings.html', housings=housings)

@app.route('/addhousing', methods=['POST'])
def add_housing():
    g.db.execute('insert into housing (location, price) values (?, ?)',
                 [request.form['name'], request.form['research']])
    g.db.commit()
    flash('New housing was successfully added')
    return redirect('/housing')

@app.route('/deletehousing', methods=['POST'])
def delete_housing():
    a=request.form.getlist("delete")
    for i in a:
        g.db.execute('delete from housing where housing.location = ?',[i])
    g.db.commit()
    flash('successfully deleted')
    return redirect(url_for('show_housing'))

@app.route('/housing/<housing_name>')
def show_housing_name(housing_name):
    housings = g.db.execute("SELECT * FROM housing where housing.location='%s'" % housing_name)
    housings = housings.fetchall()
    return render_template('show_one_housing.html', housings=housings)


if __name__ == '__main__':
    app.run(debug=True)