from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


def employee_profile(request):
    return render(request, "Employee/Profile/Profile.html")


def employee_query_list(request):
    return render(request, "Employee/Queries/querieslist.html")


def employee_pending_query(request):
    return render(request, "Employee/Queries/pending_query.html")


def employee_followup_list(request):
    return render(request, "Employee/FollowUp/followup_list.html")


def employee_lead_list(request):
    return render(request, "Employee/Enquiry/lead_list.html")


def employee_lead_grid(request):
    return render(request, "Employee/Enquiry/lead-grid.html")


def employee_lead_details(request):
    return render(request, "Employee/Enquiry/lead-details.html")


def employee_other_details(request):
    return render(request, "Employee/Enquiry/other-details.html")


def employee_product_selection(request):
    return render(request, "Employee/Enquiry/Product-Selection.html")


def employee_lead_documents(request):
    return render(request, "Employee/Enquiry/documents.html")


def employee_enrolled_lead(request):
    return render(request, "Employee/Enquiry/Enrolledleads.html")


def employee_enrolled_grid(request):
    return render(request, "Employee/Enquiry/enroll_lead-grid.html")
