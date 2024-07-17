from django.shortcuts import render,HttpResponse,redirect
from gamestopapp.forms import AddProductForm, UpdateProductForm, UserRegisterForm, UserLoginForm
from gamestopapp.models import Product ,Cart, Orders ,Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection,EmailMessage,send_mail
from django.conf import settings
import random 
import razorpay

# Create your views here.

def index(request):
    return render(request,'index.html')

@login_required(login_url = '/login') 

def createProduct(request):

    if request.method == "GET":
        form = AddProductForm()
        context = {'form':form}

        return render(request,'addproduct.html',context)

    else:
        form = AddProductForm(request.POST,request.FILES)

        if form.is_valid():

            form.save()

           # return HttpResponse('Product saved')
            return redirect('/products/view')

        else:

            context = {'error':'Product not saved'}

            return render(request,'addproduct.html',context)

def readProduct(request):

    prod = Product.objects.filter(isAvailable = True)     # it will show only when checkbox is ticked
    context = {'data':prod}                                # Product.objects.all()
    return render(request,'showproduct.html',context)

def productDetails(request,rid):

    product = Product.objects.filter(id = rid)
    prod = Product.objects.get(id = rid)
    review = Review.objects.filter(product = prod)
    rating = 0
    n=0

    for x in review:
        
        rating += x.rating
        n += 1
    avg_rating = int(rating/n)
    context = {'data':product}
    context['rating'] = avg_rating
    return render(request,'productdetails.html',context)
    
def updateProduct(request,rid): 
    if request.method == "GET":

        prod = Product.objects.get(id = rid)
        form = UpdateProductForm()

        form.fields['name'].initial = prod.name
        form.fields['description'].initial = prod.description
        form.fields['manufacturer'].initial = prod.manufacturer
        form.fields['price'].initial = prod.price
        form.fields['category'].initial = prod.category
        form.fields['isAvailable'].initial = prod.isAvailable
        form.fields['image'].initial = prod.image

        context = {'form':form}

        return render(request,'updateproduct.html',context)

    else:

        prod = Product.objects.get(id = rid)

        form = UpdateProductForm(request.POST,request.FILES,instance = prod)

        if form.is_valid():

            form.save()

            return redirect('/products/view')

        else:

            return HttpResponse('Products not saved')


def deleteProduct(request,rid):

    prod = Product.objects.filter(id = rid)
    prod.delete()
    return redirect('/products/view')

def userRegister(request):
    if request.method == "GET":
        form = UserRegisterForm()
        context = {'form':form}
        return render(request,'register.html',context)

    else:

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            password = form.cleaned_data['password']
            confirmPassword = form.cleaned_data['confirmPassword']
            #it just takes the content in the variable to compare it

            if password == confirmPassword:

                user = form.save(commit = False) # purpose of commit is that the data dosen't get saved
                                                 # in data base ,only in user variable
                user.set_password(password) # this statement sets password in star/hash format
                
                user.save()                 # this statement saves data in database
                
                return redirect('/')

        else:

            return HttpResponse('form not saved')


def userLogin(request):

    if request.method == "GET":
        form = UserLoginForm()

        context = {'form':form}

        return render(request,'login.html',context)

    else:

        form = UserLoginForm(request.POST)

        if form.is_valid():


            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username = username,password = password)

            if user is not None:

                login(request,user)

                return redirect('/')

            else: 
                HttpResponse('username password incorrect')


        else:

            return HttpResponse("form not valid")


def userLogout(request):

    logout(request)

    return redirect('/')

@login_required(login_url='/login')
def readUser(request):

    user = User.objects.filter()     
    context = {'data':user}
    return render(request,'showusers.html',context)


def updateUser(request,rid):

    if request.method == "GET":
        user = User.objects.filter(id = rid)

        context = {'data':user}

        return render(request,'updateuser.html',context)

    else:

        user = User.objects.filter(id = rid)
    
        username = request.POST['username']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        isSuperuser = request.POST['is_superuser']
        isStaff = request.POST['is_staff']

        

        user.update(username = username, first_name = firstname, last_name = lastname, email = email, is_superuser = isSuperuser,is_staff = isStaff)

        return redirect('/users/view')

@login_required(login_url='/login')

