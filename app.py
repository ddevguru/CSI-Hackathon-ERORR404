from aifc import Error
from django import db
from flask import Flask, jsonify, render_template, redirect, send_from_directory, url_for, session, flash,request
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'studentmentor'
app.config['SECRET_KEY'] = 'supersecretkey'

app.config['UPLOAD_FOLDER'] = 'uploads'
mysql = MySQL(app)

@app.route('/')
def landing():
    return render_template('landing.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", [email])
        existing_user = cur.fetchone()

        if existing_user:
            flash("Email already registered, please log in.", "warning")
            return redirect(url_for('signup'))

        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                    (name, email, hashed_password, role))
        mysql.connection.commit()
        cur.close()

        flash(f"Account created successfully for {name}!", "success")
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND role=%s", (email, role))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password): 
            session['loggedin'] = True
            session['id'] = user[0]
            session['name'] = user[1]
            session['role'] = user[4]  

            flash(f"Welcome {user[1]}! Logged in as {user[4].capitalize()}.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Check your credentials.", "danger")

    return render_template('login.html')





@app.route('/approve/<int:user_id>', methods=['GET'])
def approve(user_id):
    if 'loggedin' in session and session['role'] == 'admin':
        cur = mysql.connection.cursor()
        
        cur.execute("UPDATE users SET approved = TRUE WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cur.close()

        flash('User approved successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))
    
    
    
    
    
    
@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    role = session['role']

    if role == 'student':
        cur = mysql.connection.cursor()
        
        # Fetch list of mentors
        cur.execute("SELECT * FROM users WHERE role='mentor'")
        mentors = cur.fetchall()

        # Fetch study materials
        cur.execute("SELECT * FROM study_materials")
        study_materials = cur.fetchall()

        # Fetch courses
        cur.execute("SELECT * FROM courses")
        courses = cur.fetchall()
        
           # Fetch the student's join requests status
        cur.execute("""
            SELECT c.id, c.course_name, COALESCE(cr.status, 'pending') AS status
            FROM courses c
            LEFT JOIN course_requests cr
            ON c.id = cr.course_id AND cr.student_id = %s
        """, [session['id']])
        course_requests = cur.fetchall()

        # Fetch the student's join requests status
        cur.execute("""
            SELECT u.id, u.name, u.profile_photo, COALESCE(jr.status, 'pending') AS status
            FROM users u
            LEFT JOIN join_requests jr
            ON u.id = jr.mentor_id AND jr.student_id = %s
            WHERE u.role = 'mentor'
        """, [session['id']])
        mentor_requests = cur.fetchall()

        cur.close()

        # Print mentor_requests to verify the data
        print("Mentor Requests:", mentor_requests)

        
        return render_template('studentdashboard.html', mentors=mentors, mentor_requests=mentor_requests, study_materials=study_materials, courses=courses,course_requests=course_requests)
    elif role == 'mentor':

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users INNER JOIN mentor_students ON users.id = mentor_students.student_id WHERE mentor_students.mentor_id=%s", [session['id']])
        mentees = cur.fetchall()

        cur.execute("SELECT * FROM courses WHERE mentor_id=%s", [session['id']])
        courses = cur.fetchall()
      
        
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT jr.id, u.name, jr.reason 
            FROM join_requests jr 
            JOIN users u ON jr.student_id = u.id 
            WHERE jr.status = 'pending' AND jr.mentor_id = %s
        """, (session['id'],))
        pending_requests = cur.fetchall()

       
        cur.execute("""
            SELECT jr.id, u.name, jr.reason 
            FROM join_requests jr 
            JOIN users u ON jr.student_id = u.id 
            WHERE jr.status = 'approved' AND jr.mentor_id = %s
        """, (session['id'],))
        approved_requests = cur.fetchall()
        cur.close()

        return render_template('mentordashboard.html', mentees=mentees, courses=courses,  pending_requests=pending_requests,approved_requests=approved_requests)
    

    elif role == 'admin':
   
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE role='mentor' OR role='student'")
        accounts = cur.fetchall()

        cur.execute("SELECT * FROM courses")
        courses = cur.fetchall()
        
        cur.execute("""
            SELECT cr.id, c.course_name, s.name, cr.status
            FROM course_requests cr
            JOIN courses c ON cr.course_id = c.id
            JOIN users s ON cr.student_id = s.id WHERE role ='student'
        """)
        course_requests = cur.fetchall()
    

        cur.close()

        return render_template('admindashboard.html', accounts=accounts, courses=courses,course_requests=course_requests)

    return redirect(url_for('login'))



@app.route('/studentmentorlist')
def studentmentorlist():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    role = session['role']

    if role == 'student':
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM users WHERE role='mentor'")
        mentors = cur.fetchall()
        cur.close()
    return render_template('studentmentorlist.html', mentors=mentors)

    

@app.route('/studentmentorsrequest')
def studentmentorsrequest():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    role = session['role']

    if role == 'student':
        cur = mysql.connection.cursor()
        
      
        cur.execute("""
            SELECT u.id, u.name, u.profile_photo, COALESCE(jr.status, 'pending') AS status
            FROM users u
            LEFT JOIN join_requests jr
            ON u.id = jr.mentor_id AND jr.student_id = %s
            WHERE u.role = 'mentor'
        """, [session['id']])
        mentor_requests = cur.fetchall()

        cur.close()
    return render_template('studentmentorsrequest.html', mentor_requests=mentor_requests)
    
    
    
@app.route('/studymateriallist')
def studymateriallist():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    role = session['role']

    if role == 'student':
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM study_materials")
        study_materials = cur.fetchall()

        cur.close()
    return render_template('studymateriallist.html', study_materials=study_materials)
    
    
    
@app.route('/studentcourselist')
def studentcourselist():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    role = session['role']

    if role == 'student':
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM courses")
        courses = cur.fetchall()
        

        cur.close()
    return render_template('studentcourselist.html', courses=courses)
    

@app.route('/studentcourseaprovelist')
def studentcourseaprovelist():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    role = session['role']

    if role == 'student':
        cur = mysql.connection.cursor()
        
        cur.execute("""
            SELECT c.id, c.course_name, COALESCE(cr.status, 'pending') AS status
            FROM courses c
            LEFT JOIN course_requests cr
            ON c.id = cr.course_id AND cr.student_id = %s
        """, [session['id']])
        course_requests = cur.fetchall()
        

        cur.close()
    return render_template('studentcourseaprovelist.html', course_requests=course_requests)


# @app.route('/mentordashboard')
# def mentordashboard():
#     cur = mysql.connection.cursor()

#     cur.execute("""
#             SELECT jr.id, u.name, jr.reason 
#             FROM join_requests jr 
#             JOIN users u ON jr.student_id = u.id 
#             WHERE jr.status = 'approved' AND jr.mentor_id = %s
#         """, (session['id'],))
#     approved_requests = cur.fetchall()
#     cur.close()
#     return render_template('mentordashboard.html',approved_requests=approved_requests)


@app.route('/uploadcourseadmin', methods=['GET', 'POST'])
def uploadcourseadmin():

        
    return render_template('uploadcourseadmin.html')

@app.route('/aproveacc', methods=['GET', 'POST'])
def aproveacc():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE role='mentor' OR role='student'")
    accounts = cur.fetchall()
    cur.close()
    return render_template('aproveacc.html', accounts=accounts)
    

@app.route('/updatecourseadmin', methods=['GET', 'POST'])
def updatecourseadmin():

        
    return render_template('updatecourseadmin.html')
    

@app.route('/update_course_admin', methods=['GET', 'POST'])
def update_course_admin():
    if 'loggedin' in session and session['role'] == 'admin':
        cur = mysql.connection.cursor()

        if request.method == 'POST':
            course_id = request.form.get('course_id')
            course_name = request.form.get('course_name')
            course_description = request.form.get('course_description')
            course_duration = request.form.get('course_duration')

            if not course_id:
                flash('Please select a course to update.', 'danger')
            elif not (course_name and course_description and course_duration):
                flash('All fields are required.', 'danger')
            else:
              
                cur.execute("""
                    UPDATE courses
                    SET course_name = %s, course_description = %s, course_duration = %s
                    WHERE id = %s
                """, (course_name, course_description, course_duration, course_id))
                mysql.connection.commit()
                flash('Course updated successfully!', 'success')


        cur.execute("SELECT * FROM courses")
        courses = cur.fetchall()
        cur.close()

        return render_template('update_course_admin.html', courses=courses)
    else:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    
    
    

@app.route('/update_course', methods=['GET', 'POST'])
def update_course():
    if 'loggedin' in session and session['role'] == 'mentor':
        mentor_id = session['id']  # Assuming mentor's ID is stored in the session
        cur = mysql.connection.cursor()

        if request.method == 'POST':
            # Fetch course data from form
            course_id = request.form['course_id']
            course_name = request.form['course_name']
            course_description = request.form['course_description']
            course_duration = request.form['course_duration']

            # Update the course details in the database (only for this mentor)
            cur.execute("""
                UPDATE courses
                SET course_name = %s, course_description = %s, course_duration = %s
                WHERE id = %s AND mentor_id = %s
            """, (course_name, course_description, course_duration, course_id, mentor_id))
            mysql.connection.commit()
            flash('Course updated successfully!', 'success')

        # Fetch courses associated with this mentor
        cur.execute("SELECT * FROM courses WHERE mentor_id = %s", (mentor_id,))
        courses = cur.fetchall()
        cur.close()

        return render_template('update_course.html', courses=courses)
    else:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))


