from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from Ecomapp.models import Product,Cart
from django.db.models import Q

# Create your views here.

def home(request):
    userdata=request.user.id
    # print('Userdata id:',userdata)
    # print('userdata id:',request.user.is_authenticated)
    obj=Product.objects.filter(is_active=True)
    context={'product':obj}
    return render(request,'index.html',context)

def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        u=request.POST['uname']
        p=request.POST['upass']
        c=request.POST['ucpass']
        uobj=User.objects.create(username=u,email=u)
        uobj.set_password(p)
        uobj.save()
        return redirect('/register')
    
def user_login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        u=request.POST['uname']
        p=request.POST['upass']
        a=authenticate(username=u,password=p)
        if a is not None:
            print(a)
            print(a.password,a.id)
            login(request,a)
            return redirect('/')
        else:
            print(a)
            return HttpResponse('Login Fail')
        
def user_logout(request):
    logout(request)
    return redirect('/')
    
def product_detail(request,pid):
    obj=Product.objects.filter(id=pid)
    context={'product':obj}
    return render(request,'product.html',context)

def addtocart(request,pid):
    userid=request.user.id
    u=User.objects.filter(id=userid)
    p=Product.objects.filter(id=pid)
    c=Cart.objects.create(uid=u[0], pid=p[0], cprice=p[0].price)
    c.save()
    return redirect('/cart')

def cart(request):
    c=Cart.objects.filter(uid=request.user.id)
    s=0
    cnt=0
    for i in c:
        cnt+=1
        s=s+(i.pid.price * i.qty)
    context={'product':c,'total':s,'cnt':cnt}
    print('sum:',s)
    return render(request,'cart.html',context)

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':       
        qty=c[0].qty+1
        c.update(qty=qty) 
        return redirect('/cart')
    elif  c[0].qty>1:
        qty=c[0].qty-1
        c.update(qty=qty)
        return redirect('/cart')
    else:
        return redirect('/cart')
    
def catfilter(request, cv):
    if cv=='1':
        obj=Product.objects.filter(cat=1)
        context={'product':obj}
        return render(request,'index.html',context)
    elif cv=='2':
        obj=Product.objects.filter(cat=2)
        context={'product':obj}
        return render(request,'index.html',context)
    else:
        obj=Product.objects.filter(cat=3)
        context={'product':obj}
        return render(request,'index.html',context)
    
def range(request):
    if request.method=='GET':
        min = request.GET['min']
        max = request.GET['max']

        #select pname from  products price->=min and price->=max 
        c1=Q(price__gte=min)
        c2=Q(price__lte=max)
        obj=Product.objects.filter(c1 & c2)
        context={'product':obj}
        return render(request,'index.html',context)
