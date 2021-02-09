from django.shortcuts import render, HttpResponse, redirect
from .models import Quote, User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def create(request):
    
    if request.method == "POST":

        errors = User.objects.create_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()   

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['new_user'] = new_user.id
        return redirect('/results')

def results(request):
    if 'new_user' not in request.session:
        return redirect('/')

    all_quotes = Quote.objects.all()
    context = {
        'confirmed_user': User.objects.get(id=request.session['new_user']),
        'all_quotes': all_quotes,
            
    }
    return render(request, 'home_page.html', context)


def login(request):
    if request.method == "POST":

        errors = User.objects.authenticate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        login = User.objects.filter(email=request.POST['email'])
        logged_user = login[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            

            request.session['new_user'] = logged_user.id
            return redirect('/results')


def logout(request):
    request.session.clear()
    return redirect('/')

def new_quote(request):
    if 'new_user' not in request.session:
        return redirect('/')

    if request.method == "POST":

        errors = Quote.objects.quote_manager(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/results')

        user = User.objects.get(id=request.session['new_user'])
        my_new_quote = Quote.objects.create(
            author = request.POST['author'],
            quote = request.POST['quote'],
            creator = user
        )
        user.added_quotes.add(my_new_quote)

        return redirect('/results')

def author_page(request, id):
    if 'new_user' not in request.session:
        return redirect('/')

    all_quotes = Quote.objects.all()
    context = {
        'quote': Quote.objects.get(id=id),
        'current_user': User.objects.get(id=request.session['new_user']),
        'all_quotes': all_quotes,

    }
    return render(request, 'author_page.html', context)


def like_quote(request, id):
    user = User.objects.get(id=request.session['new_user'])
    quote = Quote.objects.get(id=id)
    user.added_quotes.add(quote)
    user.save()

    return redirect('/results')


def delete(request, id):
    quote = Quote.objects.get(id=id)
    quote.delete()
    return redirect('/results')




def edit(request):

    context = {
        'confirmed_user': User.objects.get(id=request.session['new_user']),
            
    }
    return render(request, 'edit_account.html', context)

def update(request, id):
    if request.method == "POST":

        errors = User.objects.update(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/account_edit')
    
        to_update = User.objects.get(id=id)
        to_update.first_name = request.POST['first_name']
        to_update.last_name = request.POST['last_name']
        to_update.email = request.POST['email']
        to_update.save()

    return redirect('/results')


def this_quote(request, id):
    if 'new_user' not in request.session:
        return redirect('/')

    context = {
        'quote': Quote.objects.get(id=id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'home_page.html', context)