@app.route('/upload_study_material', methods=['POST'])
def upload_study_material():
    if 'study_material' not in request.files:
        return redirect(url_for('admin_dashboard'))

    file = request.files['study_material']
    title = request.form['material_title']
    course_id = request.form.get('course_id')  # Optional field

    if file and title:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Generate the file URL
        file_url = url_for('uploaded_file', filename=filename)

        cursor = mysql.connection.cursor()

        if course_id:
            query = 'INSERT INTO study_materials (material_title, material_link, course_id) VALUES (%s, %s, %s)'
            values = (title, file_url, course_id)
        else:
            query = 'INSERT INTO study_materials (material_title, material_link) VALUES (%s, %s)'
            values = (title, file_url)

        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()

    return redirect(url_for('dashboard'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
   return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/update_mentor_profile')
def update_mentor_profile():

    return render_template('update_mentor_profile.html')


@app.route('/mentorpenreqli')
def mentorpenreqli():
    cur = mysql.connection.cursor()
    cur.execute("""
            SELECT jr.id, u.name, jr.reason 
            FROM join_requests jr 
            JOIN users u ON jr.student_id = u.id 
            WHERE jr.status = 'pending' AND jr.mentor_id = %s
        """, (session['id'],))
    pending_requests = cur.fetchall()
    return render_template('mentorpenreqli.html',pending_requests=pending_requests)

@app.route('/aprovestudentli')
def aprovestudentli():
    cur=mysql.connection.cursor()
    cur.execute("""
            SELECT jr.id, u.name, jr.reason 
            FROM join_requests jr 
            JOIN users u ON jr.student_id = u.id 
            WHERE jr.status = 'approved' AND jr.mentor_id = %s
        """, (session['id'],))
    approved_requests = cur.fetchall()
    cur.close()
    return render_template('aprovestudentli.html',approved_requests=approved_requests)



@app.route('/update_profile', methods=['POST'])
def update_profile():
    if session.get('role') != 'mentor':
        return "Access denied", 403

    name = request.form['name']
    bio = request.form.get('bio')
   

    profile_photo = request.files['profile_photo']
    profile_photo_filename = None
    if profile_photo:
        filename = secure_filename(profile_photo.filename)
        profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        profile_photo_filename = filename
        
        number = request.form.get('number')
    try:
        cur = mysql.connection.cursor()
        query = """
            UPDATE users 
            SET name = %s, bio = %s, profile_photo = %s, number=  %s
            WHERE id = %s AND role = 'mentor'
        """
        cur.execute(query, (name, bio,profile_photo_filename,number, session['id']))
        mysql.connection.commit()
        cur.close()

        session['bio'] = bio
        session['profile_photo'] = profile_photo_filename

        return redirect(url_for('dashboard'))

    except mysql.connect.Error as err:
        print(f"Error: {err}")
        return "Database error", 500
        




@app.route('/request_join', methods=['POST'])
def request_join():
    mentor_id = request.form['mentor_id']
    reason = request.form['reason']
    student_id = session['id']  

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO join_requests (student_id, mentor_id, reason, status) VALUES (%s, %s, %s, %s)',
                   (student_id, mentor_id, reason, 'pending'))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboard'))


@app.route('/approve_request/<int:request_id>', methods=['GET', 'POST'])
def approve_request(request_id):
    if 'id' in session and session['role'] == 'mentor':
        if request.method == 'POST':
        
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE join_requests 
                SET status = 'approved' 
                WHERE id = %s AND mentor_id = %s
            """, (request_id, session['id']))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('dashboard'))
        
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT jr.id, u.name, jr.reason 
            FROM join_requests jr 
            JOIN users u ON jr.student_id = u.id 
            WHERE jr.id = %s AND jr.mentor_id = %s
        """, (request_id, session['id']))
        join_request = cur.fetchone()
        cur.close()

        if not join_request:
            return "Request not found", 404

        return render_template('approve_request.html', join_request=join_request)
    else:
        return redirect(url_for('login'))


@app.route('/request_course_join', methods=['POST'])
def request_course_join():
    course_id = request.form['course_id']
    student_id = session['id']  

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO course_requests (student_id, course_id) VALUES (%s, %s)',
                   (student_id, course_id))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboard'))


@app.route('/approve_course_request/<int:request_id>', methods=['POST'])
def approve_course_request(request_id):
    try:
        cur = mysql.connection.cursor()
        # Check if the request ID exists
        cur.execute("SELECT id FROM course_requests WHERE id = %s", [request_id])
        request_exists = cur.fetchone()
        
        if request_exists:
            cur.execute("UPDATE course_requests SET status = 'approved' WHERE id = %s", [request_id])
            mysql.connection.commit()
            flash('Request approved successfully!', 'success')
        else:
            flash('Request not found.', 'danger')
        
        cur.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred while approving the request.', 'danger')
    
    return redirect(url_for('dashboard'))




    data = request.json
    sender_id = session.get('user_id')
    if not sender_id:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 401

    receiver_id = data.get('receiver_id')
    message = data.get('message')

    try:
        cursor = mysql.get_db().cursor()
        cursor.execute(
            "INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)",
            (sender_id, receiver_id, message)
        )
        mysql.get_db().commit()
        cursor.close()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
