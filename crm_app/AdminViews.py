from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import *
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.views import View
from django.urls import reverse_lazy
import pandas as pd
from .whatsapp_api import send_whatsapp_message
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Prefetch
import requests
######################################### COUNTRY #################################################


def admin_dashboard(request):
    return render(request, "Admin/Dashboard/dashboard.html")


def admin_profile(request):
    return render(request, "Admin/Profile/profile.html")


def add_visacountry(request):
    visacountry = VisaCountry.objects.all().order_by("-id")
    form = VisaCountryForm(request.POST or None)

    if form.is_valid():
        country_name = form.cleaned_data["country"]
        if VisaCountry.objects.filter(country__iexact=country_name).exists():
            messages.error(request, "This country already exists.")
        else:
            form.save()
            messages.success(request, "Visa Country added successfully")
            return HttpResponseRedirect(reverse("add_visacountry"))

    context = {"form": form, "visacountry": visacountry}
    return render(request, "Admin/mastermodule/VisaCountry/VisaCountry.html", context)


def visacountryupdate_view(request):
    if request.method == "POST":
        visa_country = request.POST.get("visa_country_id")
        visa_country_name = request.POST.get("visa_country_name")

        visa_Country_id = VisaCountry.objects.get(id=visa_country)
        visa_Country_id.country = visa_country_name.capitalize()

        visa_Country_id.save()
        messages.success(request, "Visa Country Updated successfully")
        return HttpResponseRedirect(reverse("add_visacountry"))


def import_country(request):
    if request.method == "POST":
        file = request.FILES["file"]
        path = str(file)

        try:
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                country_name = row["countryname"].capitalize()

                visa_country, created = VisaCountry.objects.get_or_create(
                    country=country_name
                )

                if created:
                    visa_country.save()

            messages.success(request, "Data Imported Successfully!!")

        except Exception as e:
            messages.warning(request, e)
            return redirect("add_visacountry")
    return redirect("add_visacountry")


def delete_visa_country(request, id):
    visacountry_id = VisaCountry.objects.get(id=id)
    visacountry_id.delete()
    messages.success(request, f"{visacountry_id.country} deleted successfully..")
    return HttpResponseRedirect(reverse("add_visacountry"))


######################################### CATEGORY #################################################


def add_visacategory(request):
    visacategory = VisaCategory.objects.all().order_by("-id")
    country = VisaCountry.objects.all()
    form = VisaCategoryForm(request.POST or None)

    if request.method == "POST":
        form = VisaCategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            subcategory = form.cleaned_data["subcategory"]
            visa_country_id = form.cleaned_data["visa_country_id"]

            if VisaCategory.objects.filter(
                Q(
                    category__iexact=category,
                    subcategory__iexact=subcategory,
                    visa_country_id=visa_country_id,
                )
                | Q(
                    category__iexact=category,
                    subcategory__iexact=subcategory,
                    visa_country_id__isnull=True,
                )
            ).exists():
                messages.error(
                    request,
                    "Category/Subcategory already exists for the selected country.",
                )
            else:
                form.save()
                messages.success(
                    request, "Visa Category/SubCategory Added Successfully"
                )
                return HttpResponseRedirect(reverse("add_visacategory"))

    context = {"form": form, "visacategory": visacategory, "country": country}
    return render(request, "Admin/mastermodule/VisaCategory/VisaCategory.html", context)


def visacategoryupdate_view(request):
    if request.method == "POST":
        visa_country_id = request.POST.get("visa_contry_id")
        visa_category_name = request.POST.get("visa_category")
        visa_subcategory = request.POST.get("visa_subcategory_id")
        visa_category_id = request.POST.get("visa_category_id")

        visa_country = VisaCountry.objects.get(id=visa_country_id)
        visa_category = VisaCategory.objects.get(id=visa_category_id)

        visa_category.visa_country_id = visa_country
        visa_category.category = visa_category_name
        visa_category.subcategory = visa_subcategory

        visa_category.save()
        messages.success(request, "Visa Category Updated successfully")
        return HttpResponseRedirect(reverse("add_visacategory"))


def delete_category(request, id):
    category = get_object_or_404(VisaCategory, id=id)
    category.delete()
    messages.success(request, f"{category.category} deleted successfully..")
    return redirect("add_visacategory")


######################################### DOCUMENT CATEGORY ############################################


def add_documentcategory(request):
    documentcategory = DocumentCategory.objects.all().order_by("-id")
    form = DocumentCategoryForm(request.POST or None)

    if form.is_valid():
        Document_category = form.cleaned_data["Document_category"]
        if DocumentCategory.objects.filter(
            Document_category__iexact=Document_category
        ).exists():
            messages.error(request, "This Document Category already exists.")
        else:
            form.save()
            messages.success(request, "Document Category added successfully")
            return HttpResponseRedirect(reverse("add_documentcategory"))

    context = {"form": form, "documentcategory": documentcategory}
    return render(
        request, "Admin/mastermodule/DocumentCategory/DocumentCategory.html", context
    )


