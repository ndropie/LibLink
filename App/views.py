from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Member

# Create your views here.


def AddMember(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        date_of_birth = request.POST.get("date_of_birth")
        address = request.POST.get("address")
        joined_date = request.POST.get("joined_date")

        member = Member(
            full_name=full_name,
            phone=phone,
            email=email,
            date_of_birth=date_of_birth,
            address=address,
            joined_date=joined_date
        )
        member.save()
        return redirect("MembersPage")
        
    return render(request,"AddMemberForm.html")

'''----------------------------------------------------
members now can be added using the POST method 
--------------------------------------------------------'''


def MembersPage(request):
    allmembers = Member.objects.all().order_by("-id")
    return render(request,"MembersPage.html",{'allmembers':allmembers})


def MemberDetails(request,MemberID):
    member = Member.objects.get(id = MemberID)
    return render ( request, "MemberDetails.html",
                   {"member":member})

def EditMember(request, MemberID):
    member = Member.objects.get(id = MemberID)

    if request.method == 'POST':
        member.full_name = request.POST.get("full_name")
        member.phone = request.POST.get("phone")
        member.email = request.POST.get("email")
        member.date_of_birth = request.POST.get("date_of_birth")
        member.address = request.POST.get("address")
        member.joined_date = request.POST.get("joined_date")

        member.save()
        return redirect("EditMember",MemberID= member.id)

    return render(request,"EditMember.html",{"member":member})



def MembershipPage(request):
    return render(request,"MembershipPage.html")


def SeatManagementPage(request):
    return render(request,"SeatManagementPage.html")


def FinancePage(request):
    return render(request,"FinancePage.html")

def SettingsPage(request):
    return render(request,"SettingsPage.html")

def Dashboard(request):
    return render(request,"Dashbaord.html")

