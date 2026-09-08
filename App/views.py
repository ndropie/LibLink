from django.shortcuts import render

# Create your views here.

def Dashboard(request):
    return render(request,"Dashbaord.html")

def SeatManagementPage(request):
    return render(request,"SeatManagementPage.html")

def MembersPage(request):
    return render(request,"MembersPage.html")

def MembershipPage(request):
    return render(request,"MembershipPage.html")

def FinancePage(request):
    return render(request,"FinancePage.html")

def SettingsPage(request):
    return render(request,"SettingsPage.html")

