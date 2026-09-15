from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.Dashboard, name= 'Dashboard'),
    path('MembersPage/', views.MembersPage, name= 'MembersPage'),
    path('MembersPage/AddMember/', views.AddMember, name= 'AddMember'),
    path('MembersPage/<int:MemberID>/', views.MemberDetails, name='MemberDetails'),
    path('EditMember/<int:MemberID>/', views.EditMember, name='EditMember'),    
    path("DeleteMember/<int:id>/", views.DeleteMember, name="DeleteMember"),

    path('MembershipPlans/', views.MembershipPlansPage, name='MembershipPlans'),
    path('MembershipPlans/AddPlan/', views.AddMembershipPlan, name='AddMembershipPlan'),
    path('EditMembershipPlan/<int:plan_id>/',views.EditMembershipPlan , name='EditMembershipPlan'),
    path('DeleteMembershipPlan/<int:plan_id>/',views.DeleteMembershipPlan,name='DeleteMembershipPlan'),
    
    path('SeatManagement/', views.SeatManagementPage, name= 'SeatManagementPage'),


    path('SettingsPage/', views.SettingsPage, name= 'SettingsPage'),

    
]