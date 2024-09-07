from django.shortcuts import render, redirect



def choose_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        request.session['role'] = role
        return redirect('register')
    return render(request, 'home/choose_role.html')


