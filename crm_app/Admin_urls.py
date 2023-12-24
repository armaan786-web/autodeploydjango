from django.urls import path, include

from .AdminViews import *

urlpatterns = [
    path("Dashboard/", admin_dashboard, name="admin_dashboard"),
    path("Profile/", admin_profile, name="admin_profile"),
    path("AddVisaCountry/", add_visacountry, name="add_visacountry"),
    path("VisaCountry/update/", visacountryupdate_view, name="visacountryupdate_view"),
    path("import/Country", import_country, name="importcountry"),
    path(
        "VisaCountry/Delete/<int:id>", delete_visa_country, name="delete_visa_country"
    ),
    path("AddVisaCategory/", add_visacategory, name="add_visacategory"),
    path("VisaCategory/Edit/", visacategoryupdate_view, name="visacategoryupdate_view"),
    path("deletecategory/<int:id>/", delete_category, name="delete_category"),
    path("AddDocumentCategory/", add_documentcategory, name="add_documentcategory"),
    path(
        "DocumentCategory/Edit/",
        documentcategoryupdate_view,
        name="documentcategoryupdate_view",
    ),
    path(
        "deletedocumentcategory/<int:id>/",
        delete_documentcategory,
        name="delete_documentcategory",
    ),
    path("AddDocument/", add_document, name="add_document"),
    path("Document/Edit/", documentupdate_view, name="documentupdate_view"),
    path("deletedocument/<int:id>/", delete_document, name="delete_document"),
    path(
        "AddCaseCategoryDocument/",
        CaseCategoryDocumentCreateView.as_view(),
        name="add_CaseCategoryDocument",
    ),
    path(
        "CaseCategoryDocumentList/",
        CaseCategoryDocumentListView.as_view(),
        name="CaseCategoryDocument_list",
    ),
    path(
        "CaseCategoryDocumentEdit/<int:pk>",
        editCaseCategoryDocument.as_view(),
        name="editCaseCategoryDocument",
    ),
    path(
        "casecategorydocument/delete/<int:id>/",
        delete_casecategorydocument,
        name="delete_casecategorydocument",
    ),
    path("Addbranch/", add_branch, name="add_branch"),
    path("Branch/Edit/", branchupdate_view, name="branchupdate_view"),
    path("deletebranch/<int:id>/", delete_branch, name="delete_branch"),
    path("import/Branch", import_branch, name="import_branch"),
    path("create_group/", CreateGroupView.as_view(), name="create_group"),
    path("GroupList/", GroupListView.as_view(), name="Group_list"),
    path("GroupEdit/<int:pk>", editGroup.as_view(), name="editgroup"),
    path("group/delete/<int:id>/", delete_group, name="delete_group"),
    path("personal_details/", PersonalDetailsView.as_view(), name="personal_details"),
    path("receiver_details/", ReceiverDetailsView.as_view(), name="receiver_details"),
    path(
        "ViewCourierAddress/", viewcourieraddress_list, name="viewcourieraddress_list"
    ),
    path(
        "update_company_details/<int:id>/",
        UpdateCompanyDetailsView.as_view(),
        name="update_company_details",
    ),
    path(
        "update_receiver_details/<int:id>/",
        UpdateReceiverDetailsView.as_view(),
        name="update_receiver_details",
    ),
    path(
        "courierdetails/delete/<int:id>/",
        delete_courierdetails,
        name="delete_courierdetails",
    ),
    path("emp_personal_details/", add_employee, name="emp_personal_details"),
    path("emp_list/", all_employee.as_view(), name="emp_list"),
    path("Employe/Update/<int:pk>", employee_update, name="employee_update"),
    path("Employe/Update/Save", employee_update_save, name="employee_update_save"),
    path("Employee/delete/<int:id>/", delete_employee, name="delete_employee"),
    path("add_agent/", add_agent, name="add_agent"),
    path("agent_list/", all_agent.as_view(), name="agent_list"),
    path("Agent/Details/<int:id>", admin_agent_details, name="admin_agent_details"),
    path(
        "Agent/Agreement/<int:id>", admin_agent_agreement, name="admin_agent_agreement"
    ),
    path(
        "Agent/Agreement/update/<int:id>/",
        admin_agent_agreement_update,
        name="update_agreement",
    ),
    path(
        "Agent/Agreement/Delete/<int:id>/",
        admin_agent_agreement_delete,
        name="admin_agent_agreement_delete",
    ),
    path("Agent/Kyc/<int:id>", admin_agent_kyc, name="admin_agent_kyc"),
    path(
        "AllOutSourceAgent/", all_outsource_agent.as_view(), name="all_outsource_agent"
    ),
    path(
        "OutSourceAgent/Details/<int:id>",
        admin_outsourceagent_details,
        name="admin_outsourceagent_details",
    ),
    path(
        "OutSourceAgent/Agreement/<int:id>",
        admin_outsource_agent_agreement,
        name="admin_outsource_agent_agreement",
    ),
    path(
        "OutSource/Agent/Kyc/<int:id>",
        admin_outsource_agent_kyc,
        name="admin_outsource_agent_kyc",
    ),
    path(
        "AllOutSourceAgent/", all_outsource_agent.as_view(), name="all_outsource_agent"
    ),
    path("AddPackage/", PackageCreateView.as_view(), name="add_Package"),
    path("PackageList/", PackageListView.as_view(), name="Package_list"),
    path("PackageEdit/<int:pk>", editPackage.as_view(), name="editPackage"),
    path("packages/<int:pk>/", PackageDetailView.as_view(), name="package_detail"),
    path("package/delete/<int:id>/", delete_package, name="delete_package"),
    path("LoginLogs", loginlog.as_view(), name="loginlog"),
    path("AddSubCategory/", add_subcategory, name="add_subcategory"),
    path("SubCategoryList/", subcategory_list, name="subcategory_list"),
    path(
        "SubCategoryEdit/<int:id>", visa_subcategory_edit, name="visa_subcategory_edit"
    ),
    path("pricing/delete/<int:id>/", delete_pricing, name="delete_pricing"),
    path("AddEnquiry/", Enquiry1View.as_view(), name="enquiry_form1"),
    path("AddEnquiry2/", Enquiry2View.as_view(), name="enquiry_form2"),
    path("AddEnquiry3/", Enquiry3View.as_view(), name="enquiry_form3"),
    path("enquiry_form4/<int:id>/", admindocument, name="enquiry_form4"),
    path("Uploaddocument/", upload_document, name="uploaddocument"),
    path("Delete/UploadFile/<int:id>", delete_docfile, name="docfile"),
    # ------------------------------- LEADS ------------------------
    path("AllNewLeads", admin_new_leads_details, name="admin_new_leads_details"),
    path("AddNotes/", add_notes, name="add_notes"),
]
