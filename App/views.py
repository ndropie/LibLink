from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Member, MemberShipPlans

from django.db import connection
# Create your views here.
'''
----------------------------------------------------------------------------------
members module functions 
----------------------------------------------------------------------------------
'''

def AddMember(request):
    if request.method == "POST":

        member_id = request.POST.get("MemberID") or None
        print("DATABASE:", connection.settings_dict["NAME"])
        print("MEMBER ID:", member_id)
        print("EXISTS:", Member.objects.filter(MemberID=member_id).exists())

        if member_id and Member.objects.filter(MemberID=member_id).exists():
            return render(
                request,
                "AddMemberForm.html",
                {
                    "error": f"Member ID '{member_id}' is already in use."
                }
            )

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        date_of_birth = request.POST.get("date_of_birth")
        address = request.POST.get("address")
        joined_date = request.POST.get("joined_date")

        if not full_name or not phone or not date_of_birth or not joined_date:
            print("full_name:", full_name)
            print("phone:", phone)
            print("date_of_birth:", date_of_birth)
            print("address:", address)
            print("joined_date:", joined_date)

            return render(
                request,
                "AddMemberForm.html",
                {
                    "form_error": "Please fill in all required fields."
                }
            )

        member = Member(
            full_name=full_name,
            MemberID=member_id,
            phone=phone,
            email=email,
            date_of_birth=date_of_birth,
            address=address,
            joined_date=joined_date
        )

        member.save()

        return redirect("MembersPage")

    return render(request, "AddMemberForm.html")

def MembersPage(request):
    allmembers = Member.objects.all().order_by("-id")
    return render(request,"MembersPage.html",{'allmembers':allmembers})


def MemberDetails(request,MemberID):
    member = Member.objects.get(id = MemberID)
    return render ( request, "MemberDetails.html",
                   {"member":member})


def EditMember(request, MemberID):
    member = Member.objects.get(id=MemberID)

    if request.method == 'POST':

        member_id = request.POST.get("MemberID") or None

        if (
            member_id
            and Member.objects.filter(MemberID=member_id)
            .exclude(id=member.id)
            .exists()
        ):
            return render(
                request,
                "EditMember.html",
                {
                    "member": member,
                    "error": f"Member ID '{member_id}' is already in use."
                }
            )

        member.full_name = request.POST.get("full_name")
        member.MemberID = member_id
        member.phone = request.POST.get("phone")
        member.email = request.POST.get("email")
        member.date_of_birth = request.POST.get("date_of_birth")
        member.address = request.POST.get("address")
        member.joined_date = request.POST.get("joined_date")
        member.status = request.POST.get("status") == "True"

        member.save()

        return redirect("MembersPage")

    return render(request, "EditMember.html", {"member": member})

def DeleteMember(request,id):
    member = get_object_or_404(Member, id=id)

    if request.method == "POST":
        member.delete()
        return redirect("MembersPage")

    return redirect("EditMember", MemberID=member.id)



'''
----------------------------------------------------------------------------------
MembershipPlan module functions 
----------------------------------------------------------------------------------
'''



def MembershipPlansPage(request):
    plans = MemberShipPlans.objects.all()

    return render(request, 'MembershipPlans.html', {
        'plans': plans
    })


def AddMembershipPlan(request):

    if request.method == 'POST':

        plan_name = request.POST.get('plan_name')
        duration = request.POST.get('duration')
        plan_price = request.POST.get('plan_price')

        MemberShipPlans.objects.create(
            Plan_Name=plan_name,
            Duration=duration,
            Plan_price=plan_price
        )

        return redirect('MembershipPlans')

    return render(request, 'AddMembershipPlan.html')

def EditMembershipPlan(request, plan_id):
    plan = MemberShipPlans.objects.get(id=plan_id)
    if request.method == "POST":

        plan.Plan_Name = request.POST.get("plan_name")
        plan.Duration = request.POST.get("duration")
        plan.Plan_price = request.POST.get("plan_price")
        plan.Plan_Status = request.POST.get("plan_status")

        plan.save()
        return redirect("MembershipPlans")

    return render(request, "EditMembershipPlan.html", {
                "plan": plan})



def DeleteMembershipPlan(request, plan_id):

    plan = MemberShipPlans.objects.get(id=plan_id)

    if request.method == "POST":
        plan.delete()
        return redirect("MembershipPlans")







def SeatManagementPage(request):
    return render(request,"SeatManagementPage.html")


def FinancePage(request):
    return render(request,"FinancePage.html")

def SettingsPage(request):
    return render(request,"SettingsPage.html")

def Dashboard(request):
    return render(request,"Dashbaord.html")

