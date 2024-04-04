from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from Eshop.models import Product,Cart,Order
from django.db.models import Q
import random 
import razorpay 

# Create your views here.
def home(request):
    #userid=request.user.id
    #print(userid)
    #print("result :",request.user.is_authenticated)
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    context['products']=p
    return render(request,'index.html',context)
    

def user_login(request):
    context={}
    if request.method=="POST":
        uname=request.POST['suemail']
        upass=request.POST['supass1']
        if uname=="" or upass=="" :
             context['errormsg']="Field cannot be empty"
             return render(request,'index.html',context)
        
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errormsg']="Invalid username and password"
                return render(request,'index.html',context)
    else:
        return render(request,'login.html')
        #print(u.password)
            #return HttpResponse("in else part")
        
        
    

def user_logout(request):
    logout(request)
    return redirect('/home')
   

def register(request):
    context={}
    if request.method=="POST":
        uname=request.POST['suemail']
        upass=request.POST['supass1']
        upassed=request.POST['supass2']
        if uname=="" or upass=="" or upassed=="":
             context['errormsg']="Field cannot be empty"
             return render(request,'register.html',context)
        
        elif upass != upassed:
            context['errormsg']="Password didi not match"
            return render(request,'register.html',context)
        
        else:
            try:
                u=User.objects.create(username=uname,password=upass,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="user created successfully please log in"
                #return HttpResponse("user created successfully")
                return render(request,'register.html',context)
            except Exception:
                context['errormsg']="Username already exist"
                return render(request,'register.html',context)


    else:
        if request.method=='GET':
          return render(request,'register.html')
    

def cart(request):
    return render (request,'cart.html')

def product_details(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'product_details.html',context)



def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print('order id ',oid)
    

    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(c)
    
    for x in c:

        s=s+x.pid.price*x.qty
        context={}
        context['n']=np
        context['products']=c
        context['total']=s
    return render(request,'placeorder.html',context)

def addtocart(request,pid):

    if request.user.is_authenticated:

        userid=request.user.id

        u=User.objects.filter(id=userid)
        print(u[0])

        p=Product.objects.filter(id=pid)
        print(p[0])

        c=Cart.objects.create(uid=u[0],pid=p[0])
        c.save()

        #print(userid)
        #print(pid)
        return HttpResponse("Added")
    
    else:
        return HttpResponse("Error")
    
def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect ('/viewcart')

def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    s=0
    np=len(c)
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price *x.qty
        context={}
        context['n']=np
        context['products']=c
        context['total']=s
    return render(request,'cart.html',context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect("/viewcart")




def range(request):
    min=request.GET['umin']
    max=request.GET['umax']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,abc):
    if abc == '0':
        col = 'price'
    
    else:
        col='-price'

    p=Product.objects.filter(is_active=True).order_by(col)

    context={}
    context['products']=p

    return render(request,"index.html",context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    
    
    for x in orders:

        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_hOWkTFGDgS4Z5V", "aFZDtZhLF29o6S3AE5J0KTel"))

    data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    return render (request,'pay.html',context)




def contact(request):
    return render(request,'contact.html')










