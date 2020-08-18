from django.urls import path
from .views import (
                    CampaignManagementMainView,CreateComitteeView,
                    GrantPermissions,ComitteeMemberView,SearchComitteeView,
                    CreateAreaView,CreateDistrictView,html_to_pdf_view,
                    GetReportByCommitteeMember,GetGovernorateDepartment ,
                    GetDepartmentArea,GetVotersList,by_committee_member_report,
                    GetReportByIdentifier,by_identifier_report,GetVotersByAddressReport,
                    by_address_report,GetVotersByStatusReport,by_status_report,
                    update_comittee,update_comittee_member,get_cm,
                    get_identifier,update_voter,
                    GetDistrict                                                                                                                                                
                    )
urlpatterns = [
    path("main",CampaignManagementMainView.as_view(),name="main"),
    path("comittee-member",ComitteeMemberView.as_view(),name="comittee-member"),
    path("create-comittee",CreateComitteeView.as_view(),name="create-comittee"),
    path("grant-permession",GrantPermissions.as_view(),name="grant-permession"),
    path("search-comittee",SearchComitteeView.as_view(),name="search-comittee"),
    path("create-area",CreateAreaView.as_view(),name="create-area"),
    path("create-district",CreateDistrictView.as_view(),name="create-district"),
    path("pdf-report",html_to_pdf_view,name="pdf-report"),
    path("cm-report",GetReportByCommitteeMember.as_view(),name="cm-report"),
    path("get_gover_dept",GetGovernorateDepartment.as_view(),name="get_gover_dept"),
    path("get_dept_area",GetDepartmentArea.as_view(),name="get_dept_area"),
    path("get_district",GetDistrict.as_view(),name="get_district"),

    path("get_voters",GetVotersList.as_view(),name="get_voters"),
    path("by-cm-report",by_committee_member_report,name="by-cm-report"),
    path("identifier-report",GetReportByIdentifier.as_view(),name="identifier-report"),
    path("by-idn-report",by_identifier_report,name="by-idn-report"),
    path("address-report",GetVotersByAddressReport.as_view(),name="address-report"),
    path("by-address-report",by_address_report,name="by-address-report"),
    path("status-report",GetVotersByStatusReport.as_view(),name="status-report"),
    path("by-status-report",by_status_report,name="by-status-report"),
    path("update-committee/<id>/",update_comittee,name="update-committee"),
    path("update-cm/<id>/",update_comittee_member,name="update-cm"),
    path("get-cm",get_cm,name="get-cm"),
    path("get-identifier",get_identifier,name="get-identifier"),
    path("update-voter/<id>/",update_voter,name="update-voter"),












]
