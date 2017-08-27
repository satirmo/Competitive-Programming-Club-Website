from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_mail import Message, Mail;
from flask_bootstrap import Bootstrap;
import os;
import sqlite3 as sql;
import databaseManagement;
import utilityFunctions;

app = Flask( __name__ );

@app.route( "/", methods = [ "GET" ] )
def index() :
	connection = sql.connect( "database.db" );
	connection.row_factory = sql.Row;

	cursor = connection.cursor();

	cursor.execute( "SELECT * FROM announcements" );
	tmpAnnouncements = sorted( cursor.fetchall(), key = lambda tup: tup[2], reverse = True );

	announcements = [];

	for tmpAnnouncement in tmpAnnouncements :
		if tmpAnnouncement[3] == 1 :
			announcement = dict( tmpAnnouncement );
			announcement['fecha'] = utilityFunctions.convertToTextDate( announcement['fecha'] );

			announcements.append( announcement );

		if len( announcements ) == 5 :
			break;

	return render_template( "index.html", announcements = announcements );

@app.route( "/layout/", methods = [ "GET" ] )
def layout() :
	return render_template( "layout.html" );

@app.route( "/contests/", methods = [ "GET" ] )
def contests() :
	connection = sql.connect( "database.db" );
	connection.row_factory = sql.Row;

	cursor = connection.cursor();

	cursor.execute( "SELECT edition,title,fecha,public,winner FROM contests" );
	tmpContests = sorted( cursor.fetchall(), key = lambda tup: tup[2], reverse = True );

	contests = [];

	for tmpContest in tmpContests :
		if tmpContest[ 3 ] == 1 :
			contest = dict();

			contest['title'] = tmpContest['title'];
			contest['fecha'] = tmpContest['fecha'];			
			contest['winner'] = tmpContest['winner'];
			contest['pageURL'] = '/contest/' + str( tmpContest['edition'] );

			contests.append( contest );

	return render_template( "contests.html", contests = contests );

# CONSIDER REWRITING THIS WITH UTILITY FUNCTIONS
@app.route( "/contest/<int:edition>/", methods = [ "GET" ] )
def contest( edition ) :
	connection = sql.connect( "database.db" );
	connection.row_factory = sql.Row;

	cursor = connection.cursor();

	# generate contest informtion

	cursor.execute( "SELECT * FROM contests WHERE edition = ?", (edition,) );
	contests = cursor.fetchall();

	if len( contests ) < 1 :
		return "calm your horses! this contest hasn't even occurred yet!";

	elif len( contests ) > 1 :
		return "you messed up your indexing, buddy.";

	contest = dict( contests[0] );

	if contest['public'] == 0 :
		return "this isn't public yet. quit snoopin'!"

	# generate problem information

	cursor.execute( "SELECT * FROM problems WHERE edition = ?", (edition,) );
	tmpProblems = [ dict( problem ) for problem in cursor.fetchall() ];

	codePath = 'contests/contest_' + str( contest[ 'edition' ] ) + '/codes/';
	imagePath = 'contests/contest_' + str( contest[ 'edition' ] ) + '/images/';
	
	solutionsLink = url_for( 'static', filename = codePath + 'solutions.zip' );
	scoreboardLink = url_for( 'static', filename = imagePath + 'scoreboard.png' );

	contest['solutionsLink'] = solutionsLink;
	contest['scoreboardLink'] = scoreboardLink;
	contest['fecha'] = utilityFunctions.convertToTextDate( contest['fecha'] );

	absPath = os.getcwd() + '/static/' + codePath;
	dirFiles = os.listdir( absPath );

	problems = [];

	for problem in tmpProblems :
		tabClass = "nav-link" + ( " active" if problem['letter'] == "A" else "" );
		paneClass = "tab-pane" + ( " active" if problem['letter'] == "A" else "" );
		
		problem['tabClass'] = tabClass;
		problem['paneClass'] = paneClass;

		solutionLinks = [];

		for dirFile in dirFiles :
			if problem['letter'] in dirFile :
				solutionLink = ( '/static/' + codePath + dirFile, dirFile.split( "/" )[-1] );
				solutionLinks.append( solutionLink );

		problem['solutionLinks'] = sorted( solutionLinks );
		problems.append( problem );

	# check next and previous contest
	cursor.execute( "SELECT public FROM contests WHERE edition = ?", (edition-1,) );
	previousContest = cursor.fetchall();

	if len( previousContest ) == 1 and previousContest[ 0 ][ 0 ] == 1 :
		contest['hasPreviousContest'] = True;
		contest['linkPreviousContest'] = '/contest/' + str( edition-1 );

	else :
		contest['hasPreviousContest'] = False;

	cursor.execute( "SELECT public FROM contests WHERE edition = ?", (edition+1,) );
	nextContest = cursor.fetchall();

	if len( nextContest ) == 1 and nextContest[ 0 ][ 0 ] == 1 :
		contest['hasNextContest'] = True;
		contest['linkNextContest'] = '/contest/' + str( edition+1 );

	else :
		contest['hasNextContest'] = False;

	return render_template( 'contest.html', contest = contest, problems = problems );

# THIS NEEDS TO BE TIDIED UP
@app.route( "/contact/", methods = [ "GET", "POST" ] )
def contact() :
	if request.method == "POST" :
		# ADD SERVER SIDE VALIDATION
		verdict = utilityFunctions.validateContactForm( request.form );
		
		if verdict != True :
			return "failure"
		
		firstName = request.form['firstName'];
		lastName = request.form['lastName'];
		email = request.form['email'];
		subject = request.form['subject'];
		message = request.form['message']; 

		msg = Message(subject, sender = "tshurehog@gmail.com", recipients=['tshurehog@gmail.com'])
		msg.body = """
		From: %s <%s>
		%s
		""" % ( firstName + " " + lastName, email, message)
		mail.send(msg);

		return render_template( "contactForm.html", messageSent = "sucess" );

	elif request.method == "GET" :
		return render_template( "contactForm.html" );

if __name__ == '__main__':
	databaseManagement.createDatabase();

	mail = Mail()

	app.secret_key = 'super secret development key'
	app.config["MAIL_SERVER"] = "smtp.gmail.com"
	app.config["MAIL_PORT"] = 465
	app.config["MAIL_USE_SSL"] = True
	app.config['MAIL_USE_TLS'] = False
	app.config["MAIL_USERNAME"] = 'tshurehog@gmail.com'
	app.config["MAIL_PASSWORD"] = 'thisistotallymypassword'
	mail.init_app(app)

	app.run(debug = True, port = 5001 )
