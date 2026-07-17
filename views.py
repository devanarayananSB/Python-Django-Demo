from django.shortcuts import render,redirect
from.models import*
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout


# Create your views here.

def index (request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def register_action(request):
    if request.method=='POST':
        username=request.POST.get("username")
    data = {
        'username_exists': Login.objects.filter(username=username).exists(),
            'error':"Username Already Exist"
    }
    if(data["username_exists"]==False):
        ob=Login()
        ob.username=request.POST.get('username')
        ob.password=request.POST.get('password')
        ob.usertype='user'
        ob.status='approved'
        ob.save()
        obj=UserInfo()
        obj.name=request.POST.get("name")
        obj.address=request.POST.get("address")
        obj.email=request.POST.get("email")
        obj.phone_number=request.POST.get("phone")
        obj.login=ob
        obj.save()
        messages.success(request,'Registered Scuccessfully')
        return redirect('register')
    else:
        messages.add_message(request,messages.INFO, 'User name is already Exist.Sorry Registration Failed.')
        return redirect('register')
    
def login(request):
    return render(request,'login.html')

def login_action(request):
    u=request.POST.get("username")
    p=request.POST.get("password")
    obj = authenticate(username=u,password=p)
    if obj is not None:
        if obj.is_superuser == 1:
            request.session['aname'] = u
            request.session['slogid'] = obj.id
            return redirect('admin_home')
        else:
         messages.add_message(request,messages.INFO,
                              'Invalid User. ')
         return redirect('login')
    else:
        try:
            obj1 = Login.objects.get(username=u, password=p)
            if obj1.usertype == "user":
                if obj1.status == "approved":
                    request.session['uname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('user_home')
                elif obj1.status == "Not Approved":
                    messages.add_message(request,messages.INFO,'Waiting For Approval.')
                    return redirect('login')
                else:
                    messages.add_message(request,messages.INFO,'Invalid User.')
                    return redirect('login')
          
            else:
                messages.add_message(request,messages.INFO,'Invalid User.')
                return redirect('login')
        
        except Login.DoesNotExist:
            messages.add_message(request,messages.INFO,'Invalid User.')
            return redirect('login')
        

def admin_home(request):
    if 'aname'in request.session:
        return render(request,'master/index.html')
    else:
        return redirect('login')

def user_list(request):
    if 'aname'in request.session:
        users=UserInfo.objects.all()
        return render(request,'master/user_list.html',{'users':users})
    else:
        return redirect('login')

def add_book(request):
    if 'aname' in request.session:
        if request.method == 'POST':
            obj=Book()
            obj.bookname=request.POST.get("bookname")
            obj.author=request.POST.get("author")
            obj.description=request.POST.get("description")
            obj.price=request.POST.get("price")      
            obj.photo=request.FILES.get("photo")
            obj.save()
            messages.add_message(request,messages.INFO,
            'Books added Successfully')
            return redirect('add_book')      
        return render(request,'master/addbook.html')      
    else:
        return redirect('login')
    
def book_list(request):
    if 'aname'in request.session:
        data=Book.objects.all()
        return render(request,'master/booklist.html',{'books':data})
    else:
        return redirect('login')

def delete_book(request,id):
    if 'aname'in request.session:
        data=Book.objects.get(id=id)
        data.delete()
        messages.add_message(request,messages.INFO,
            'Books Deleted Successfully')
        return redirect('book_list')
    else:
        return redirect('login')
#   edit book  
def edit_book(request,id):
    if 'aname' in request.session:
        if request.method == 'POST':
            obj=Book.objects.get(id=id)
            obj.bookname=request.POST.get("bookname")
            obj.author=request.POST.get("author")
            obj.description=request.POST.get("description")
            obj.price=request.POST.get("price") 
            if request.FILES.get('photo'):     
                obj.photo=request.FILES.get("photo")
            obj.save()
            messages.add_message(request,messages.INFO,
            'Books Updated Successfully')
            return redirect('book_list') 
        data=Book.objects.get(id=id)     
        return render(request,'master/edit_book.html',{'data':data})      
    else:
        return redirect('login')

def common_logout(request):
    logout(request)
    request.session.delete()
    return redirect('login')

def user_home(request):
    if 'uname'in request.session:
        books=Book.objects.count()
        return render(request,'user/index.html',{'books':books})
    else:
        return redirect('login')
    
def profile(request):
    if 'uname'in request.session:
        # data=UserInfo.objects.get(login_id=request.session['slogid'])
        data=UserInfo.objects.select_related('login').get(login_id=request.session['slogid'])
        return render(request,'user/profile.html',{'data':data})
    else:
        return redirect('login')    
    
def edit_profile(request):
    if 'uname'in request.session:
        data=UserInfo.objects.get(login_id=request.session['slogid'])
        if request.method=='POST':
            data.name=request.POST.get('name')
            data.address=request.POST.get('address')
            data.email=request.POST.get('email')
            data.phonr_number=request.POST.get('phone')
            data.save()
            messages.add_message(request,messages.INFO,
            'Profile Updated Successfully')
            return redirect('profile')
        return render(request,'user/edit_profile.html',{'data':data})
    else:
        return redirect('login')
    
def view_books(request):
    if 'uname'in request.session:
        data=Book.objects.all()
        return render(request,'user/booklist.html',{'books':data})
    else:
        return redirect('login')
    
def more_details(request,id):
    if 'uname'in request.session:
        data=Book.objects.get(id=id)
        return render(request,'user/moredetails.html',{'book':data})
    else:
        return redirect('login')
