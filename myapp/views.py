from django.shortcuts import render, redirect
from .models import Hiace, Book
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import loginequired

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')
    else:
        return render(request, 'signin.html')

def findhiace(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        dest = request.POST.get('destination')
        date = request.POST.get('date')
        hiace_list = Hiace.objects.filter(source=source, dest=dest, date=date)
        if hiace_list:
            return render(request, 'another_list.html', locals())
        else:
            return render(request, 'no_hiace_available.html')
    else:
        return render(request, 'findhiace.html')


# check views from chargpt
def bookings(request):
    context = {}
    if request.method == 'POST':
        id = request.POST.get('hiace_id')
        seats = request.POST.get('no_seats') 
        selected_seats = request.POST.get('selected_seats')
        if seats and selected_seats:
            seats = int(seats)
            hiace = Hiace.objects.get(id=id)
            if hiace:
                if hiace.rem > int(seats):
                    name = hiace.hiace_name
                    cost = int(seats) * hiace.price
                    source = hiace.source
                    dest = hiace.dest
                    nos = Decimal(hiace.nos)
                    price = hiace.price
                    date = hiace.date
                    time = hiace.time
                    username = request.user.username
                    email = request.user.email
                    userid = request.user.id
                    rem = hiace.rem - seats
                    Hiace.objects.filter(id=id).update(rem=rem)
                    
                    # Filter the data entered by the user
                    hiace_seats = hiace.name_seats.split(',')
                    selected_seats = selected_seats.split(',')
                    name_seats = [seat for seat in hiace_seats if seat in selected_seats]
                    name_seats = ','.join(name_seats)
                    
                    book = Book.objects.create(name=username, email=email, userid=userid, hiace_name=name,
                                            source=source, hiaceid=id,
                                            dest=dest, price=price, nos=seats, name_seats=name_seats, date=date, time=time,
                                            status='BOOKED')
                    print('------------book id-----------', book.id)
                    # book.save()
                    return render(request, 'bookings.html', locals())
                else:
                    return render(request, 'no_hiace_available.html')
            else:
                return render(request, 'no_hiace_available.html')
        else:
            return render(request, 'no_hiace_available.html')                
    else:
        return render(request, 'findhiace.html')



# working views
# def bookings(request):
#     context = {}
#     if request.method == 'POST':
#         id = request.POST.get('hiace_id')
#         seats = request.POST.get('no_seats') 
#         if seats:
#             seats = int(seats)
#             hiace = Hiace.objects.get(id=id)
#             if hiace:
#                 if hiace.rem > int(seats):
#                     name = hiace.hiace_name
#                     cost = int(seats) * hiace.price
#                     source = hiace.source
#                     dest = hiace.dest
#                     nos = Decimal(hiace.nos)
#                     name_seats = hiace.name_seats
#                     price = hiace.price
#                     date = hiace.date
#                     time = hiace.time
#                     username = request.user.username
#                     email = request.user.email
#                     userid = request.user.id
#                     rem = hiace.rem - seats
#                     Hiace.objects.filter(id=id).update(rem=rem)
#                     book = Book.objects.create(name=username, email=email, userid=userid, hiace_name=name,
#                                             source=source, hiaceid=id,
#                                             dest=dest, price=price, nos=seats, name_seats=name_seats, date=date, time=time,
#                                             status='BOOKED')
#                     print('------------book id-----------', book.id)
#                     # book.save()
#                     return render(request, 'bookings.html', locals())
#                 else:
#                     return render(request, 'no_hiace_available.html')
#             else:
#                 return render(request, 'no_hiace_available.html')
#         else:
#             return render(request, 'no_hiace_available.html')                
#     else:
#         return render(request, 'findhiace.html')


# @loginequired(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id = request.POST.get('hiace_id')
        #seats = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id)
            hiace = Hiace.objects.get(id=book.hiaceid)
            rem = hiace.rem + book.nos
            Hiace.objects.filter(id=book.hiaceid).update(rem=rem)
            #nos = book.nos - seats
            Book.objects.filter(id=id).update(status='CANCELLED')
            Book.objects.filter(id=id).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that hiace"
            return render(request, 'error.html', context)
    else:
        return render(request, 'findhiace.html')


# @loginequired(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id = request.user.id
    book_list = Book.objects.filter(userid=id)
    if book_list:
        return render(request, 'booklist.html', locals())
    else:
        context["error"] = "Sorry no hiacees booked"
        return render(request, 'findhiace.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(name, email, password, )
        if user:
            login(request, user)
            return render(request, 'thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'signup.html', context)
    else:
        return render(request, 'signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name
            context["id"] = request.user.id
            return render(request, 'success.html', context)
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'success.html', context)        
               