from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.Dashboard, name= 'Dashboard'),
    path('SeatManagementPage/', views.SeatManagementPage, name= 'SeatManagementPage'),
    path('MembersPage/', views.MembersPage, name= 'MembersPage'),
    path('MembersPage/AddMember/', views.AddMember, name= 'AddMember'),

    path('MembersPage/<int:MemberID>/', views.MemberDetails, name='MemberDetails'),
    path('EditMember/<int:MemberID>/', views.EditMember, name='EditMember'),
    path('MembershipPage/', views.MembershipPage, name= 'MembershipPage'),
    path('FinancePage/', views.FinancePage, name= 'FinancePage'),
    path('SettingsPage/', views.SettingsPage, name= 'SettingsPage'),
    path("DeleteMember/<int:id>/", views.DeleteMember, name="DeleteMember")

    
]