def add_to_cart(request,rid):
    #user = user.objects.filter(id=request.user)

    product = Product.objects.get(id = rid)

    data = Cart.objects.filter(user = request.user,product = product).exists() 
    #check whether it is in the db or not exists() gives true false
    # the user cannot enter the same product again 

    if data:
        
        return redirect('/cart')

    else:

        price = product.price

        cart = Cart.objects.create(user = request.user,product = product, price = price)
        # user = request.user it gives specific user can't add same product

        cart.save()

        # return HttpResponse("Hello")

        return redirect('/cart')


def cart(request):

    cart = Cart.objects.filter(user = request.user)

    total_price = 0

    for x in cart:
        total_price  += x.price

    context = {'data': cart}
    context['total_price'] = total_price

    return render(request, 'cart.html',context)



def removeCart(request,rid):

    data = Cart.objects.filter(id = rid)

    data.delete()

    return redirect('/cart') 


def updateCart(request,cid,rid):    #quantity=cid

    data = Cart.objects.filter(id = rid)

    c = Cart.objects.get(id = rid)

    price = c.product.price * float(cid) # we took product bec product price is constant

    data.update(quantity = cid, price = price) 

    return redirect('/cart')


def add_to_order(request):

    data = Cart.objects.filter(user = request.user)

    total_price = 0

    for x in data:

        product = x.product
        quantity = x.quantity
        price = x.price

        total_price += x.price

        order = Orders.objects.create(user = request.user,product = product, quantity = quantity,price = price)

        order.save()

    client = razorpay.Client(auth=(settings.KEY_ID,settings.KEY_SECRET))
    payment = client.order.create({'amount':int(total_price*100),'currency':'INR','payment_capture':1})

    print(payment)

    context = {'data':payment}
    context['amount'] = int(total_price*100)

    data.delete()

    #return HttpResponse("your orders")
    #return redirect('/orders')
    return render(request,'payment.html',context)


def show_orders(request):

    data = Orders.objects.filter(user = request.user)

    context = {'data':data}

    return render(request,'orders.html',context)


def add_review(request,rid):

    product = Product.objects.get(id = rid)

    review = Review.objects.filter(product = product,user = request.user).exists()

    if review:

        return HttpResponse("review already exists")

    else:

        if request.method == "GET":
            return render(request,'addreview.html')

        else:

            rating = request.POST['rate']
            image = request.FILES['image']
            review = request.POST['review']

            r = Review.objects.create(user = request.user,product = product,rating = rating, image = image, review = review)

            r.save()

            # return HttpResponse("data saved")
            return redirect('/products/details/' + rid)


def forgot_password(request):
    if request.method == "GET":

        return render(request,'emailreturn.html')

    else:

        email = request.POST['email']

        request.session['email'] = email

        user = User.objects.filter(email = email).exists()

        if user:

            otp = random.randint(1000,9999)

            request.session['email_otp'] = otp



            with get_connection(

                host = settings.EMAIL_HOST,
                port = settings.EMAIL_PORT,
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,
                use_tls = settings.EMAIL_USE_TLS
            ) as connection:

                subject = "OTP Verification"
                email_from = settings.EMAIL_HOST_USER
                recipetion_list = [ email ]
                message = f"OTP is {otp}"

            EmailMessage(subject,message,email_from, recipetion_list,connection = connection).send()

            # return HttpResponse("Email Send")
            return redirect('/verify_otp')
 
        else:

            return HttpResponse("user not registered")

   
def verify_otp(request):

    if request.method == "GET":

        return render(request,'otpverification.html')

    else:
        user_otp = int(request.POST['otp'])

        email_otp = int(request.session['email_otp'])

        if user_otp == email_otp:

            return redirect('/change_password')

                # print("user otp:",user_otp)
               # print("email otp:",email_otp)

                # return HttpResponse('ok')
        else:

            return redirect('/forgot_password')



def change_password(request):

    if request.method == "GET":

        return render(request,'newpassword.html')

    else:

        email = request.session['email']

        password = request.POST['password']

        confirmPassword = request.POST['confirmpassword']

        if password == confirmPassword:

            user = User.objects.get(email = email)

            user.set_password(password)

            user.save()

            return redirect('/login')
            #return HttpResponse("Password changed")

        else:

            return httpResponse("password and confirm Password does not match")






    





    