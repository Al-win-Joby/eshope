import email
from itertools import product
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import JsonResponse
from account.models import Accounts, Orders ,Referrel ,Wallet ,tempAccount
from django.urls import reverse
import os
from store import views as pp
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from twilio.rest import Client

from store.models import Products, RealOffers
# Create your views here.
rotp = 9999

def loginn(request):
    if request.user.is_authenticated:
        
      if request.user.is_admin==False:
         return redirect('store/home')
    return render(request,'loginReal.html')

def signup(request):
    return render(request,'signupReal.html')  
def signedup(request):
    if request.method=='POST':
        #print("signedup")
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('first_name')
        referrel= request.POST.get('referrel')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2') 
        phone_number=request.POST.get('phone_number')
        if email=="" or first_name=="" or last_name=="" or username=="" or password1=="" or password2=="" or phone_number=="":
            messages.info(request,"Require all fields")
            return redirect('signup')
           
        if password1==password2: 
                
            if Accounts.objects.filter(email=email).exists():
                messages.info(request,"Email exist")
                return redirect('signup')
            elif Accounts.objects.filter(phone_number=phone_number).exists():
                messages.info(request,"Phone number exist")
                return redirect('signup') 
                                
            else:
                global referrelG 
                referrelG=""
                if referrel != "":
                    if Referrel.objects.filter(code=referrel).exists():
                        referrelG = referrel

                global user 
                newuser= tempAccount()
                newuser.first_name=first_name
                newuser.last_name=last_name
                newuser.email = email
                newuser.phone_number= phone_number
                newuser.password = password1
                newuser.save()
                user={'first_name':first_name,'last_name':last_name,'phone_number':phone_number,'username':username,'email':email,'password':password1}
                #user= Accounts.objects.create_user(first_name=first_name,last_name=last_name,phone_number=phone_number,username=username,email=email,password=password1)
                resp= redirect('signed_up')
                resp.set_cookie('first_name',first_name)
                return resp

        else:
             return render(request,'signup.html')


def signed_up(request):
    import random

    # prints a random value from the list

    list=range(1000,9999)
    otp=random.choice(list)


    account_sid ='AC0c82fc0f46279be5c92de65a35a2a481'
    auth_token = '21816cd3c2fb16d9fb0af0800b9bbc1c'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    body = otp,
    from_ = '+17174936731',
    to    = '+919072863781'
    )

    global rotp
    request.session['otp']=otp 
    rotp= otp #,'xyz':"xyz"}   
    return render(request,'otp.html')


def verifynumber(request):

    if 'phone' in request.COOKIES:
        phone_number = request.COOKIES['phone']
    else:    
        phone_number=request.POST.get('phone_number')
    #print(phone_number+"dddddddddd")
    if Accounts.objects.filter(phone_number=phone_number).exists():
        user=Accounts.objects.get(phone_number=phone_number)
        resp=redirect('otplogin')
        resp.set_cookie('phone',phone_number)
        print(user.username)
        if user is not None:
            import random
            # prints a random value from the list

            list=range(1000,9999)
            otp=random.choice(list)

            account_sid ='AC0c82fc0f46279be5c92de65a35a2a481'  
            auth_token = '21816cd3c2fb16d9fb0af0800b9bbc1c'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
            body = otp,
            from_ = '+17174936731',
            to    = '+919072863781'
            )
            print(otp )
            global rotp
            request.session['otp']=otp
            
            return resp
    else:
        messages.info(request,"Invalid number")
        return redirect('forgotpassword')
    
    return render(request,'otplogin.html',{'phone':phone_number})

def otplogin(request):
    if 'phone' in request.COOKIES:
        phone_number = request.COOKIES['phone']
        return render(request,'otplogin.html',{'phone':phone_number})
    else:
        messages.info(request,"Please try again")
        return redirect('forgotpassword')

