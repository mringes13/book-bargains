from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .forms import CreateUserForm, CreateProfileForm, ListBookForm, MessageForm, AddRatingForm
from .models import Book, Cart, Wishlist, Transaction, Rating, Profile, Message, Reported
from .filters import BookFilter
# Create your views here.


def userLog(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'signup.html')

def messaging(request):
    return render(request, 'messaging.html')

def hometemp(request):
    return render(request, 'hometemp.html')

def buyList(request):
    return render(request, 'buyerListing.html')

def logoutuser(request):
    logout(request)
    return redirect('../')

#Each time a user is created, a cart and wishlist are also created
@receiver(post_save, sender=User)
def createcartandwishlist(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance)
        Wishlist.objects.create(owner=instance)
        Rating.objects.create(user=instance)

class HomePageView(ListView):
    model = Book
    template_name= 'search.html'

class SearchResultsView(ListView):
    model = Book
    template_name = 'searchresults.html'
    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(
                ISBN13__icontains=query) | Q(edition__icontains=query) | Q(
                    condition__icontains=query) | Q(field__icontains=query))
        return object_list

#This function is called when a user goes to create an account.
def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            raw_password = form.cleaned_data.get('password1')
            raw_email = form.cleaned_data.get('username')
            if 'bc.edu' in raw_email:
                user = form.save()
                user.save()
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect('../profile/')
            else:
                messages.error(request,"Please enter a valid BC email.")
                return redirect('signup')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})

#This function is called when users go to create a profile after first signing up.
def createprofile(request):
    p_form = CreateProfileForm(initial={'user':request.user})
    if request.method == "POST":
        p_form = CreateProfileForm(request.POST)
        if p_form.is_valid():
            Profile = p_form.save(commit=False)
            Profile.user = request.user
            Profile = p_form.save()
            User = request.user
            User.save()
            cleanfirstname = p_form.cleaned_data.get('first_name')
            cleanlastname = p_form.cleaned_data.get('last_name')
            User.first_name = cleanfirstname
            User.last_name = cleanlastname
            User.email = User.username
            User.save()
            return redirect('../')
        else:
            form = CreateProfileForm()
    return render(request, 'createprofile.html', {'p_form':p_form})

#This function is called when the user goes to create a book listing. The ISBN number is confirmed.
@login_required
def createlisting(request):
    newlistingform = ListBookForm(initial={'user':request.user})
    if request.method == "POST":
        newlistingform = ListBookForm(request.POST, request.FILES)
        if newlistingform.is_valid():
            isbnone = newlistingform.cleaned_data['ISBN13']
            isbntwo = newlistingform.cleaned_data['ISBN13Conf']
            if (isbnone == isbntwo):
                newlistingform = newlistingform.save(commit=False)
                newlistingform.user = request.user
                newlistingform = newlistingform.save()
                messages.success(request, "Success! Your book has been listed!")
                return redirect('../')
            elif (isbnone!=isbntwo):
                messages.success(request, "Make sure ISBN13 fields match.")
                return redirect('newlisting')
    return render(request, 'sellerListing.html', {'ListBookForm':ListBookForm})

#This function is related to viewing all available books and filtering based on user input.
def searchbooks(request):
    allbooks = Book.objects.all()
    myFilter = BookFilter(request.GET, queryset=allbooks)
    allbooks = myFilter.qs
    context = {'books':allbooks,'filter': myFilter,}
    return render(request, 'searchfilter.html', context)

def changeOrdering(request):
    allbooks = Book.objects.all()
    myFilter = BookFilter(request.GET, queryset=allbooks)
    allbooks = myFilter.qs
    context = {'books': allbooks, 'filter': myFilter}
    return render(request, 'searchfilter2.html', context)


##These functions are related to the cart and wishlist:
    #adding to cart
    #adding to wishlist
    #changing from wishlist to cart
    #viewing wishlist
    #viewing cart

@login_required
def addtocart(request, bookid):
    booktoadd = Book.objects.get(uuid=bookid)
    cart, created = Cart.objects.get_or_create(owner=request.user)
    cart.cartitem.add(booktoadd)
    cart.save()
    messages.success(request, "Success! A book has been added to the cart!")
    return redirect('search')

@login_required
def addtowishlist(request, bookid):
    booktoadd = Book.objects.get(uuid=bookid)
    wishlist, created = Wishlist.objects.get_or_create(owner=request.user)
    wishlist.item.add(booktoadd)
    wishlist.save()
    messages.success(request, "Success! A book has been added to your wishlist!")
    return redirect('search')

