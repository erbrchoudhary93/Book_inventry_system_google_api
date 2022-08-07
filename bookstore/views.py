from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import Store, Books
from .forms import Add_Store, Edit_Book, Search ,CreateUserForm
import requests
from django.contrib import messages
import json


# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        fm = CreateUserForm(request.POST)
        if fm.is_valid():
            fm.save()
            user = fm.cleaned_data.get('username')
            messages.success(request,user+" Account Created Successfully  !!")
            return HttpResponseRedirect('/login/')
    else:
        fm = CreateUserForm()
    return render(request, 'bookstore/signup.html', {'form': fm})




def user_login(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request.POST,data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data.get('username')
            pas = fm.cleaned_data.get('password')
            user = authenticate(username=uname, password=pas)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/show1/')
            else:
                messages.info(request," Usernae or Password Incorrect  !!")
                fm=AuthenticationForm()
           
    else:
        
        fm = AuthenticationForm()
    return render(request, 'bookstore/login.html', {'forms': fm})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def store(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = Add_Store(request.POST)
            if fm.is_valid():
                regis = request.user
                store_name = fm.cleaned_data['store_name']
                loc = fm.cleaned_data['loc']
                s = Store(regis=regis,store_name=store_name,loc=loc)
                s.save()
                # messages.success(request, 'Data added')
                return HttpResponseRedirect('/show1/')
        else:
            fm = Add_Store()
        return render(request, 'bookstore/store.html', {'forms': fm})
    else:
        return HttpResponseRedirect('/login/')


def book(request, idd, id, title, img):
    if request.user.is_authenticated:
        # if request.method == 'POST':
        s = Store.objects.get(id=idd)
        fm = Books.objects.filter(refid=id, store=s)

        if fm:
            print('In else------------------------')
            fm[0].count += 1
            fm[0].save()
        else:
            # print('in elelele')
            fm = Books(store=s, refid=id, bookname=title, img=img, count=1)
            fm.save()
        # return HttpResponse('ok')
        return HttpResponseRedirect(f'/show/{idd}')
        # else:
        #     fm = Books_F()
        # return render(request, 'bookstore/book.html', {'forms': fm})
    else:
        return HttpResponseRedirect('/login/')


def edit_book(request, id):
    if request.user.is_authenticated:
        bookstore = Books.objects.get(id=id)
        # storeid=Store.objects.get(id=id)
        print(bookstore.store.id)
        book_store_id = bookstore.store.id
        # print(storeid)
        if request.method == 'POST':

            fm = Edit_Book(instance=bookstore, data=request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Book added')
        else:
            fm = Edit_Book(instance=bookstore)
        return render(request, 'bookstore/edit.html', {'forms': fm,'idd':book_store_id})
    else:
        return HttpResponseRedirect('/login/')


def show_book(request, id):
    if request.user.is_authenticated:
        bookstore = Books.objects.filter(store=id)
        if not bookstore.exists():
            messages.success(request, 'Inventory is empty')
        return render(request, 'bookstore/show.html', {'data': bookstore, 'idd': id})
        # else:
        #     return HttpResponseRedirect('/store/')
    else:
        return HttpResponseRedirect('/login/')


def show_store(request):
    if request.user.is_authenticated:
        bookstore = Store.objects.filter(regis=request.user)
        if bookstore.exists():
            return render(request, 'bookstore/show1.html', {'data': bookstore})
        else:
            return HttpResponseRedirect('/store/')
    else:
        return HttpResponseRedirect('/login/')


def del_book(request, id):
    if request.user.is_authenticated:
        Books.objects.get(id=id).delete()
        return HttpResponseRedirect('/show1/')
    else:
        return HttpResponseRedirect('/login/')


def search(request, idd):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = Search(request.POST)
            if fm.is_valid():
                googleapi = 'https://www.googleapis.com/books/v1/volumes?q='
                search = fm.cleaned_data['search']
                googleapi += search
                j = requests.get(googleapi)
                j = j.json()
                print(j['items'][1])
                print('-----------------------')
                if j['totalItems'] == 0:
                    messages.success(request, 'Book not found')
                else:
                    l1, l2, l3 = [], [], []

                    for i in j['items']:
                        l1.append(i['id'])
                        l2.append(i['volumeInfo']['title'])
                        try:
                            l3.append(i['volumeInfo']['imageLinks']['thumbnail'])
                        except:
                            l3.append('#')

                    d = zip(l1, l2, l3)
                    return render(request, 'bookstore/insert.html', {'d': d, 'idd': idd})
        else:
            fm = Search()
        return render(request, 'bookstore/search.html', {'forms': fm})
    else:
        return HttpResponseRedirect('/login/')