def verifylogin(request):
    if request.method=='POST':
        first=request.POST.get('first')
        second=request.POST.get('second')
        third=request.POST.get('third')
        fourth=request.POST.get('fourth')
        number=first+second+third+fourth
        global rotp
        if 'phone' in request.COOKIES:
            x=request.COOKIES['phone']
            print('cccccccccccccccccccc')
            print(type(x))
            print(x)
            user =Accounts.objects.get(phone_number=x)
        if 'otp' in request.session:
            Ootp = request.session['otp']
        if(number==str(Ootp)):
            #print("correct")          
            if user is not None:
               
                login(request,user)
                return redirect('home')            
            else:
                messages.info(request,"Invalid number")
       
                return render(request,'otplogin.html')

        return render(request,'otplogin.html')
    return render(request,'otplogin.html')

def verify(request):
    if request.method=='POST':
        first=request.POST.get('first')
        second=request.POST.get('second')
        third=request.POST.get('third')
        fourth=request.POST.get('fourth')
        number=first+second+third+fourth
        global rotp
        #global user
        #wotp = rotp["otp"]
        wotp =rotp
        Ootp=9999
        if 'otp' in request.session:
            Ootp = request.session['otp']

        if(number==str(Ootp)):
            global referrelG
           
            

            if 'first_name' in request.COOKIES:
                userformed=tempAccount.objects.get(first_name= request.COOKIES['first_name'])
            else:
                messages.info(request,"Please try again")
                return redirect('signup') 

            first_name=userformed.first_name
            last_name=userformed.last_name
            phone_number=userformed.phone_number
            username=userformed.first_name
            email=userformed.email
            password1=userformed.password
            user= Accounts.objects.create_user(first_name=first_name,last_name=last_name,phone_number=phone_number,username=username,email=email,password=password1)
            userformed.delete()

            wallet=Wallet()
            wallet.user=user
            wallet.save()

            referrel=Referrel()
            referrel.user=user 
            x=str(phone_number)
            x=x[-4:]
            
            code = first_name+x
            referrel.code=code
            
            referrel.save()


            if referrelG != "":
                if Referrel.objects.filter(code=referrelG).exists():
                    referlobj=Referrel.objects.get(code=referrelG)
                    walletuser=referlobj.user
                    #if Wallet.objects.filter(user=walletuser).exists():
                    existingwallet=Wallet.objects.get(user=walletuser)
                    existingwallet.amount=existingwallet.amount+50
                    existingwallet.save()


            resp= redirect('login')
            resp.delete_cookie('phone')
            return resp
        else:
            #print('thettipoi')
            messages.info(request,"Incorrect OTP")
            return render(request,'otp.html')

    return redirect('/')

def getotp():
    import random

    # prints a random value from the list
    
    list=range(1000,9999)
    otp=random.choice(list)
    

    account_sid ='AC0c82fc0f46279be5c92de65a35a2a481'
    auth_token = '21816cd3c2fb16d9fb0af0800b9bbc1c'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    body = otp,
    from_ = '+17174936731',
    to    = '+919072863781' 
    )
    print("otp poytind")
    return otp
    #print(message.sid)

def forgotpassword(request):
    return render(request,'forgotpasswordReal.html')

def loggedin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,email=email,password=password)
        if user is None: 
            
            messages.info(request,"Invalid credentials")
        elif user is not None:
            
            if user.is_staff==True:
                login(request,user)
                resp= redirect('home')
                if 'productid' in request.COOKIES:

                    if Products.objects.filter(id=int(request.COOKIES['productid'])).exists():
                        prod=Products.objects.get(id=int(request.COOKIES['productid']))
                        resp.delete_cookie('productid')

                    return pp.productshome(request,prod.category_name.slug,prod.slug)

                    
                return redirect('home')
            else:
                messages.info(request,"Blocked by admin")
    return redirect('login')

def landingpage(request):
    if request.user.is_authenticated:
        
      if request.user.is_admin==False:
         return redirect('store/home')
    
    listofproduct= Products.objects.all()
    alloffers = RealOffers.objects.all()

    context={'listofproducts':listofproduct,'alloffers':alloffers}
    return render(request,'index.html',context)
from django.db.models import Q
def searchG(request):
    keyword= request.GET['search']
    listofproduct=Products.objects.order_by('-created_date').filter(Q(desciption__icontains=keyword)|Q(product_name__icontains=keyword)|Q(subcategory_name__subcategory_name__icontains=keyword))
    alloffers=RealOffers.objects.all()
    context={'listofproducts':listofproduct,'alloffers':alloffers,'guestsearch':True}
    return render(request,'index.html',context)
    
