import sqlite3 as sql;
from os.path import isfile, getsize;

def isSQLite3( fileName ):
	if not isfile( fileName ):
		return False;

	# SQLite database file header is 100 bytes
	if getsize( fileName ) < 100:
		return False;

	with open( fileName, "rb" ) as fd:
		header = fd.read( 100 );

	return header[:16] == "SQLite format 3\x00";

def getDummyData( connection ) :
	cursor = connection.cursor();

	queryContest = "SELECT * FROM contests WHERE edition = 1";
	rows = cursor.execute( queryContest );

	for row in rows :
		print( row );

	queryProblem = "SELECT * FROM problems WHERE edition = 1";
	rows = cursor.execute( queryProblem );

	for row in rows :
		print( row );

def insertDummyData( connection ) :
	cursor = connection.cursor();

	contestEntries = 10;

	winners = [ "", "Spongebob", "Mr. Incredible", "Totoro", "Freddie Mercury", "Alain de Botton", "Harry Potter", "Pikachu", "Flea", "Paulo Coelho" ];

	for j in range( 1, contestEntries ) :
		edition = j;
		title = "Practice Contest " + str( j );
		fecha = "2017-08-" + str( 10 + j );
		public = 1 if j < contestEntries - 1 else 0;
		link = "https://vjudge.net/contest/172746#overview"
		synopsis = "Insert synopsis of contest " + str( j ) + " here.";
		winner = winners[ j ];

		queryContest = "INSERT INTO contests (edition,title,fecha,public,link,synopsis,winner) VALUES (?,?,?,?,?,?,?)";
		tupleContest = (edition,title,fecha,public,link,synopsis,winner);
		cursor.execute( queryContest, tupleContest );
		connection.commit();

		for i in range( 7 ) :
			letter = chr( ord( "A" ) + i );
			edition = j;
			title = "The 3n + " + str( 1 + i ) + " problem";
			judgeId = "UVa 100";
			link = "https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=36";
			solution = "This is the solution for problem " + letter + ".";

			queryProblem = "INSERT INTO problems (letter,edition,title,judgeId,link,solution) VALUES (?,?,?,?,?,?)";
			tupleProblem = (letter,edition,title,judgeId,link,solution)
			cursor.execute( queryProblem, tupleProblem );
			connection.commit();

	######################################
	######################################
	######################################

	edition = 0;
	title = "Are you looking for a challenge?";
	fecha = "2017-09-02";
	public = 1;
	post = "<p>If so, you should join our club!</p>\
			<p>Now, you may be thinking, 'Why is this guy telling me what I should?'. Hear me out. Our club focuses on the problem-solving aspect of computer programming, making our club attractive for both programmers and non-programmers alike.</p>\
			<ul>\
				<li>\
					<strong>Non-programmers.</strong> Have you ever given anybody directions to the their classroom? Assuming you have, you actually gave that person an algorithm! How easy was that? I won't lie; there are far more difficult problems out there, but you have to start somewhere. In addition to solving some challenging problems, you will learn how to translate your ideas to code! Trust me; the coding part isn't as bad as it sounds if you're algorithm designing ability is on point.\
				</li>\
				<li>\
					<strong>Programmers.</strong> I expect that you will agree with me when I say that algorithm design is an essential part of the programming process (unless if you want to stuck in infinite debugging loop, of course). Along with improving you're algorithm design skills, you will find that you're coding and debugging speed will increase drastically if you attend our meetings consistently. Moreover, you'll become much more familiar with the language that you choose to use (which will probably be C++ or Python).\
				</li>\
			</ul>\
			<p>It also stands to mention that our club participates in external contests, such as the ACM ICPC and the CCSCNE, during each semester. This means that you will also have the opportunity to interact and compete with some of the brightest students in our region.</p>\
			<p>I have promised a fair amount of benefits of joining our club. In order to obtain these benefits, we will be holding a weekly crash course on a particular algorithm or heuristic to get our members up-to-speed. In addition, we will be a hosting weekly contests so that our members can track their improvement.</p>\
			<p>If I have managed to pique your interest (hurray!) or if you have any questions, do not hesitate to send us a message!</p>\
			<p>Take care,<br>Tomas</p>";

	queryAnnouncement = "INSERT INTO announcements (edition,title,fecha,public,post) VALUES (?,?,?,?,?)";
	tupleAnnouncement = (edition,title,fecha,public,post);
	cursor.execute( queryAnnouncement, tupleAnnouncement );
	connection.commit();

	print "INSERTED DUMMMY DATA!";

def createDatabase( databaseName ) :
	if isSQLite3( databaseName ) :
		return False;

	connection = sql.connect( databaseName );

	print( "Opened database!" );

	connection.execute( "CREATE TABLE announcements (edition INTEGER, title TEXT, fecha TEXT, public INTEGER, post TEXT)" );
	connection.execute( "CREATE TABLE contests (edition INTEGER, title TEXT, fecha TEXT, public INTEGER, link TEXT, synopsis TEXT, winner TEXT)" );
	connection.execute( "CREATE TABLE problems (letter TEXT, edition INTEGER, title TEXT, judgeId TEXT, link TEXT, solution TEXT)" );

	insertDummyData( connection );
	# getDummyData( connection );