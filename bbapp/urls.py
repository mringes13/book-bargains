from django.urls import path
from django.contrib.auth import views as djangoviews
from bbapp import views
from bbapp.forms import UserLoginForm
from .views import HomePageView, SearchResultsView

urlpatterns = [
    path('', views.hometemp, name='home'),
    path('messaging/', views.messaging, name='messaging'),
    path('signup/', views.signup, name="signup"),
    path('profile/', views.createprofile, name="profile"),
    path('land/', views.hometemp, name="land"),
    path('listnew/', views.createlisting, name="newlisting"), #already linked to see new listing
    path('buyList/', views.buyList, name="buyList"),
    path('searchresults', SearchResultsView.as_view(), name = "searchresults"),
    path('search/', views.searchbooks, name = "search"),
    path('searchfilter/', views.searchbooks, name='searchfilter'),
    path('searchfilter2', views.changeOrdering, name='searchfilter2'),

    path('logout/', views.logoutuser, name='logout'),
    path('login/',djangoviews.LoginView.as_view(template_name="login.html",authentication_form=UserLoginForm),name='login'),

    path('messages/', views.createmessage, name='messages'),
    path('createtransaction/(?P<bookid>\s+)', views.createtransaction, name='createtransaction'),
    path('viewmytransactions/', views.viewmytransactions, name='viewmytransactions'),
    path('viewtransactionmessages/(?P<selleruser>\s+)(?P<buyeruser>\s+)(?P<transactionid>\s+)', views.viewtransactionmessages, name='viewtransactionmessages'),
    path('donewithtransaction/(?P<doneusername>\s+)(?P<transactionid>\s+)', views.donewithtransaction, name='donewithtransaction'),
    path('reportuser/(?P<transactionid>\s+)', views.reporteduser, name='reportuser'),
    
    path('cart/', views.viewcart, name='cart'),
    path('addtocart/(?P<bookid>\s+)', views.addtocart, name='addtocart'),
    path('addtowishlist/(?P<bookid>\s+)', views.addtowishlist, name='addtowishlist'),
    path('reportedbook/(?P<bookid>\s+)', views.reportedbook, name='reportedbook'),
    path('removefromcart/(?P<bookid>\s+)', views.removefromcart, name='removefromcart'),
    path('removefromwishlist/(?P<bookid>\s+)', views.removefromwishlist, name='removefromwishlist'),
    path('switchfromwishlisttocart/(?P<bookid>\s+)', views.switchfromwishlisttocart, name='switchfromwishlisttocart'),
    path('wishlist/', views.viewwishlist, name='wishlist'),
    path('myprofile/', views.viewmyprofile, name='myprofile'),
    path('removelisting/(?P<bookid>\s+)', views.removelisting, name='removelisting'),
    
]