def documentcategoryupdate_view(request):
    if request.method == "POST":
        document_category = request.POST.get("document_category_id")
        document_category_name = request.POST.get("document_category_name")

        document_category_id = DocumentCategory.objects.get(id=document_category)
        document_category_id.Document_category = document_category_name.capitalize()

        document_category_id.save()
        messages.success(request, "Document Category Updated successfully")
        return HttpResponseRedirect(reverse("add_documentcategory"))


def delete_documentcategory(request, id):
    documentcategory = get_object_or_404(DocumentCategory, id=id)
    documentcategory.delete()
    messages.success(
        request, f"{documentcategory.Document_category} deleted successfully.."
    )
    return redirect("add_documentcategory")


######################################### DOCUMENT  #################################################


def add_document(request):
    document = Document.objects.all().order_by("-id")
    documentcategory = DocumentCategory.objects.all()
    form = DocumentForm(request.POST or None)

    if form.is_valid():
        document_name = form.cleaned_data["document_name"]
        if Document.objects.filter(document_name__iexact=document_name).exists():
            messages.error(request, "This Document already exists.")
        else:
            form.save()
            messages.success(request, "Document added successfully")
            return HttpResponseRedirect(reverse("add_document"))

    context = {"form": form, "document": document, "documentcategory": documentcategory}
    return render(request, "Admin/mastermodule/Document/Document.html", context)


def documentupdate_view(request):
    if request.method == "POST":
        document_category_id = request.POST.get("document_category_id")
        document_name = request.POST.get("document_name")
        document_size = request.POST.get("document_size")
        document_name_id = request.POST.get("document_name_id")

        document_category = DocumentCategory.objects.get(id=document_category_id)
        document = Document.objects.get(id=document_name_id)

        document.document_category_id = document_category
        document.document_name = document_name
        document.document_size = document_size

        document.save()
        messages.success(request, "Document Updated successfully")
        return HttpResponseRedirect(reverse("add_document"))


def delete_document(request, id):
    document = get_object_or_404(Document, id=id)
    document.delete()
    messages.success(request, f"{document.document_name} deleted successfully..")
    return redirect("add_document")


################################# CASE CATEGORY DOCUMENT #########################################


class CaseCategoryDocumentCreateView(CreateView):
    model = CaseCategoryDocument
    form_class = CaseCategoryDocumentForm

    template_name = (
        "Admin/mastermodule/CaseCategoryDocument/addcasecategorydocument.html"
    )
    success_url = reverse_lazy("CaseCategoryDocument_list")

    def form_valid(self, form):
        instance = form.save(commit=False)

        instance.last_updated_by = self.request.user
        instance.save()

        messages.success(self.request, "CaseCategoryDocument Added Successfully.")

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Country Document Already exist.")
        return super().form_invalid(form)


class CaseCategoryDocumentListView(ListView):
    model = CaseCategoryDocument
    template_name = (
        "Admin/mastermodule/CaseCategoryDocument/casecategorydocumentlist.html"
    )
    context_object_name = "CaseCategoryDocument"

    def get_queryset(self):
        return CaseCategoryDocument.objects.order_by("-id")


class editCaseCategoryDocument(UpdateView):
    model = CaseCategoryDocument
    form_class = CaseCategoryDocumentForm
    template_name = (
        "Admin/mastermodule/CaseCategoryDocument/editcasecategorydocument.html"
    )
    success_url = reverse_lazy("CaseCategoryDocument_list")

    def form_valid(self, form):
        form.instance.lastupdated_by = self.request.user

        # Display a success message
        messages.success(self.request, "CaseCategoryDocument Updated Successfully.")

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Country Document Already exist.")
        return super().form_invalid(form)


def delete_casecategorydocument(request, id):
    casecategorydocument = get_object_or_404(CaseCategoryDocument, id=id)
    casecategorydocument.delete()
    messages.success(request, f"{casecategorydocument.document} deleted successfully..")
    return redirect("CaseCategoryDocument_list")


######################################### BRANCH #################################################


def add_branch(request):
    branch = Branch.objects.all().order_by("-id")
    form = BranchForm(request.POST or None)

    if form.is_valid():
        # Check for duplicate entry before saving
        branch_name = form.cleaned_data["branch_name"]
        if Branch.objects.filter(branch_name__iexact=branch_name).exists():
            messages.error(request, "This Branch already exists.")
        else:
            form.save()
            messages.success(request, "Branch added successfully")
            return HttpResponseRedirect(reverse("add_branch"))

    context = {"form": form, "branch": branch}
    return render(request, "Admin/mastermodule/Branch/BranchList.html", context)


def branchupdate_view(request):
    if request.method == "POST":
        branch_name = request.POST.get("branch_name")
        branch_source = request.POST.get("branch_source")
        branch_name_id = request.POST.get("branch_name_id")

        branch = Branch.objects.get(id=branch_name_id)

        branch.branch_name = branch_name
        branch.branch_source = branch_source

        branch.save()
        messages.success(request, "Branch Updated successfully")
        return HttpResponseRedirect(reverse("add_branch"))


