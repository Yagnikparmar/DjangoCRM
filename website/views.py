from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages #notify login log out message // messages framework
from .forms import SignUpForm,AddRecordForm
from .models import Record
# Create your views here.

def home(request):
    #record
    records = Record.objects.all()
    #check to see if logging in
    if request.method == 'POST':
        username = request.POST['username'] # username name in html file
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username=username, password=password)  #parameter is built in function from  user class
        if user is not None:
            login(request,user)
            messages.success(request,"You have been logged in!") #function calling
            return redirect("home")  
        else:
            messages.success(request,"There Was an error, please try again")
            return redirect("home")
    else:
        return render(request, 'home.html',{'records':records}) #records is key or label and records is value means it is object 

def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username , password = password)
            login(request,user)
            messages.success(request,"You  have successfully registered")
            return redirect('home')
    else:
        form= SignUpForm()
        return render(request,'register.html',{'form':form})
    
    return render(request, 'register.html', {'form':form})

def customer_record(request,pk):
    if request.user.is_authenticated:
        #Look up records
        customer_record = Record.objects.get(id=pk) #get only one pk of them
        return render(request,'record.html',{"customer_record":customer_record})
    else:
        messages.success(request,"You must be logged in to view that page")
        return redirect('home')

def delete_record(request, pk):
    # record = get_object_or_404(Record, id=pk)

    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home') 
 
# def add_record(request):
# 	form = AddRecordForm(request.POST or None)
# 	if request.user.is_authenticated:
# 		if request.method == "POST":
# 			if form.is_valid():
# 				add_record = form.save()
# 				messages.success(request, "Record Added...")
# 				return redirect('home')
# 		return render(request, 'add_record.html', {'form':form})
# 	else:
# 		messages.success(request, "You Must Be Logged In...")
# 		return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user  # Assign the logged-in user to the record
                record.save()
                messages.success(request, "Record Added Successfully.")
                return redirect('home')
        return render(request, 'adds_record.html', {'form': form})
    else:
         messages.error(request, "You must be logged in to add a record.")
         return redirect('home')
    
def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')