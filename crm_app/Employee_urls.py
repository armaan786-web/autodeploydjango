from django.urls import path, include
from .EmployeeViews import *

urlpatterns = [
    path("Profile/", employee_profile, name="employee_profile"),
    path("Query/List/", employee_query_list, name="employee_query_list"),
    path("Pending/Query/", employee_pending_query, name="employee_pending_query"),
    path("FollowUp/List/", employee_followup_list, name="employee_followup_list"),
    path("Lead/List/", employee_lead_list, name="employee_lead_list"),
    path("Lead/Grid/", employee_lead_grid, name="employee_lead_grid"),
    path("Lead/Details/", employee_lead_details, name="employee_lead_details"),
    path("Other/Details", employee_other_details, name="employee_other_details"),
    path(
        "Product/Selection/",
        employee_product_selection,
        name="employee_product_selection",
    ),
    path("Documents/", employee_lead_documents, name="employee_lead_documents"),
    path("Enrollled/Lead/", employee_enrolled_lead, name="employee_enrolled_lead"),
    path("Enrollled/Grid/", employee_enrolled_grid, name="employee_enrolled_grid"),
]
