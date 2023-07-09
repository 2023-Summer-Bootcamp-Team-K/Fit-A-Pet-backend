from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Pet
from .forms import PetForm

def index(request):
    pet_list = Pet.objects.all()
    context = {'pet_list': pet_list}
    return render(request, '', context)

def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.create_date = timezone.now()
            return redirect('pet:index')
    else:
        form = PetForm()
        context = {'form': form}
        return render(request, '', context)
