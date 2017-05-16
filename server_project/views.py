# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from server_project import forms as my_forms
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from server_project import models as my_models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


def register(request):
	if request.method == 'POST':

		form = my_forms.UserRegistrationForm(request.POST)

		if form.is_valid():
			userObj = form.cleaned_data
			username = userObj['username']
			email =  userObj['email']
			password =  userObj['password']

			# If the User does not already exists in DB
			if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				
				# Create the User in DB
				User.objects.create_user(username, email, password)
				
				# Authentication
				user = authenticate(username = username, password = password)
				login(request, user)
				return HttpResponseRedirect('/')

			# If exists, then error
			else:
				raise forms.ValidationError('Username or email already exists')
	
	elif request.method == 'GET':
		form = my_forms.UserRegistrationForm()

	return render(request, 'register.html', {'form' : form})



# We can use a decorator to require a login, as described in
# https://docs.djangoproject.com/en/1.11/topics/auth/default/#the-login-required-decorator
#
# from django.contrib.auth.decorators import login_required
# @login_required
# @login_required(login_url='/accounts/login/')

def main_site(request):

	form = my_forms.UploadFileForm()	

	return HttpResponse(render(request, 'main_site.html', {'form' : form}))

	# https://docs.djangoproject.com/en/1.11/topics/auth/default/#how-to-log-a-user-in
	#if request.user.is_authenticated:
		# Do something for authenticated users.
	#    ...
	#else:
		# Do something for anonymous users.
	#    ...




@login_required
def upload_file(request):
	
	if request.method == 'POST' and request.FILES['file']:

		form = my_forms.UploadFileForm(request.POST, request.FILES)

		if form.is_valid:

			myfile = request.FILES['file']

			#fs = FileSystemStorage()
			#filename = fs.save(myfile.name, myfile)


			# If you are constructing an object manually, you can simply 
			# assign the file object from request.FILES to the file 
			# field in the model
			# https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/#handling-uploaded-files-with-a-model
			user_file = my_models.User_File.objects.create(
								user=request.user,
								modelo=myfile,
								localname=myfile.name,
								size=myfile.size,
			)

			user_file.save()


    
	return HttpResponseRedirect('/')