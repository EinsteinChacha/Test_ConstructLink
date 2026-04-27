from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingRequestForm, EquipmentForm, RegisterForm
from .models import BookingRequest, Equipment, EquipmentCategory, User


def home(request):
    featured_equipment = Equipment.objects.select_related('category', 'owner').order_by('-created_date')[:6]
    return render(request, 'mainapp/home.html', {'featured_equipment': featured_equipment})


def how_it_works(request):
    return render(request, 'mainapp/how_it_works.html')


def contact(request):
    return render(request, 'mainapp/contact.html')


def equipment_marketplace(request):
    category_id = request.GET.get('category')
    query = request.GET.get('q', '')
    equipment = Equipment.objects.select_related('category', 'owner').all().order_by('-created_date')
    if category_id:
        equipment = equipment.filter(category_id=category_id)
    if query:
        equipment = equipment.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(region__icontains=query))

    categories = EquipmentCategory.objects.all().order_by('name')
    return render(
        request,
        'mainapp/equipment_marketplace.html',
        {'equipment': equipment, 'categories': categories, 'selected_category': category_id, 'query': query},
    )


def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment.objects.select_related('owner', 'category'), pk=pk)
    can_book = request.user.is_authenticated and request.user != equipment.owner
    if request.method == 'POST' and can_book:
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.equipment = equipment
            booking.requested_by = request.user
            booking.save()
            messages.success(request, 'Booking request submitted successfully.')
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = BookingRequestForm()

    return render(request, 'mainapp/equipment_detail.html', {'equipment': equipment, 'form': form, 'can_book': can_book})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard_redirect(request):
    if request.user.account_type == User.AccountType.EQUIPMENT_OWNER:
        return redirect('equipment_owner_dashboard')
    if request.user.account_type == User.AccountType.CONTRACTOR:
        return redirect('contractor_dashboard')
    if request.user.account_type == User.AccountType.DRIVER:
        return redirect('driver_dashboard')
    if request.user.account_type == User.AccountType.LOGISTICS_PARTNER:
        return redirect('logistics_partner_dashboard')
    if request.user.account_type == User.AccountType.CONSTRUCTION_COMPANY:
        return redirect('construction_company_dashboard')
    return redirect('individual_client_dashboard')


@login_required
def equipment_owner_dashboard(request):
    my_equipment = Equipment.objects.filter(owner=request.user).order_by('-created_date')
    booking_requests = BookingRequest.objects.filter(equipment__owner=request.user).select_related('equipment', 'requested_by')
    return render(
        request,
        'mainapp/dashboards/equipment_owner_dashboard.html',
        {'my_equipment': my_equipment, 'booking_requests': booking_requests},
    )


@login_required
def contractor_dashboard(request):
    available_equipment = Equipment.objects.filter(availability_status=Equipment.AvailabilityStatus.AVAILABLE).select_related('category', 'owner')
    my_requests = BookingRequest.objects.filter(requested_by=request.user).select_related('equipment')
    return render(
        request,
        'mainapp/dashboards/contractor_dashboard.html',
        {'available_equipment': available_equipment, 'my_requests': my_requests},
    )


@login_required
def generic_dashboard(request, title):
    my_requests = BookingRequest.objects.filter(requested_by=request.user).select_related('equipment')
    return render(request, 'mainapp/dashboards/generic_dashboard.html', {'dashboard_title': title, 'my_requests': my_requests})


@login_required
def add_equipment(request):
    if request.user.account_type != User.AccountType.EQUIPMENT_OWNER:
        messages.error(request, 'Only equipment owners can add equipment.')
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.owner = request.user
            equipment.save()
            messages.success(request, 'Equipment added successfully.')
            return redirect('equipment_owner_dashboard')
    else:
        form = EquipmentForm()

    return render(request, 'mainapp/add_equipment.html', {'form': form})


@login_required
def driver_dashboard(request):
    return generic_dashboard(request, 'Driver Dashboard')

@login_required
def logistics_partner_dashboard(request):
    return generic_dashboard(request, 'Logistics Partner Dashboard')

@login_required
def construction_company_dashboard(request):
    return generic_dashboard(request, 'Construction Company Dashboard')

@login_required
def individual_client_dashboard(request):
    return generic_dashboard(request, 'Individual Client Dashboard')
