import sqlite3 as sql;
import os;
import re;
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

def insertContestData( cursor ) :
	contestsPath = os.getcwd() + '/static/contests/';
	contestFolders = os.listdir( contestsPath );
	contestFolders.sort();

	for contestFolder in contestFolders :
		contestPath = contestsPath + contestFolder;

		with open( contestPath + '/contest_info', 'r' ) as contestFile :
			contestInfo = contestFile.read().splitlines();

			edition = contestFolder.split( '_' )[ 1 ];
			title = contestInfo[ 0 ];
			fecha = contestInfo[ 1 ];
			public = int( contestInfo[ 2 ] );
			link = contestInfo[ 3 ];
			synopsis = contestInfo[ 4 ];
			winner = contestInfo[ 5 ];

			queryContest = "INSERT INTO contests (edition,title,fecha,public,link,synopsis,winner) VALUES (?,?,?,?,?,?,?)";
			tupleContest = (edition,title,fecha,public,link,synopsis,winner);
			cursor.execute( queryContest, tupleContest );

			problemInfo = contestInfo[ 7 : ];

			solutionsPath = contestPath + '/solutions';
			solutionLetters = os.listdir( solutionsPath );
			solutionLetters.sort();

			for i in range( len( solutionLetters ) ) :
				solutionTxt = solutionLetters[ i ];

				with open( solutionsPath + '/' + solutionTxt, "r" ) as solutionFile : 
					letter = solutionTxt.split( '.' )[ 0 ];
					title = problemInfo[ 3*i ];
					judgeId = problemInfo[ 3*i + 1 ];
					link = problemInfo[ 3*i + 2 ];
					solution = solutionFile.read();

					queryProblem = "INSERT INTO problems (letter,edition,title,judgeId,link,solution) VALUES (?,?,?,?,?,?)";
					tupleProblem = (letter,edition,title,judgeId,link,solution);
					cursor.execute( queryProblem, tupleProblem );

def insertAnnouncementData( cursor ) :
	announcementsPath = os.getcwd() + '/static/announcements/';
	announcementNames = os.listdir( announcementsPath );
	announcementNames.sort();

	for announcementName in announcementNames :
		announcementPath = announcementsPath + announcementName;

		with open( announcementPath, 'r' ) as announcementFile :
			announcementInfo = announcementFile.read().splitlines();

			edition = int( re.split( r'[_.]+', announcementName )[ 1 ] );
			title = announcementInfo[ 0 ];
			fecha = announcementInfo[ 1 ];
			author = announcementInfo[ 2 ];
			public = int( announcementInfo[ 3 ] );
			post = "\n".join( announcementInfo[ 4 : ] );

			queryAnnouncement = "INSERT INTO announcements (edition,title,fecha,author,public,post) VALUES (?,?,?,?,?,?)";
			tupleAnnouncement = (edition,title,fecha,author,public,post);
			cursor.execute( queryAnnouncement, tupleAnnouncement );

def insertData( connection ) :
	cursor = connection.cursor();

	insertContestData( cursor );
	connection.commit();

	insertAnnouncementData( cursor );
	connection.commit();

	print "INSERTED DATA!";

def createDatabase( databaseName ) :
	if isSQLite3( databaseName ) :
		return False;

	connection = sql.connect( databaseName );

	print( "Opened database!" );

	connection.execute( "CREATE TABLE announcements (edition INTEGER, title TEXT, fecha TEXT, author TEXT, public INTEGER, post TEXT)" );
	connection.execute( "CREATE TABLE contests (edition INTEGER, title TEXT, fecha TEXT, public INTEGER, link TEXT, synopsis TEXT, winner TEXT)" );
	connection.execute( "CREATE TABLE problems (letter TEXT, edition INTEGER, title TEXT, judgeId TEXT, link TEXT, solution TEXT)" );

	insertData( connection );
	# getDummyData( connection );