from django.db import models
import re
from time import localtime, strftime, strptime
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['email'])

        if len(postData['first_name']) <2:
            errors['first_name'] = "Name must be more than two characters."
        if len(postData['last_name']) <2:
            errors['last_name'] = "Last name must be more than two characters."
        if len(postData['email']) <2:
            errors['email'] = "Must be a valid email address."
        if len(postData['password']) <8:
            errors['password'] = "Password must be more than 8 characters."
        
        if (postData['password']) != (postData['password_confirm']):
            errors['password'] = "Passwords need to match."

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email, try again."

        if len(email) ==1:
            errors ['email'] = "Email is already registered"
        return errors


    def authenticate(self, postData):
        errors = {}
        if len(postData['email']) <2:
            errors['email'] = "Must be a valid email address."

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email dude, try again."

        if len(postData['password']) <8:
            errors['password'] = "Password must be more than 8 characters."

        check = User.objects.filter(email=postData['email'])
        if not check:
            errors['email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), check[0].password.encode()):
                errors['email'] = "Email and password do not match."
        return errors


    def update(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['email'])

        if len(postData['first_name']) <2:
            errors['first_name'] = "Name must be more than two characters."
        if len(postData['last_name']) <2:
            errors['last_name'] = "Last name must be more than two characters."
        if len(postData['email']) <2:
            errors['email'] = "Must be a valid email address."

        if len(email) ==1:
            errors ['email'] = "Email is already registered"
        return errors
        





class QuoteManager(models.Manager):
    def quote_manager(self, postData):
        errors = {}

        if len(postData['author']) <= 3:
            errors['author'] = "Author name must be more than 3 characters."
        if len(postData['author']) <= 0:
            errors['author'] = "Author field must be filled in."

        if len(postData['quote']) <= 10:
            errors['my_quote'] = "Quote field must have at least 10 characters."
        if len(postData['quote']) <= 0:
            errors['this_quote'] = "Quote field must be filled in."

        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.TextField()
    creator = models.ForeignKey(User, related_name="quotes_uploaded", on_delete = models.CASCADE)
    users_added = models.ManyToManyField(User, related_name="added_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

