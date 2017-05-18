# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings

from server_project import forms as my_forms
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from server_project import models as my_models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

import os

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

@login_required(login_url='/login/')
def main_site(request):

	form = my_forms.UploadFileForm()

	files = [ f.modelo.name.split('/')[-1] for f in request.user.user_file_set.all() ]

	context = {'form' : form, 'files' : files }
	return HttpResponse(render(request, 'main_site.html', context))

	# https://docs.djangoproject.com/en/1.11/topics/auth/default/#how-to-log-a-user-in
	#if request.user.is_authenticated:
		# Do something for authenticated users.
	#    ...
	#else:
		# Do something for anonymous users.
	#    ...




@login_required(login_url='/login/')
def upload_file(request):
	
	if request.method == 'POST' and request.FILES['file']:

		form = my_forms.UploadFileForm(request.POST, request.FILES)

		if form.is_valid:

			myfile = request.FILES['file']


			# If you are constructing an object manually, you can simply 
			# assign the file object from request.FILES to the file 
			# field in the model
			# https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/#handling-uploaded-files-with-a-model
			user_file = my_models.User_File.objects.create(
								user=request.user,
								modelo=myfile,
								size=myfile.size,
			)

			user_file.save()

	return HttpResponseRedirect('/')





@login_required(login_url='/login/')
def download(request,file_name):
	user_folder = 'user_{0}_{1}/{2}'.format(request.user.id, request.user.username, file_name)
	file_path = os.path.join(settings.MEDIA_ROOT, user_folder)
	
	
	file_wrapper = FileWrapper(file(file_path,'rb'))
	file_mimetype = mimetypes.guess_type(file_path)

	response = HttpResponse(file_wrapper, content_type=file_mimetype )
	response['X-Sendfile'] = file_path
	response['Content-Length'] = os.stat(file_path).st_size
	response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name) 

	return response


	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
	raise Http404