from django.urls import path, include
from .AgentViews import *

urlpatterns = [
    path("Dashboard/", dashboard, name="agent_dashboard"),
    path("Query/", view_query, name="view_query"),
    path("ResolvedQuery/", view_resolvedquery, name="view_resolvedquery"),
    path("Add/Query/", agent_add_query, name="agent_add_query"),
    path("Product/", agent_product, name="agent_product"),
    path("Product/Details/", agent_product_details, name="agent_product_details"),
    path("Appointment/List/", agent_appointment_list, name="agent_appointment_list"),
    path("Appointment/Grid/", agent_appointment_grid, name="agent_appointment_grid"),
]
