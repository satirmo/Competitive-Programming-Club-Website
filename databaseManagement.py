import sqlite3 as sql;
from os.path import isfile, getsize;

def isSQLite3( fileName ):
	if not isfile( fileName ):
		return False;

	if getsize( fileName ) < 100: # SQLite database file header is 100 bytes
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

	print "INSERTED DUMMMY DATA!";

def createDatabase() :
	databaseName = "database.db"

	if isSQLite3( databaseName ) :
		return False;

	connection = sql.connect( databaseName );

	print( "Opened database!" );

	connection.execute( "CREATE TABLE contests (edition INTEGER, title TEXT, fecha TEXT, public INTEGER, link TEXT, synopsis TEXT, winner TEXT)" );
	connection.execute( "CREATE TABLE problems (letter TEXT, edition INTEGER, title TEXT, judgeId TEXT, link TEXT, solution TEXT)" );

	insertDummyData( connection );
	# getDummyData( connection );