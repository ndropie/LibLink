from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.Dashboard, name= 'Dashboard'),
    path('SeatManagementPage/', views.SeatManagementPage, name= 'SeatManagementPage'),
    path('MembersPage/', views.MembersPage, name= 'MembersPage'),
    path('MembershipPage/', views.MembershipPage, name= 'MembershipPage'),
    path('FinancePage/', views.FinancePage, name= 'FinancePage'),
    path('SettingsPage/', views.SettingsPage, name= 'SettingsPage')

]