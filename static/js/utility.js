$(document).ready(function(){
	$( ".problemTab.A" ).toggleClass( "active" );
	$( ".problemContent.A" ).toggle();

	$( ".problemTab" ).click(function(){
		var oldTabLetter = "";
		var newTabLetter = "";

		for( var i = 0; i < 26; i++ ){
			var asciiValue = i + "A".charCodeAt( 0 );
			var classCandidate = String.fromCharCode( asciiValue );

			if( $( ".problemTab.active" ).hasClass( classCandidate ) ){
				oldTabLetter = classCandidate;
			}

			if( $( this ).hasClass( classCandidate ) ){
				newTabLetter = classCandidate;
			}
		}

		$( ".problemTab.active." + oldTabLetter ).toggleClass( "active" );
		$( ".problemTab." + newTabLetter ).toggleClass( "active" );

		$( ".problemContent." + oldTabLetter ).toggle();
		$( ".problemContent." + newTabLetter ).toggle();
	});
});

function validateContactForm(){
	var firstName = document.forms["contactForm"]["firstName"].value;
	var lastName = document.forms["contactForm"]["lastName"].value;
	var email = document.forms["contactForm"]["email"].value;
	var subject = document.forms["contactForm"]["subject"].value;
	var message = document.forms["contactForm"]["message"].value;

	if( ( ! validName( firstName ) ) || ( ! validName( lastName ) ) ){
		return false;
	}

	if( ! validateEmail( email ) ){
		return false;
	}

	if( ! validSubject( subject ) ){
		return false;
	}

	if( ! validMessage( message ) ){
		return false;
	}

	return true;
}

function validName( name ){
	return name;
}

function validSubject( subject ){
	return subject !== "";
}

function validateEmail( email ){
	var pattern = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?";
	var emailRegex = new RegExp( pattern );

	return emailRegex.test( email );
}

function validMessage( message ){
	return message !== "";
}