@login_required
def viewcart(request):
    currentcart = Cart.objects.get(owner=request.user)
    context = {'cart': currentcart}
    return render(request, 'cart.html', context)

@login_required
def viewwishlist(request):
    currentwishlist = Wishlist.objects.get(owner=request.user)
    context = {'wishlist': currentwishlist}
    return render(request, 'wishlist.html', context)

@login_required
def switchfromwishlisttocart(request, bookid):
    booktoswitch = Book.objects.get(uuid=bookid)
    currentwishlist = Wishlist.objects.get(owner = request.user)
    currentcart = Cart.objects.get(owner = request.user)
    currentwishlist.item.remove(booktoswitch)
    currentcart.cartitem.add(booktoswitch)
    messages.success(request, "Success! A book from your wishlist has been added to your cart.")
    return redirect('cart')

@login_required
def removefromcart(request, bookid):
    booktoremove = Book.objects.get(uuid=bookid)
    cart, created = Cart.objects.get_or_create(owner=request.user)
    cart.cartitem.remove(booktoremove)
    cart.save()
    messages.success(request, "Success! A book has been removed from your cart!")
    return redirect('cart')

@login_required
def removefromwishlist(request, bookid):
    booktoremove = Book.objects.get(uuid=bookid)
    wishlist, created = Wishlist.objects.get_or_create(owner=request.user)
    wishlist.item.remove(booktoremove)
    wishlist.save()
    messages.success(request, "Success! A book has been removed from your wishlist!")
    return redirect('wishlist')

#These two functions have to deal with the user viewing their own book listings and removing if necessary.
@login_required
def viewmyprofile(request):
    mycurrentbooks = Book.objects.filter(user = request.user)
    myprofile = Profile.objects.get(user = request.user)
    myratings = Rating.objects.get(user = request.user)
    myrecommendations = Book.objects.filter(field = myprofile.field)[0:3]
    context = {'mycurrentbooks':mycurrentbooks, 'myprofile':myprofile, 'myrecommendations':myrecommendations, 'myratings':myratings}
    return render(request, 'myprofile.html', context)

@login_required
def removelisting(request, bookid):
    booktoremove = Book.objects.get(uuid=bookid)
    booktoremove.delete()
    messages.success(request, "Success! Your book has been successfully removed from listings.")
    return redirect('myprofile')


@login_required
def reportedbook(request,bookid):
    booktoreport = Book.objects.get(uuid=bookid)
    userreporting = request.user
    userreported = booktoreport.user
    new_report = Reported(reporter = userreporting, reported = userreported, reportedbook = booktoreport)
    new_report.save()
    booktoreport.reported = True
    booktoreport.save()
    messages.success(request, "Thank you! This book has been reported. An admin may follow up with you if more information is needed.")
    return redirect('searchfilter')

def reporteduser(request,transactionid):
    reportattransaction = Transaction.objects.get(uuid=transactionid)
    booktoreport = Book.objects.get(uuid=reportattransaction.book.uuid)
    userreporting = request.user
    userreported = booktoreport.user
    new_report = Reported(reporter = userreporting, reported = userreported, reportedtransaction=reportattransaction)
    new_report.save()
    booktoreport.reported = True
    booktoreport.save()
    reportattransaction.buyerhasrated = True
    reportattransaction.sellerhasrated = True
    reportattransaction.status = 'Completed'
    reportattransaction.save()
    messages.success(request, "Thank you! This user has been reported. An admin may follow up with you if more information is needed.")
    return redirect('viewmytransactions')


#This function is called when the user goes to message the user from the cart. It will create a transaction instance.
@login_required
def createtransaction(request, bookid):
    newtransaction = Transaction.objects.create(buyer=request.user, book=Book.objects.get(uuid=bookid), seller=Book.objects.get(uuid=bookid).user)
    booktoremove = Book.objects.get(uuid=bookid)
    cart, created = Cart.objects.get_or_create(owner=request.user)
    cart.cartitem.remove(booktoremove)
    cart.save()
    messages.success(request, "Success! You have messaged the owner and have created a transaction. This item will be removed from your cart.")
    return redirect('viewtransactionmessages', selleruser=booktoremove.user, buyeruser=request.user, transactionid=newtransaction.uuid)

