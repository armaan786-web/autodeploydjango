from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect


def dashboard(request):
    return render(request, "Agent/Dashboard/dashboard.html")


def view_query(request):
    return render(request, "Agent/Queries/quries.html")


def view_resolvedquery(request):
    return render(request, "Agent/Queries/resolvedquery.html")


def agent_add_query(request):
    return render(request, "Agent/Queries/add_query.html")


def agent_product(request):
    return render(request, "Agent/Product/product.html")


def agent_product_details(request):
    return render(request, "Agent/Product/Productdetails.html")


def agent_appointment_list(request):
    return render(request, "Agent/Appointment/appointmentlist.html")


def agent_appointment_grid(request):
    return render(request, "Agent/Appointment/appointmentgrid.html")