def delete_branch(request, id):
    branch = get_object_or_404(Branch, id=id)
    branch.delete()
    messages.success(request, f"{branch.branch_name} deleted successfully..")
    return redirect("add_branch")


######################################### GROUP #################################################


class CreateGroupView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = "Admin/mastermodule/Manage Groups/addgroup.html"  # Update with your template name
    success_url = reverse_lazy("Group_list")

    def form_valid(self, form):
        # Set the lastupdated_by field to the current user's username
        # form.instance.create_by = self.request.user

        # Display a success message
        messages.success(self.request, "Group Added Successfully.")

        return super().form_valid(form)


class GroupListView(ListView):
    model = Group
    template_name = "Admin/mastermodule/Manage Groups/grouplist.html"
    context_object_name = "group"

    def get_queryset(self):
        return Group.objects.order_by("-id")


class editGroup(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "Admin/mastermodule/Manage Groups/updategroup.html"
    success_url = reverse_lazy("Group_list")

    def form_valid(self, form):
        # Set the lastupdated_by field to the current user's username
        # form.instance.lastupdated_by = self.request.user

        # Display a success message
        messages.success(self.request, "Group Updated Successfully.")

        return super().form_valid(form)


def delete_group(request, id):
    group = get_object_or_404(Group, id=id)
    group.delete()
    messages.success(request, f"{group.group_name} deleted successfully..")
    return redirect("Group_list")


######################################### COURIER #################################################
# -------------------------------------- Test -------------------------------------
class PersonalDetailsView(CreateView):
    def get(self, request):
        form = CompanyCourierDetailsForm()
        return render(
            request,
            "Admin/mastermodule/CourierDetails/companydetails.html",
            {"form": form},
        )

    def post(self, request):
        form = CompanyCourierDetailsForm(request.POST)
        if form.is_valid():
            # Save personal details to session or another storage mechanism
            request.session["personal_details"] = form.cleaned_data
            return redirect("receiver_details")

        return render(
            request,
            "Admin/mastermodule/CourierDetails/otherdetails.html",
            {"form": form},
        )


class ReceiverDetailsView(CreateView):
    def get(self, request):
        form = ReceiverDetailsForm()
        return render(
            request,
            "Admin/mastermodule/CourierDetails/otherdetails.html",
            {"form": form},
        )

    def post(self, request):
        form = ReceiverDetailsForm(request.POST)
        if form.is_valid():
            # Retrieve personal details from session
            personal_details = request.session.get("personal_details", {})

            # Merge personal details with receiver details
            merged_data = {**personal_details, **form.cleaned_data}

            # Save the merged data to the database
            courier_address = CourierAddress(**merged_data)
            courier_address.save()
            messages.success(request, "Courier Address added successfully")

            return redirect("viewcourieraddress_list")

        return render(
            request,
            "Admin/mastermodule/CourierDetails/otherdetails.html",
            {"form": form},
        )


# -------------------------------------- Test -------------------------------------


def viewcourieraddress_list(request):
    courier_addss = CourierAddress.objects.all().order_by("-id")
    context = {"courier_addss": courier_addss}
    return render(
        request, "Admin/mastermodule/CourierDetails/Courierdetail.html", context
    )


class UpdateCompanyDetailsView(View):
    template_name = "Admin/mastermodule/CourierDetails/editcompanydetails.html"

    def get(self, request, id):
        courier_address = CourierAddress.objects.get(id=id)
        company_form = CompanyCourierDetailsForm(instance=courier_address)
        return render(
            request,
            self.template_name,
            {"company_form": company_form, "courier_address": courier_address},
        )

    def post(self, request, id):
        courier_address = CourierAddress.objects.get(id=id)
        company_form = CompanyCourierDetailsForm(request.POST, instance=courier_address)
        if company_form.is_valid():
            company_form.save()
            return redirect("update_receiver_details", id=id)
        return render(
            request,
            self.template_name,
            {"company_form": company_form, "courier_address": courier_address},
        )


class UpdateReceiverDetailsView(View):
    template_name = "Admin/mastermodule/CourierDetails/editotherdetails.html"

    def get(self, request, id):
        courier_address = CourierAddress.objects.get(id=id)
        receiver_form = ReceiverDetailsForm(instance=courier_address)
        return render(
            request,
            self.template_name,
            {"receiver_form": receiver_form, "courier_address": courier_address},
        )

    def post(self, request, id):
        courier_address = CourierAddress.objects.get(id=id)
        receiver_form = ReceiverDetailsForm(request.POST, instance=courier_address)
        if receiver_form.is_valid():
            receiver_form.save()
            messages.success(request, "Courier Address Updated successfully")
            return redirect("viewcourieraddress_list")
        return render(
            request,
            self.template_name,
            {"receiver_form": receiver_form, "courier_address": courier_address},
        )


def delete_courierdetails(request, id):
    courier = get_object_or_404(CourierAddress, id=id)
    courier.delete()
    messages.success(request, "CourierAddress deleted successfully..")
    return redirect("viewcourieraddress_list")


# --------------------- Import Branch -----------------------


def import_branch(request):
    if request.method == "POST":
        file = request.FILES["file"]
        print("filesss", file)
        path = str(file)

        try:
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                branch_name = row["branch_name"].capitalize()
                branch_source = row["branch_source"].upper()

                branch, created = Branch.objects.get_or_create(
                    branch_name=branch_name,
                    branch_source=branch_source,
                )

                if created:
                    branch.save()

            messages.success(request, "Data Imported Successfully!!")

        except Exception as e:
            messages.warning(request, e)
            return redirect("add_branch")
    return redirect("add_branch")


######################################### EMPLOYEE #################################################


def add_employee(request):
    branches = Branch.objects.all()
    groups = Group.objects.all()

    if request.method == "POST":
        department = request.POST.get("department")
        branch_id = request.POST.get("branch_id")
        group_id = request.POST.get("group_id")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        password = "123456"
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        address = request.POST.get("address")
        zipcode = request.POST.get("zipcode")
        api_key = request.POST.get("api_key")
        authorization = request.POST.get("authorization")
        tata_tele_agent_no = request.POST.get("tata_tele_agent_no")
        files = request.FILES.get("file")

        if not branch_id:
            messages.warning(request, "Branch ID is required")
            return redirect("emp_personal_details")

        try:
            branchh = Branch.objects.get(id=branch_id)
            group = Group.objects.get(id=group_id)
            if Employee.objects.filter(contact_no__iexact=contact).exists():
                messages.error(request, "Contact No. already exists.")
                return redirect("emp_personal_details")
            if CustomUser.objects.filter(email__iexact=email).exists():
                messages.error(request, "Email Address already Register...")
                return redirect("emp_personal_details")
            user = CustomUser.objects.create_user(
                username=email,
                first_name=firstname,
                last_name=lastname,
                email=email,
                password=password,
                user_type="3",
            )

            user.employee.department = department
            user.employee.branch = branchh
            user.employee.group = group
            user.employee.contact_no = contact
            user.employee.country = country
            user.employee.state = state
            user.employee.City = city
            user.employee.Address = address
            user.employee.zipcode = zipcode
            user.employee.tata_tele_api_key = api_key
            user.employee.tata_tele_authorization = authorization
            user.employee.tata_tele_agent_number = tata_tele_agent_no
            user.employee.file = files

            user.save()
            subject = "Congratulations! Your Account is Created"
            message = (
                f"Hello {firstname} {lastname},\n\n"
                f"Welcome to SSDC \n\n"
                f"Congratulations! Your account has been successfully created as an agent.\n\n"
                f" Your id is {email} and your password is {password}.\n\n"
                f" go to login : https://crm.theskytrails.com/ \n\n"
                f"Thank you for joining us!\n\n"
                f"Best regards,\nThe Sky Trails"
            )

            recipient_list = [email]

            send_mail(subject, message, from_email=None, recipient_list=recipient_list)
            messages.success(
                request,
                "Employee Added Successfully , Congratulation Mail Send Successfully!!",
            )

            mobile = contact
            message = (
                f"Welcome to SSDC \n\n"
                f"Congratulations! Your account has been successfully created as an agent.\n\n"
                f" Your id is {email} and your password is {password}.\n\n"
                f" go to login : https://crm.theskytrails.com/ \n\n"
                f"Thank you for joining us!\n\n"
                f"Best regards,\nThe Sky Trails"
            )
            response = send_whatsapp_message(mobile, message)
            if response.status_code == 200:
                pass
            else:
                pass

            return redirect("emp_list")

        except Exception as e:
            messages.warning(request, str(e))
            return redirect("emp_personal_details")

    context = {"branch": branches, "group": groups}
    return render(request, "Admin/Employee Management/addemp1.html", context)


class all_employee(ListView):
    model = Employee
    template_name = "Admin/Employee Management/Employeelist.html"
    context_object_name = "employee"

    def get_queryset(self):
        return Employee.objects.order_by("-id")


def employee_update(request, pk):
    employee = Employee.objects.get(pk=pk)
    context = {"employee": employee}

    return render(request, "Admin/Employee Management/editemp1.html", context)


def employee_update_save(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        department = request.POST.get("department")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        address = request.POST.get("address")
        zipcode = request.POST.get("zipcode")

        authorization = request.POST.get("authorization")
        api_key = request.POST.get("api_key")
        tata_tele_agent_no = request.POST.get("tata_tele_agent_no")
        file = request.FILES.get("file")

        user = CustomUser.objects.get(id=employee_id)

        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.employee.department = department
        user.employee.contact_no = contact
        user.employee.country = country
        user.employee.state = state
        user.employee.City = city
        user.employee.Address = address
        user.employee.zipcode = zipcode

        user.employee.tata_tele_authorization = authorization
        user.employee.tata_tele_api_key = api_key
        user.employee.tata_tele_agent_number = tata_tele_agent_no

        if file:
            user.employee.file = file
        user.save()
        messages.success(request, "Employee Updated Successfully")
        return redirect("emp_list")


def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    messages.success(request, "Employee deleted successfully..")
    return redirect("emp_list")


############################################### AGENT ########################################################


def add_agent(request):
    # logged_in_user = CustomUser.objects.get(username=request.user.username)
    relevant_employees = Employee.objects.all()

    if request.method == "POST":
        type = request.POST.get("type")

        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        password = request.POST.get("password")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        address = request.POST.get("address")
        zipcode = request.POST.get("zipcode")
        files = request.FILES.get("files")

        existing_agent = CustomUser.objects.filter(username=email)

        try:
            if existing_agent:
                messages.warning(request, f'"{email}" already exists.')
                return redirect("add_agent")

            if type == "Outsourcing Partner":
                user = CustomUser.objects.create_user(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password,
                    user_type="5",
                )
                # logged_in_user = CustomUser.objects.get(username=request.user.username)

                user.outsourcingagent.type = type
                user.outsourcingagent.contact_no = contact
                user.outsourcingagent.country = country
                user.outsourcingagent.state = state
                user.outsourcingagent.City = city
                user.outsourcingagent.Address = address
                user.outsourcingagent.zipcode = zipcode
                user.outsourcingagent.profile_pic = files
                # user.outsourcingagent.registerdby = logged_in_user
                user.save()

                subject = "Congratulations! Your Account is Created"
                message = (
                    f"Hello {firstname} {lastname},\n\n"
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an Outsource Agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com/Agent/Login/ \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )

                recipient_list = [email]

                send_mail(
                    subject, message, from_email=None, recipient_list=recipient_list
                )

                mobile = contact
                message = (
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an Outsource Agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com/ \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )
                response = send_whatsapp_message(mobile, message)
                if response.status_code == 200:
                    pass
                else:
                    pass

                messages.success(request, "OutSource Agent Added Successfully")
                return redirect("all_outsource_agent")

            else:
                user = CustomUser.objects.create_user(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password,
                    user_type="4",
                )
                # logged_in_user = CustomUser.objects.get(username=request.user.username)

                user.agent.type = type
                user.agent.contact_no = contact
                user.agent.country = country
                user.agent.state = state
                user.agent.City = city
                user.agent.Address = address
                user.agent.zipcode = zipcode
                user.agent.profile_pic = files
                # user.agent.registerdby = logged_in_user
                user.save()

                context = {
                    "employees": relevant_employees,
                }

                subject = "Congratulations! Your Account is Created"
                message = (
                    f"Hello {firstname} {lastname},\n\n"
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com/Agent/Login/ \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )

                recipient_list = [email]

                send_mail(
                    subject, message, from_email=None, recipient_list=recipient_list
                )

                mobile = contact
                message = (
                    f"Welcome to SSDC \n\n"
                    f"Congratulations! Your account has been successfully created as an agent.\n\n"
                    f" Your id is {email} and your password is {password}.\n\n"
                    f" go to login : https://crm.theskytrails.com/ \n\n"
                    f"Thank you for joining us!\n\n"
                    f"Best regards,\nThe Sky Trails"
                )
                response = send_whatsapp_message(mobile, message)
                if response.status_code == 200:
                    pass
                else:
                    pass

                messages.success(request, "Agent Added Successfully")
                return redirect("agent_list")

        except Exception as e:
            messages.warning(request, e)

    context = {
        "employees": relevant_employees,
    }

    return render(request, "Admin/Agent Management/addagent.html", context)


class all_agent(ListView):
    model = Agent
    template_name = "Admin/Agent Management/agentlist.html"
    context_object_name = "agent"

    def get_queryset(self):
        return Agent.objects.all().order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee_queryset"] = Employee.objects.all()
        return context


def admin_agent_details(request, id):
    agent = Agent.objects.get(id=id)
    users = agent.users

    if request.method == "POST":
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")

        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        maritial = request.POST.get("maritial")
        original_pic = request.FILES.get("original_pic")
        organization = request.POST.get("organization")
        business_type = request.POST.get("business_type")
        registration = request.POST.get("registration")
        address = request.POST.get("address")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        zipcode = request.POST.get("zipcode")
        accountholder = request.POST.get("accountholder")
        bankname = request.POST.get("bankname")
        branchname = request.POST.get("branchname")
        account = request.POST.get("account")
        ifsc = request.POST.get("ifsc")

        print("first nameeee", firstname)

        if dob:
            users.agent.dob = dob
        if gender:
            users.agent.gender = gender
        if maritial:
            users.agent.marital_status = maritial
        if original_pic:
            users.agent.profile_pic = original_pic

        users.first_name = firstname

        users.agent.organization_name = organization
        users.agent.business_type = business_type
        users.agent.registration_number = registration
        users.agent.Address = address
        users.agent.country = country
        users.agent.state = state
        users.agent.City = city
        users.agent.zipcode = zipcode
        users.agent.account_holder = accountholder
        users.agent.bank_name = bankname
        users.agent.branch_name = branchname
        users.agent.account_no = account
        users.agent.ifsc_code = ifsc

        users.save()
        messages.success(request, "Updated Successfully")
        return redirect("admin_agent_details", id)

    context = {"agent": agent}
    return render(request, "Admin/Agent Management/Update/agentupdate.html", context)


def admin_agent_agreement(request, id):
    agent = Agent.objects.get(id=id)
    agntagreement = AgentAgreement.objects.all()
    if request.method == "POST":
        name = request.POST.get("agreement_name")
        file = request.FILES.get("file")
        agreement = AgentAgreement.objects.create(
            agent=agent, agreement_name=name, agreement_file=file
        )
        agreement.save()
        messages.success(request, "Agreement Updated Succesfully...")
        return redirect("admin_agent_agreement", id)
    context = {"agent": agent, "agreement": agntagreement}
    return render(request, "Admin/Agent Management/Update/agentagreement.html", context)


def admin_agent_agreement_update(request, id):
    agree = AgentAgreement.objects.get(id=id)
    agent = agree.agent

    if request.method == "POST":
        agntagreement = AgentAgreement.objects.get(id=id)
        agreement_name = request.POST.get("agreement_name")
        file = request.FILES.get("file")

        agntagreement.agreement_name = agreement_name
        if file:
            agntagreement.agreement_file = file
        agntagreement.save()
        messages.success(request, "Agreement Updated Successfully...")
        return redirect("admin_agent_agreement", agent.id)


def admin_agent_agreement_delete(request, id):
    agree = AgentAgreement.objects.get(id=id)
    agent = agree.agent
    agreement = AgentAgreement.objects.get(id=id)
    agreement.delete()
    messages.success(request, "Agreement Deleted Successfully...")
    return redirect("admin_agent_agreement", agent.id)


def admin_agent_kyc(request, id):
    agent = Agent.objects.get(id=id)
    context = {"agent": agent}
    if request.method == "POST":
        adharfront_file = request.FILES.get("adharfront_file")
        adharback_file = request.FILES.get("adharback_file")
        pan_file = request.FILES.get("pan_file")
        registration_file = request.FILES.get("registration_file")
        if adharfront_file:
            agent.adhar_card_front = adharfront_file
            agent.save()
        elif adharback_file:
            agent.adhar_card_back = adharback_file
            agent.save()
        elif pan_file:
            agent.pancard = pan_file
            agent.save()
        elif registration_file:
            agent.registration_certificate = registration_file
            agent.save()

    return render(request, "Admin/Agent Management/Update/agentkyc.html", context)


class all_outsource_agent(ListView):
    model = OutSourcingAgent
    template_name = "Admin/Agent Management/outsourcelist.html"
    context_object_name = "agentoutsource"

    def get_queryset(self):
        return OutSourcingAgent.objects.all().order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee_queryset"] = Employee.objects.all()
        return context


def admin_outsourceagent_details(request, id):
    outsourceagent = OutSourcingAgent.objects.get(id=id)
    context = {"outsourceagent": outsourceagent}
    return render(
        request,
        "Admin/Agent Management/OutsourceUpdate/outsource_agentupdate.html",
        context,
    )


def admin_outsource_agent_agreement(request, id):
    outsourceagent = OutSourcingAgent.objects.get(id=id)
    context = {"outsourceagent": outsourceagent}
    return render(
        request,
        "Admin/Agent Management/OutsourceUpdate/outsource_agentagreement.html",
        context,
    )


def admin_outsource_agent_kyc(request, id):
    outsourceagent = OutSourcingAgent.objects.get(id=id)
    context = {"outsourceagent": outsourceagent}
    return render(
        request,
        "Admin/Agent Management/OutsourceUpdate/outsource_agentkyc.html",
        context,
    )


###################################################### PACKAGE ###############################################


class PackageCreateView(CreateView):
    model = Package
    form_class = PackageForm
    template_name = "Admin/Product/addproduct.html"
    success_url = reverse_lazy("Package_list")

    def form_valid(self, form):
        try:
            # form.instance.last_updated_by = self.request.user
            form.save()
            messages.success(self.request, "Package Added Successfully.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error: {e}")
            print("Error Occured ", e)
            return self.form_invalid(form)


class PackageListView(ListView):
    model = Package
    template_name = "Admin/Product/product.html"
    context_object_name = "Package"

    def get_queryset(self):
        return Package.objects.order_by("-id")


class editPackage(UpdateView):
    model = Package
    form_class = PackageForm
    template_name = "Admin/Product/editProduct.html"
    success_url = reverse_lazy("Package_list")

    def form_valid(self, form):
        # form.instance.lastupdated_by = self.request.user

        messages.success(self.request, "Package Updated Successfully.")

        return super().form_valid(form)


class PackageDetailView(DetailView):
    model = Package
    template_name = "Admin/Product/Productdetails.html"
    context_object_name = "package"


def delete_package(request, id):
    package = get_object_or_404(Package, id=id)
    package.delete()
    return redirect("Package_list")


############################################ LOGIN LOGS ######################################################


class loginlog(ListView):
    model = LoginLog
    template_name = "Admin/Login Logs/Loginlogs.html"
    context_object_name = "loginlog"

    def get_queryset(self):
        return LoginLog.objects.exclude(user__user_type="1").order_by("-id")


########################################################## PRICING ##########################################################################


def add_subcategory(request):
    country = VisaCountry.objects.all()
    category = VisaCategory.objects.all()

    context = {
        "country": country,
        "category": category,
    }

    if request.method == "POST":
        country_id = request.POST.get("country")
        category_id = request.POST.get("category")
        subcategory_name = request.POST.get("subcategory")
        amount = float(request.POST.get("amount") or 0)
        cgst = float(request.POST.get("cgst") or 0)
        sgst = float(request.POST.get("sgst") or 0)
        # user = request.user

        # try:
        # Calculate the totalAmount
        total = amount + ((amount * (cgst + sgst)) / 100)

        pricing = VisaSubcategory.objects.create(
            country_id_id=country_id,
            category_id_id=category_id,
            subcategory_name_id=subcategory_name,
            estimate_amt=amount,
            cgst=cgst,
            sgst=sgst,
            totalAmount=total,
            # lastupdated_by=user.first_name,
        )
        pricing.save()

        messages.success(request, "Pricing Added Successfully !!")
        return redirect("subcategory_list")
        # except Exception as e:
        #     # Handle any exceptions here and possibly log them
        #     # messages.error(request, str(e))
        #     print("eeee",e)

    return render(request, "Admin/mastermodule/Pricing/add_pricing.html", context)


def subcategory_list(request):
    subcategory = VisaSubcategory.objects.all().order_by("-id")
    context = {"subcategory": subcategory}
    return render(request, "Admin/mastermodule/Pricing/pricing.html", context)


def visa_subcategory_edit(request, id):
    instance = VisaSubcategory.objects.get(id=id)

    if request.method == "POST":
        form = VisasubCategoryForm(request.POST, instance=instance)
        if form.is_valid():
            # user = request.user
            # form.instance.lastupdated_by = f"{user.first_name} {user.last_name}"
            form.instance.totalAmount = form.instance.estimate_amt + (
                (form.instance.estimate_amt * (form.instance.cgst + form.instance.sgst))
                / 100
            )
            form.save()
            messages.success(request, "Subcategory updated successfully.")
            return redirect("subcategory_list")
    else:
        form = VisasubCategoryForm(instance=instance)

    return render(
        request, "Admin/mastermodule/pricing/edit_pricing.html", {"form": form}
    )


def delete_pricing(request, id):
    pricing = VisaSubcategory.objects.get(id=id)
    pricing.delete()
    messages.success(request, "Pricing deleted successfully..")
    return HttpResponseRedirect(reverse("subcategory_list"))


def leads(request):
    return render(request, "Admin/Enquiry/lead1.html")


def leads2(request):
    return render(request, "Admin/Enquiry/lead2.html")


def leads3(request):
    return render(request, "Admin/Enquiry/lead3.html")


def leads4(request):
    return render(request, "Admin/Enquiry/lead4.html")


from django.forms.models import model_to_dict
from django.http import JsonResponse


class Enquiry1View(CreateView):
    def get(self, request):
        form = EnquiryForm1()
        return render(
            request,
            "Admin/Enquiry/lead1.html",
            {"form": form},
        )

    def post(self, request):
        form = EnquiryForm1(request.POST)
        if form.is_valid():
            cleaned_data = {
                "FirstName": form.cleaned_data["FirstName"],
                "LastName": form.cleaned_data["LastName"],
                "email": form.cleaned_data["email"],
                "contact": form.cleaned_data["contact"],
                "Dob": form.cleaned_data["Dob"].strftime("%Y-%m-%d"),
                "Gender": form.cleaned_data["Gender"],
                "Country": form.cleaned_data["Country"],
                "passport_no": form.cleaned_data["passport_no"],
            }
            request.session["enquiry_form1"] = cleaned_data
            return redirect("enquiry_form2")

        return render(
            request,
            "Admin/Enquiry/lead2.html",
            {"form": form},
        )


class Enquiry2View(CreateView):
    def get(self, request):
        form = EnquiryForm2()
        return render(
            request,
            "Admin/Enquiry/lead2.html",
            {"form": form},
        )

    def post(self, request):
        form = EnquiryForm2(request.POST)
        if form.is_valid():
            # Retrieve personal details from session
            enquiry_form1 = request.session.get("enquiry_form1", {})
            cleaned_data = {
                "spouse_name": form.cleaned_data["spouse_name"],
                "spouse_no": form.cleaned_data["spouse_no"],
                "spouse_email": form.cleaned_data["spouse_email"],
                "spouse_passport": form.cleaned_data["spouse_passport"],
                "spouse_dob": form.cleaned_data["spouse_dob"].strftime("%Y-%m-%d"),
            }

            # Merge personal details with receiver details
            merged_data = {**enquiry_form1, **cleaned_data}

            # Save the merged data to the session
            request.session["enquiry_form2"] = merged_data
            return redirect("enquiry_form3")

        return render(
            request,
            "Admin/Enquiry/lead2.html",
            {"form": form},
        )


class Enquiry3View(CreateView):
    def get(self, request):
        form = EnquiryForm3()
        return render(
            request,
            "Admin/Enquiry/lead3.html",
            {"form": form},
        )

    def post(self, request):
        form1_data = request.session.get("enquiry_form1", {})
        form2_data = request.session.get("enquiry_form2", {})
        form3 = EnquiryForm3(request.POST)

        if form3.is_valid():
            # Merge data from all three forms
            merged_data = {
                **form1_data,
                **form2_data,
                **form3.cleaned_data,
            }

            # Save the merged data to the database
            enquiry = Enquiry(**merged_data)
            enquiry.save()
            messages.success(request, "Enquiry Added successfully")

            # Clear session data after successful submission
            request.session.pop("enquiry_form1", None)
            request.session.pop("enquiry_form2", None)

            return redirect("enquiry_form4", id=enquiry.id)

        return render(
            request,
            "Admin/Enquiry/lead3.html",
            {"form": form3},
        )

    def get_success_url(self):
        enquiry_id = self.object.id
        return reverse_lazy("Agent_Document", kwargs={"id": enquiry_id})


def admindocument(request, id):
    enq = Enquiry.objects.get(id=id)
    document = Document.objects.all()

    doc_file = DocumentFiles.objects.filter(enquiry_id=enq)

    case_categories = CaseCategoryDocument.objects.filter(country=enq.Visa_country)

    documents_prefetch = Prefetch(
        "document",
        queryset=Document.objects.select_related("document_category", "lastupdated_by"),
    )

    case_categories = case_categories.prefetch_related(documents_prefetch)

    grouped_documents = {}

    for case_category in case_categories:
        for document in case_category.document.all():
            document_category = document.document_category
            testing = document.document_category.id

            if document_category not in grouped_documents:
                grouped_documents[document_category] = []

            grouped_documents[document_category].append(document)

    context = {
        "enq": enq,
        "grouped_documents": grouped_documents,
        "doc_file": doc_file,
    }

    return render(request, "Admin/Enquiry/lead4.html", context)


def upload_document(request):
    if request.method == "POST":
        document_id = request.POST.get("document_id")
        enq_id = request.POST.get("enq_id")

        document = Document.objects.get(pk=document_id)
        document_file = request.FILES.get("document_file")
        enq = Enquiry.objects.get(id=enq_id)
        # Check if a DocumentFiles object with the same document exists
        try:
            doc = DocumentFiles.objects.filter(
                enquiry_id=enq_id, document_id=document
            ).first()
            if doc:
                doc.document_file = document_file
                doc.lastupdated_by = request.user
                doc.save()

                return redirect("enquiry_form4", id=enq_id)
            else:
                documest_files = DocumentFiles.objects.create(
                    document_file=document_file,
                    document_id=document,
                    enquiry_id=enq,
                    lastupdated_by=request.user,
                )
                documest_files.save()
                return redirect("enquiry_form4", enq_id)

        except Exception as e:
            pass


def delete_docfile(request, id):
    doc_id = DocumentFiles.objects.get(id=id)
    enq_id = Enquiry.objects.get(id=doc_id.enquiry_id.id)
    enqq = enq_id.id

    doc_id.delete()
    return redirect("enquiry_form4", enqq)


# ----------------------------------- Leads Details --------------------------


def admin_new_leads_details(request):
    enquiry = Enquiry.objects.all()
    context = {"enquiry": enquiry}
    return render(request, "Admin/Enquiry/lead-details.html", context)


def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        data = response.json()
        return data["ip"]
    except Exception as e:
        # Handle the exception (e.g., log the error)
        return None


def add_notes(request):
    if request.method == "POST":
        enq_id = request.POST.get("enq_id")
        notes_text = request.POST.get("notes")
        file = request.FILES.get("file")
        user = request.user

        try:
            enq = Enquiry.objects.get(id=enq_id)
            ip_address = get_public_ip()

            notes = Notes.objects.create(
                enquiry=enq,
                notes=notes_text,
                file=file,
                ip_address=ip_address,
                created_by=user,
            )
            notes.save()

        except Enquiry.DoesNotExist:
            pass

    return redirect("admin_new_leads_details")