@login_required
def viewmytransactions(request):
    transactionsasseller = Transaction.objects.filter(seller=request.user) #get all transactions where the current user is the seller
    transactionsasbuyer = Transaction.objects.filter(buyer=request.user) #get all transactions where the current user is the buyer
    context = {'transactionsasseller':transactionsasseller, 'transactionsasbuyer':transactionsasbuyer}
    return render(request, 'mytransactions.html', context)

@login_required
def viewtransactionmessages(request, selleruser, buyeruser, transactionid):
    transactiontoview = Transaction.objects.get(uuid=transactionid)
    messagesseller = User.objects.get(username=selleruser)
    messagesbuyer = User.objects.get(username=buyeruser)
    messages = Message.objects.filter(transaction__in=Transaction.objects.filter(seller=messagesseller).filter(buyer=messagesbuyer)).order_by('creation_time')

    if messagesseller == request.user:
        notcurrentuser = messagesbuyer
    else:
        notcurrentuser = messagesseller

    newmessageform = MessageForm()
    if request.method=="POST":
        newmessageform=MessageForm(request.POST)
        if newmessageform.is_valid():
            newmessageform = newmessageform.save(commit=False)
            newmessageform.sender = request.user
            newmessageform.recipient = notcurrentuser
            newmessageform.transaction = transactiontoview
            newmessageform = newmessageform.save()
            return redirect('viewtransactionmessages', selleruser=messagesseller, buyeruser=messagesbuyer, transactionid=transactiontoview.uuid)
    context={'transactionmessages':messages, 'transaction':transactiontoview, 'form':newmessageform}
    return render(request, 'transactionmessages.html', context)


@login_required
def createmessage(request):
    newmessageform = MessageForm()
    if request.method == "POST":
        newmessageform = MessageForm(request.POST)
        if newmessageform.is_valid():
            newmessageform = newmessageform.save(commit=False)
            newmessageform.sender = request.user
            newmessageform = newmessageform.save()
    return render(request, 'messages.html', {'MessageForm':MessageForm})

@login_required
def donewithtransaction(request, doneusername, transactionid):
    doneuser = User.objects.get(username=doneusername)
    
    transaction = Transaction.objects.get(uuid=transactionid)
    if doneuser==transaction.buyer:
        transaction.buyerhasrated = True
        transaction.save()
    else:
        transaction.sellerhasrated = True
        transaction.save()

    if transaction.buyerhasrated and transaction.sellerhasrated:
        #transaction is complete, mark book as sold
        booktomarkassold = transaction.book 
        booktomarkassold.sold = True
        booktomarkassold.save()

    if doneuser==transaction.buyer:
        addratingform = AddRatingForm()
        if request.method == "POST":
            addratingform = AddRatingForm(request.POST)
            if addratingform.is_valid():
                addedrating = addratingform.cleaned_data['addedrating']
                usertoupdate = User.objects.get(username=transaction.seller)
                currentusersellerrating = float(Rating.objects.get(user=usertoupdate).sellerrating)
                currentnumberofsellerratings = float(Rating.objects.get(user=usertoupdate).numberofsellerratings)
                Rating.objects.filter(user=usertoupdate).update(sellerrating=((currentnumberofsellerratings*currentusersellerrating)+(addedrating))/(currentnumberofsellerratings+1)) #(9*(5.0)+1*(3.0))/10
                Rating.objects.filter(user=usertoupdate).update(numberofsellerratings=currentnumberofsellerratings+1)
                messages.success(request, "Thank you for rating this user!")
                return redirect('viewmytransactions')
    else:
        addratingform = AddRatingForm()
        if request.method == "POST":
            addratingform = AddRatingForm(request.POST)
            if addratingform.is_valid():
                addedrating = addratingform.cleaned_data['addedrating']
                usertoupdate = User.objects.get(username=transaction.buyer)
                currentuserbuyerrating = float(Rating.objects.get(user=usertoupdate).buyerrating)
                currentnumberofbuyerratings = float(Rating.objects.get(user=usertoupdate).numberofbuyerratings)
                Rating.objects.filter(user=usertoupdate).update(buyerrating=((currentnumberofbuyerratings*currentuserbuyerrating)+(addedrating))/(currentnumberofbuyerratings+1)) #(9*(5.0)+1*(3.0))/10
                Rating.objects.filter(user=usertoupdate).update(numberofbuyerratings=currentnumberofbuyerratings+1)
                messages.success(request, "Thank you for rating this user!")
                return redirect('viewmytransactions')

    return render(request, 'addrating.html', {'form':addratingform})