def statusupdate(request):
    orderid=request.POST['orderid']
    statusx=request.POST['statusvalue']
    
    
    order=Orders.objects.get(id=orderid)
    if statusx== "Returned" :
        prod=Products.objects.get(id=order.product.id)
        prod.stock=prod.stock+1
        prod.save()
        

    order=Orders.objects.get(id=orderid)
    order.status=statusx
    order.save()
    return JsonResponse({'status':True})

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated and request.user.is_staff == True: 

        # if 'productid' in request.session:
        #     x=request.session['productid']
        #     print("home ethi  ",x)
        #     prod=Products.objects.get(id=int(x))
            

        listofproduct= Products.objects.all()
        offer=RealOffers.objects.all()
        productcount=listofproduct.count #9
        
        paginator=Paginator(listofproduct,9)
        page=request.GET.get('page')
        pagedproduct=paginator.get_page(page)        
            
        context={'listofproducts':pagedproduct,'productcount':productcount,"inoffer":offer}
        return render(request,'userside/home.html',context)
    else:
        return redirect("landingpage")

def orderdetails(request):
    listofproduct=Orders.objects.all().order_by('-date')
    name= request.user.username
    paginator=Paginator(listofproduct,10)
    page=request.GET.get('page')
    pagedproduct=paginator.get_page(page)
    context={'name':name,'listofproducts':pagedproduct}
    #context={'allorders':pagedproduct,'name':name}
    return render(request,'adminorders.html',context)

def adminlogin(request):
    if request.user.is_authenticated:
      if request.user.is_admin==True:        
        return redirect('adminhome')
      else:
        
        return render(request,'adminlogin.html')
    return render(request,'adminlogin.html')

def adminloggedin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,email=email,password=password)
        if user is not None:

            if user.is_admin==True:
                
                login(request,user)
                return redirect('dashboard')
        else:
            messages.info(request,"Invalid Credentials")            
    return render(request,'admindashboard.html') 

def logout1(request):
    logout(request)
    return redirect("landingpage")

@login_required(login_url='login')
def  adminhome(request):
    if request.user.is_admin==False:
         return redirect("login")

    name= request.user.username
    listofproduct=Accounts.objects.all().order_by('id')
    paginator=Paginator(listofproduct,16)
    page=request.GET.get('page')
    pagedproduct=paginator.get_page(page)
    context={'name':name,'listofproducts':pagedproduct}
    #context={'name':name,'key1':key1}
    return render(request,'admindashboard.html',context)

@login_required(login_url='login')
def createadminuser(request):
    name= request.user.username
    return render(request,'createadmin.html',{'name':name})

@login_required(login_url='login')
def addadminuser(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        phone_number=request.POST.get('phone_number')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2') 
        if email=="" or first_name=="" or last_name=="" or username=="" or password1=="" or password2=="" or phone_number=="":
            messages.info(request,"Require all fields")
            return render(request,'createadmin.html')
        if password1==password2: 
            if Accounts.objects.filter(username=username).exists():
                messages.info(request,"User exist")
               
                name= request.user.username
                return render(request,'createadmin.html',{'name':name})

            elif Accounts.objects.filter(email=email).exists():
                messages.info(request,"Email exist")
                name= request.user.username
                return render(request,'createadmin.html',{'name':name})
            else:
                user= Accounts.objects.create_superuser(first_name=first_name,last_name=last_name,phone_number=phone_number,username=username,email=email,password=password1)
        return redirect('adminhome')
    
    else:
        return redirect('adminhome')

def edit1(request,pk):
   get_data=Accounts.objects.get(id=pk)
   if get_data.is_staff == True:
    get_data.is_staff=False
    get_data.save()
   else:
    get_data.is_staff=True
    get_data.save()
   return redirect(adminhome)

def delete(request,pk):
    get_data=Accounts.objects.get(id=pk)
    get_data.delete()
    return redirect(adminhome)

def error_404_views(request,exception):
    print("RRRRRR")
    return render(request,'404.html')