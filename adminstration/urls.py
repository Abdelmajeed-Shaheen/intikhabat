from django.urls import path
from .views import (
                    CampaignManagementMainView,CreateComitteeView,
                    GrantPermissions,ComitteeMemberView,SearchComitteeView,
                    CreateAreaView,CreateDistrictView,html_to_pdf_view,
                    GetReportByCommitteeMember,GetGovernorateDepartment ,
                    GetDepartmentArea,GetVotersList,by_committee_member_report,
                    GetReportByIdentifier,by_identifier_report                                                                                                                                                 
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
    path("get_voters",GetVotersList.as_view(),name="get_voters"),
    path("by-cm-report",by_committee_member_report,name="by-cm-report"),
    path("identifier-report",GetReportByIdentifier.as_view(),name="identifier-report"),
    path("by-idn-report",by_identifier_report,name="by-idn-report"),



]
