from django.shortcuts import render, redirect, HttpResponse
from .forms import MyForm
from urllib.parse import urlencode
from django.urls import reverse

def main(request):

    f = MyForm(initial={'last_name': 'Васечкин'})
    if request.method == 'POST':
        print(request.POST)
        f = MyForm(request.POST)
        if f.is_valid():
            first_name = request.POST['first_name']
            last_name = request.POST.get('last_name', '')

            user = {
                'first_name': first_name,
                'last_name': last_name
            }
            base_url = reverse('success')
            params = urlencode(user)
            return redirect(f'{base_url}?{params}')
        
    return render(request, 'mathem/main.html', context={'form': f})

def hello(request):
    first_name =  request.GET.get('first_name', '12')
    last_name = request.GET.get('last_name', '23')
    return HttpResponse(f'<h1>Hello, { first_name } { last_name }</h1>')