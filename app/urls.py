from django.urls import path
from app import views
from django.conf import settings # image related configuration package for dynamic response in webpage
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,PasswordChange,MypasswordResetForm,MySetPasswordForm

urlpatterns = [
    #path('', views.home), this is for when it is a component based fun
    path('',views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    #int pk is for primary key
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart',views.plus_cart,name='pluscart'),
    path('minuscart',views.minus_cart,name='minuscart'),
    path('removecart',views.remove_cart,name='removecart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('paymentdone/',views.payment_done,name="paymentdone"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=PasswordChange,success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset1.html',form_class=MypasswordResetForm),name="password_reset1"),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name="password_reset_confirm"),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
    path('fertilizers/',views.fertilizers,name='fertilizers'),
    path('fertilizers/<slug:data>', views.fertilizers, name='fertilizersdata'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('pestagri/',views.pestagri,name='pestagri'),
    path('pestagri/<slug:data>', views.pestagri, name='pestagridata'),
    path('pestaqua/',views.pestaqua,name='pestaqua'),
    path('pestaqua/<slug:data>',views.pestaqua,name='pestaquadata'),
    path('faq/',views.faq,name='faq'),
    path('equip/',views.equip,name='equip'),
    path('equip/<slug:data>',views.equip,name='equipdata'),
    ]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
#image related configuration for dynamic response in webpage
