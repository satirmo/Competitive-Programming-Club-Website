import re;

def convertToTextDate( fecha ) :
	year, tmonth, day = fecha.split( '-' );

	months = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
	month = months[ int( tmonth ) - 1 ];

	return month + " " + day + ", " + year;

def validateContactForm( form, captcha ) :
	if inputExists( form['firstName'] ) == False :
		return "First name required.";

	if inputExists( form['lastName'] ) == False :
		return "Last name required.";

	if validateEmail( form['email'] ) == False :
		return "Email required.";

	if inputExists( form['subject'] ) == False :
		return "Subject required.";

	if inputExists( form['message'] ) == False :
		return "Message required.";

	if captcha == False :
		return "Captcha required.";

	return "success"

def inputExists( input ) :
	input = str( input );

	for c in input :
		if c != ' ' :
			return True;

	return False;

def validateEmail( email ) :
	pattern = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?";
	return re.match( pattern, email );