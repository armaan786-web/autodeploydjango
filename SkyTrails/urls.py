from django.contrib import admin
from django.urls import path, include
from crm_app import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import re_path
from crm_app.API_views import *


urlpatterns = (
    [
        re_path("media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
        re_path("static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
        path("admin/", admin.site.urls),
        path("Signup/", views.agent_signup, name="agent_signup"),
        path("", views.CustomLoginView, name="login"),
        path("OTP/", views.verify_otp, name="verify_otp"),
        path("ResendOTP/", views.resend_otp, name="resend_otp"),
        path("forgot/Password", views.forgot_psw, name="forgot_psw"),
        path("Forget/Verify/OTP/", views.forget_otp, name="forget_otp"),
        path("ResetPassword/", views.reset_psw, name="reset_psw"),
        path("Admin/", include("crm_app.Admin_urls")),
        path("Agent/", include("crm_app.Agent_urls")),
        path("Employee/", include("crm_app.Employee_urls")),
        ########################## API URLS ##############################################
        path(
            "enquiry_form/",
            BookingViewSet.as_view({"get": "list", "post": "create"}),
            name="enquiry",
        ),
        path("FrontWebsite/", FrontWebsite.as_view({"get": "list", "post": "create"})),
        path("Api/VisaCountry/", apiVisaCountry.as_view({"get": "list"})),
        path("Api/VisaCategory/", apiVisaCategory.as_view({"get": "list"})),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
