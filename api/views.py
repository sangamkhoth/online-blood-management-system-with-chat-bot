from rest_framework import viewsets
from users.models import User
from core.models import Donor, Hospital, BloodInventory
from .serializers import UserSerializer, DonorSerializer, HospitalSerializer, BloodInventorySerializer

from django.shortcuts import render

def api_dashboard(request):
    return render(request, 'api/api_dashboard.html')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class BloodInventoryViewSet(viewsets.ModelViewSet):
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Hospital, Donor
from .forms import HospitalForm, DonorForm

# Hospitals
@login_required(login_url='/accounts/login/')
def hospitals_list(request):
    q = request.GET.get('q', '').strip()
    city = request.GET.get('city', '').strip()
    qs = Hospital.objects.all().order_by('-created_at')
    if q:
        qs = qs.filter(name__icontains=q)
    if city:
        qs = qs.filter(city__icontains=city)
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    hospitals = paginator.get_page(page)
    return render(request, 'api/hospitals_list.html', {'hospitals': hospitals, 'q': q, 'city': city})

@login_required(login_url='/accounts/login/')
def hospital_create(request):
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hospitals_list')
    else:
        form = HospitalForm()
    return render(request, 'api/hospital_form.html', {'form': form})

@login_required(login_url='/accounts/login/')
def hospital_edit(request, pk):
    obj = get_object_or_404(Hospital, pk=pk)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('hospitals_list')
    else:
        form = HospitalForm(instance=obj)
    return render(request, 'api/hospital_form.html', {'form': form, 'edit': True})

@login_required(login_url='/accounts/login/')
def hospital_delete(request, pk):
    obj = get_object_or_404(Hospital, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('hospitals_list')
    return render(request, 'api/confirm_delete.html', {'object': obj, 'type': 'Hospital'})

# Donors
@login_required(login_url='/accounts/login/')
def donors_list(request):
    q = request.GET.get('q', '').strip()
    bg = request.GET.get('blood_group', '').strip()
    city = request.GET.get('city', '').strip()
    qs = Donor.objects.all().order_by('-created_at')
    if q:
        qs = qs.filter(name__icontains=q)
    if bg:
        qs = qs.filter(blood_group__iexact=bg)
    if city:
        qs = qs.filter(city__icontains=city)
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    donors = paginator.get_page(page)
    return render(request, 'api/donors_list.html', {'donors': donors, 'q': q, 'bg': bg, 'city': city})

@login_required(login_url='/accounts/login/')
def donor_create(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('donors_list')
    else:
        form = DonorForm()
    return render(request, 'api/donor_form.html', {'form': form})

@login_required(login_url='/accounts/login/')
def donor_edit(request, pk):
    obj = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('donors_list')
    else:
        form = DonorForm(instance=obj)
    return render(request, 'api/donor_form.html', {'form': form, 'edit': True})

@login_required(login_url='/accounts/login/')
def donor_delete(request, pk):
    obj = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('donors_list')
    return render(request, 'api/confirm_delete.html', {'object': obj, 'type': 'Donor'})
