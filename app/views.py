#all the functions are sepcified here..!
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required#for functional based
from django.utils.decorators import method_decorator
from .models import Customer,Product,Cart,Orderplaced
from .forms import CustomerRegistrationForm
from django.contrib import messages
#def home(request):# this is for the component bases
# return render(request, 'app/home.html')
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from .models import Customer,Product,Cart,Orderplaced

class ProductView(View):
 def get(self,request):
  Cpesticides = Product.objects.filter(category='P')
  Fertlizers=Product.objects.filter(category='F')
  Pesticides=Product.objects.filter(category='PE')
  Equipment=Product.objects.filter(category='E')
  return render(request,'app/home.html',{'Cpesticides':Cpesticides,'Fertlizers':Fertlizers,'Pesticides':Pesticides,'Equipment':Equipment})
#class baseed callinhor rendering

#def product_detail(request):
# return render(request, 'app/productdetail.html')

class ProductDetailView(View):
 def get(self, request, pk, product=None):
  product=Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
   item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})



@login_required()
def add_to_cart(request):
 #we need product id and user name
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')

@login_required()
def show_cart(request):
 if request.user.is_authenticated:
  user=request.user
  cart=Cart.objects.filter(user=user)
  #print(cart)
  amount=0.0
  shipping_amount=80.0
  total_amount=0.0
  cart_product=[p for p in Cart.objects.all() if p.user==user]
  #print(cart_product)
  if cart_product:
   for p in cart_product:
    temp=(p.quantity*p.product.discounted_price)
    amount+=temp
    totalamount=amount+shipping_amount
    return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
  else:
   return render(request,'app/empycart.html')

def plus_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
  c.quantity+=1
  c.save()
  amount =0.0
  shipping_amount=80.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   temp = (p.quantity * p.product.discounted_price)
   amount += temp

  data={
    'quantity':c.quantity,
    'amount':amount,
    'totalamount':amount + shipping_amount
   }
  return JsonResponse(data)

def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity -= 1
  c.save()
  amount = 0.0
  shipping_amount = 80.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   temp = (p.quantity * p.product.discounted_price)
   amount += temp

  data = {
    'quantity': c.quantity,
    'amount': amount,
    'totalamount': amount + shipping_amount
   }

 return JsonResponse(data)

def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity -= 1
  c.delete()
  amount = 0.0
  shipping_amount = 80.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   temp = (p.quantity * p.product.discounted_price)
   amount += temp

  data = {
    'amount': amount,
    'totalamount': amount + shipping_amount
   }

 return JsonResponse(data)



def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')
@login_required()
def address(request):
 add=Customer.objects.filter(user=request.user)#filtered for a user expected data
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})
@login_required()
def orders(request):
 op=Orderplaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op,})

def pestagri(request,data=None):
 if data==None:
  pest=Product.objects.filter(category='P')
 elif data=='Plantic' or data=='BigHaat':
  pest=Product.objects.filter(category='P').filter(brand=data)
 elif data=='below':
  pest=Product.objects.filter(category='P').filter(discounted_price__lt=500)
 elif data=='above':
  pest=Product.objects.filter(category='P').filter(discounted_price__gt=500)
 return render(request, 'app/pestagri.html',{'pest':pest})

#def login(request):
 #return render(request, 'app/login.html')
 # we are removing login since we are using default athuntication no need we directly write them in urls.py
# defaultly loginform is created by django we just use them


class CustomerRegistrationView(View):
 def get(self,request):
  form=CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 def post(self,request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulations !! You have Registered Sucessfully')
   form.save()
  return render(request,'app/customerregistration.html',{'form':form})




#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')
@login_required
def checkout(request):
 user=request.user
 add=Customer.objects.filter(user=user)
 cart=Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=80.0
 totalamount=0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart:
  for p in cart_product:
   temp = (p.quantity * p.product.discounted_price)
   amount += temp
   totalamount= amount + shipping_amount
 return render(request, 'app/checkout.html', {'add':add,'totalamount':totalamount,'cart':cart})

@login_required
def payment_done(request):
 user=request.user
 custid=request.GET.get('custid')
 customer=Customer.objects.get(id=custid)
 cart=Cart.objects.filter(user=user)
 for c in cart:
  Orderplaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
  c.delete()
 return redirect("orders")



def fertilizers(request,data=None):
 if data == None:
  pest = Product.objects.filter(category='F')
 elif data == 'GeoLife' or data == 'Uravara':
  pest = Product.objects.filter(category='F').filter(brand=data)
 elif data=='below':
  pest=Product.objects.filter(category='F').filter(discounted_price__lt=1500)
 elif data=='above':
  pest=Product.objects.filter(category='F').filter(discounted_price__gt=1500)

 return render(request, 'app/fertilizers.html', {'pest': pest})
 #return render(request,'app/fertilizers.html')

def aboutus(request):
 return render(request,'app/aboutus.html')


def pestaqua(request,data=None):
 if data == None:
  pest = Product.objects.filter(category='PE')
 elif data == 'Aquagrow' or data == 'AquaVitals':
  pest = Product.objects.filter(category='PE').filter(brand=data)
 elif data=='below':
  pest=Product.objects.filter(category='PE').filter(discounted_price__lt=1500)
 elif data=='above':
  pest=Product.objects.filter(category='PE').filter(discounted_price__gt=1500)
 return render(request, 'app/pestaqua.html', {'pest': pest})
 #return render(request,'app/pestaqua.html')

def faq(request):
 return render(request,'app/faq.html')

def equip(request,data=None):
 if data == None:
  equip = Product.objects.filter(category='E')
 elif data == 'Aquagri' or data == 'Allexpress':
  equip = Product.objects.filter(category='E').filter(brand=data)
 elif data=='below':
  equip=Product.objects.filter(category='E').filter(discounted_price__lt=1500)
 elif data=='above':
  equip=Product.objects.filter(category='E').filter(discounted_price__gt=1500)

 return render(request, 'app/equip.html', {'equip': equip})#mapping fun
 #return render(request,'app/equip.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get(self,request):
  form=CustomerProfileForm()
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

 def post(self,request):
  form=CustomerProfileForm(request.POST)
  if form.is_valid():
   user=request.user
   name=form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode=form.cleaned_data['zipcode']
   regis=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   regis.save()
   messages.success(request,'Congratulations!! Profile Updated Sucessfully')

  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

