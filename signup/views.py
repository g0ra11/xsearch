from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegForm, LogForm, SearchForm
from . import doquerry
from .search import search_routine
import requests, html, re

facebook_pic_re = re.compile("src=\"[^\"]+\"")


def handle_errors(request, error_code):
    if error_code == 1:
        messages.error(request, 'passwords do not match')
    if error_code == 2:
        messages.error(request, 'username already existing')
    if error_code == 3:
        messages.error(request, 'email already in use')
    if error_code == 4:
        messages.error(request, 'connection with database failed')
    if error_code == 5:
        messages.error(request, 'username not existing')
    if error_code == 6:
        messages.error(request, 'wrong password')
    if error_code == 8:
        messages.error(request, 'No network')
    if error_code == 33:
        messages.error(request, 'You have been blocked')


def register(request):
    if doquerry.isvalid(request):
        return redirect('/search')

    if request.method == 'POST':  # If the form has been submitted...
        form = RegForm(data=request.POST)   # A form bound to the POST data
        if form.is_valid():
            res = doquerry.register(form.cleaned_data)

            if res != 0:
                handle_errors(request, res)
                return redirect('/register')
            else:
                messages.success(request, 'Account registered for approval')
                return redirect('/register')

    else:
        form = RegForm()  # An unbound form    return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def test_graph(request):
    return render(request, 'graph.html')

def search(request):
    adm = doquerry.is_admin(request)

    if request.method == 'POST':
        form = SearchForm(data=request.POST)  # A form bound to the POST data
        print(form.errors)
        if form.is_valid():  # All validation rules pass
            querry = form.cleaned_data['search']
            results = search_routine(querry)
            if type(results) == int:
                handle_errors(request, results)
                return redirect('/search')
            doquerry.update_search(request, querry)
            my_dict = {"querry": querry, "results": results}
            return render(request, 'search_results.html', {'data': my_dict, 'adm': adm})

    else:
        result = doquerry.isvalid(request)
        if result == 0:
            return render(request, 'search_invalid.html')
        else:
            form = SearchForm()
            return render(request, 'search.html', {'name': result['user'], 'form': form, 'adm': adm})


def user(request):
    result = doquerry.isvalid(request)
    adm = doquerry.is_admin(request)
    if result == 0:
        return render(request, 'search_invalid.html')
    else:
        return render(request, 'userdata.html', {'adm': adm, 'username': result['user'], 'email': result['email'], 'hist': result['hist']})


def login(request):
    if doquerry.isvalid(request):
        return redirect('/search')

    if request.method == 'POST':  # If the form has been submitted...
        form = LogForm(data=request.POST)   # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            res = doquerry.login(request, form.cleaned_data)
            if res == 0:
                return redirect('/search')
            else:
                handle_errors(request, res)
                return redirect('/login')

    else:
        form = LogForm()

    return render(request, 'my_login.html', {'form': form})


def logout(request):
    doquerry.logout(request)
    return redirect('/search')


def admin(request):
    adm = doquerry.is_admin(request)

    if adm:
        reqs = doquerry.get_requests()
        users = doquerry.get_users()
        for entry in users:
            if entry['username'] == adm:
                entry['is_cur'] = 1
            else:
                entry['is_cur'] = 0
            if 'is_blk' not in entry:
                entry['is_blk'] = 0
        return render(request, 'admin_view.html ', {'requests': reqs, 'users': users, 'adm': adm})
    else:
        return render(request, 'admin_invalid.html')


def home(request):
    return render(request, 'home.html')


def node_decode(request, name):
    link = ''
    print(name)
    if 'facebook' in name:
        link = facebook_decode(name)
    print('link =', link)
    return render(request, 'placeholder.html ', {'data': link})


def app(request, name):
    adm = doquerry.is_admin(request)
    if not adm:
        return redirect('/home')
    doquerry.handle_req(name, 1)
    return redirect('/admin')


def dis(request, name):
    adm = doquerry.is_admin(request)
    if not adm:
        return redirect('/home')
    doquerry.handle_req(name, 0)
    return redirect('/admin')


def blk(request, name):
    adm = doquerry.is_admin(request)
    if not adm:
        return redirect('/home')
    doquerry.block_user(name, 1)
    return redirect('/admin')


def unb(request, name):
    adm = doquerry.is_admin(request)
    if not adm:
        return redirect('/home')
    doquerry.block_user(name, 0)
    return redirect('/admin')


def delete(request, name):
    adm = doquerry.is_admin(request)
    if not adm:
        return redirect('/home')
    doquerry.delete_user(name)
    return redirect('/admin')


def facebook_decode(link):
    res = requests.get(link)
    split = res.text.split('profilePicThumb')[1]
    link = facebook_pic_re.findall(split)[0][5:-1]
    return html.unescape(link)


