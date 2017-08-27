import re;

def convertToTextDate( fecha ) :
	year, tmonth, day = fecha.split( '-' );

	months = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
	month = months[ int( tmonth ) - 1 ];

	return month + " " + day + ", " + year;

def validateContactForm( form ) :
	#UPDATE CONTACT FORM VALIDATION
	firstName = form['firstName'];
	lastName = form['lastName'];
	email = form['email'];
	subject = form['subject'];
	message = form['message'];

	return True;
	return validateEmail( email );

def validateEmail( email ) :
	pattern = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?";
	match = re.match( "^" + pattern + "+$", email );

	return len( match ) != 0;