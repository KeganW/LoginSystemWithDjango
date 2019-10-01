from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.models import User, auth


# Create your views here.

#Method that sets the home page as create_user.html.j2.
def home(request):

	return render(request, 'create_user.html.j2')

#Method that creates a user and append it to a database; basic error 
#checking included
def create(request):

	#used to set the error message
	local_error = 0
	#used to display to the user upon failure
	error_message = ""
	#used to display to the user upon success
	success_message = "Account has successfully been created."

	#checks if the form is submitted
	if request.method == 'POST':
		#obtain user input
		first = request.POST['first']
		last = request.POST['last']
		email = request.POST['email']
		password = request.POST['password']
		verify_password = request.POST['passwordVer']
		username = request.POST['username']

		#check for empty input, valid email, and matching passwords
		if(val_length(email, password, verify_password, username)):

			local_error = local_error  + 1
			
			if (val_email(email)):

				local_error = local_error + 1
				
				if (password == verify_password):

					local_error = local_error + 1
				
					#checks if the username exists in the database		
					if (not User.objects.filter(username=username).exists()):
						
						local_error = local_error + 1

						#checks if the email exists in the database
						if (not User.objects.filter(email=email).exists()):

							local_error = local_error + 1	

							#append to the database using ORM
							user = User.objects.create_user(username=username, 
										password=password, email=email, 
											first_name=first, 
												last_name=last)
							user.save()
							return render(request, 'create_user.html.j2', 
										{'success': success_message})

	#display error on page upon failure, redirect to same page
	error_message = switch_error(local_error)
	return render(request, 'create_user.html.j2',{'error': error_message})

#Method that checks for the validity of the email.
def val_email(email):
	validator = EmailValidator();
	try:
		validator(email)
	except ValidationError:
		return False

	return True


#Method that checks for valid input lengths.
def val_length(email, password, verify_password, username):

	return len(email) > 0 and len(password) > 0 and len(verify_password) > 0 and len(username) > 0

#Method that sets the error message depending on the first detected error.
def switch_error(local_error):

	switcher = {
		0:"Account NOT created due to one or more empty inputs.",
		1:"Account NOT created due to invalid email.",
		2:"Account NOT created since passwords did not match.",
		3:"Account NOT created since username already exists.",
		4:"Account NOT created since email already exists."
	}

	return switcher.get(local_error, "Account NOT created due to error.")

#Method that logins the user.
def login(request):

	#used to display the error upon failure
	error = ""

	if request.method == 'POST':
		
		username = request.POST['userid']
		password = request.POST['userpassword']
		user = auth.authenticate(username=username,password=password)

		#login the user if the entry exists in the database
		if user is not None:
			auth.login(request, user)
			return render(request, 'create_user.html.j2')

		#entry does not exist, set error message	
		else:
			error = "Incorrect username or password."
	
	#redirect to same page with error message
	return render(request, 'login_page.html.j2', {'error': error})

#logout the user and redirect to create page with new content
def logout(request):
	auth.logout(request)
	return redirect("/")





