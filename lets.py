from flask import Flask,render_template,request,flash,redirect,url_for
from flask_wtf import Form 
from wtforms import TextField,PasswordField, SubmitField,IntegerField
from wtforms import validators, ValidationError
import MySQLdb
app=Flask(__name__)
app.secret_key = 'development key'


conn=MySQLdb.connect(host="localhost",user="root",
                     passwd="ayush1990",db="FORWEB")
c=conn.cursor()

class info(Form):
	username=TextField("Username",[validators.Required("Please enter your username.")])
	password = PasswordField('New Password', [ validators.DataRequired("please enter password"),validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	age=IntegerField("age",[validators.Required("Please enter your age.")])	
	submit=SubmitField("signup")	

class info2(Form):
	username=TextField("Username",[validators.Required("Please enter your username.")])
	password = PasswordField('New Password', [ validators.DataRequired("please enter password")])	
	submit=SubmitField("login")


@app.route('/')
def main():
	return render_template('main.html')
@app.route('/signin',methods = ['GET', 'POST'])
def signin():
	form=info()
	if request.method=='POST':
		if form.validate_on_submit()==False:
			flash ("please enter all the fields")
			return render_template('sign.html', form = form)
		else:
			Username=request.form['username']
			Password =request.form['password']
			Age=request.form['age']	
			x=c.execute("SELECT * FROM INFORMATION WHERE USERNAME = (%s);",(Username,))
			if int(x) > 0:
				return render_template('login.html', form = form)
			else:
				c.execute("INSERT INTO INFORMATION (USERNAME,PASSWORD,AGE)VALUES (%s,%s,%s);",(Username,Password,Age))
				conn.commit()				
				return render_template('sucess.html',name=Username)
	else:
		return render_template('sign.html', form = form)
	
@app.route('/login',methods = ['GET', 'POST'])
def login():
	form=info2()
	if request.method=='POST':
		if form.validate_on_submit()==False:
			flash ("please enter all the fields")			
			return render_template('login.html', form = form)
		else:
			Username=form.username.data
			Password = form.password.data
			x=c.execute("SELECT COUNT(*)  FROM INFORMATION WHERE USERNAME IN (%s) AND PASSWORD IN (%s)",(Username,Password))
			if(int(x)==1 ): 
                        	return render_template('sucesslogin.html',name=Username)
			else:
				return render_template('login.html', form = form)
	else:		
		return render_template('login.html', form = form)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__=='__main__':
	app.run(debug=True)
