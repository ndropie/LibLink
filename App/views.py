from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import timedelta, date
from django.db import connection
from django.utils import timezone


from .models import (
    Member,
    MemberShipPlans,
    Memberships,
    Seat,
    SeatConfiguration,
    SeatAssignment
)


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
    membercount = len(Member.objects.all())
    for member in allmembers:

            # Get active membership
            member.active_membership = member.memberships.filter(status=True).select_related("plan").first()

            # Get active seat assignment
            member.active_seat = member.seat_assignments.filter(status=True).select_related("seat").first()


    return render(request,"MembersPage.html",
                  {'allmembers':allmembers, 
                   'membercount':membercount})


def MemberDetails(request, MemberID):

    member = Member.objects.get(id=MemberID)

    membership = member.memberships.filter(status=True).first()

    return render(request, 'MemberDetails.html', {
                        'member': member,
                        'membership': membership
    })


def EditMember(request, MemberID):
    member = Member.objects.get(id=MemberID)
    membership = member.memberships.filter(status=True).first()
    plans = MemberShipPlans.objects.filter(Plan_Status=True)

    if request.method == 'POST':

        member_id = request.POST.get("MemberID") or None

        if (
            member_id and Member.objects.filter(MemberID=member_id).exclude(id=member.id).exists()
        ):
            return render(
                request,
                "EditMember.html",
                {
                    "member": member,
                    "membership": membership,
                    "plans": plans,
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

        # Membership
        membership_plan_id = request.POST.get("membership_plan")
        membership_start_date = request.POST.get("membership_start_date")

        if membership_plan_id and membership_start_date:

            plan = MemberShipPlans.objects.get(id=membership_plan_id)

            start_date = date.fromisoformat(membership_start_date)
            expiry_date = start_date + timedelta(days=plan.Duration)

            if membership:
                membership.plan = plan
                membership.start_date = start_date
                membership.expiry_date = expiry_date
                membership.status = True
                membership.save()

            else:
                Memberships.objects.create(
                    member=member,
                    plan=plan,
                    start_date=start_date,
                    expiry_date=expiry_date,
                    status=True
                )

        elif not membership_plan_id:

            if membership:
                membership.status = False
                membership.save()

        return redirect("MembersPage")

    return render(
        request,
        "EditMember.html",
        {
            "member": member,
            "membership": membership,
            "plans": plans
        }
    )



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


def update_expired_memberships():

    today = timezone.localdate()

    expired_memberships = Memberships.objects.filter(
        status=True,
        expiry_date__lt=today
    )

    for membership in expired_memberships:

        membership.status = False
        membership.save()

        has_active_membership = Memberships.objects.filter(
            member=membership.member,
            status=True,
            expiry_date__gte=today
        ).exists()

        if not has_active_membership:
            SeatAssignment.objects.filter(
                member=membership.member,
                status=True
            ).update(status=False)


'''
----------------------------------------------------------------------------------
Seat module functions 
----------------------------------------------------------------------------------
'''

def SeatManagementPage(request):

    update_expired_memberships()

    # Get all seats from the database
    seats = Seat.objects.all().order_by("seat_number")

    # Get the current seat configuration
    configuration = SeatConfiguration.objects.first()

    # Get today's date
    # This is used to check membership expiry
    today = timezone.now().date()

    # This list will contain all rows and their seats
    seat_rows = []

    # Create the seat map only if configuration exists
    if configuration:

        # Loop through the configured number of rows
        for row_index in range(configuration.rows):

            # Generate row letters starting from A
            row_letter = chr(
                ord("A") + row_index
            )

            # Get all seats belonging to this row
            row_seats = seats.filter(
                seat_number__startswith=row_letter
            ).order_by("seat_number")

            for seat in row_seats:

                assignment = SeatAssignment.objects.filter(
                    seat=seat,
                    status=True
                ).select_related("member").first()

                seat.assignment = assignment

                if assignment:

                    membership = assignment.member.memberships.filter(
                        status=True
                    ).first()

                    seat.membership = membership

                    if membership:

                        days_remaining = (
                            membership.expiry_date - today
                        ).days

                        if days_remaining <= 7:
                            seat.state = "expired"
                        else:
                            seat.state = "occupied"

                    else:
                        seat.state = "occupied"

                else:
                    seat.membership = None
                    seat.state = "vacant"

            seat_rows.append({
                "letter": row_letter,
                "seats": row_seats
            })

    # Store the seat selected by the user
    selected_seat = None

    # Check if the user submitted the seat form
    if request.method == "POST":

        # Get the ID of the seat
        seat_id = request.POST.get("seat_id")

        # Get the action
        action = request.POST.get("action")

        # If the user clicked a seat
        if action == "select_seat":

            # Find the selected seat
            selected_seat = get_object_or_404(
                Seat,
                id=seat_id
            )

            # Find the active assignment
            selected_seat.assignment = SeatAssignment.objects.filter(
                seat=selected_seat,
                status=True
            ).select_related("member").first()

            # If assignment exists
            if selected_seat.assignment:

                # Find the member's active membership
                selected_seat.membership = selected_seat.assignment.member.memberships.filter(
                    status=True
                ).first()

            else:

                selected_seat.membership = None

        # If the user submits the assignment form
        if action == "assign_seat":

            member_id = request.POST.get("member_id")
            assigned_date = request.POST.get("assigned_date")

            seat = get_object_or_404(
                Seat,
                id=seat_id
            )

            member = get_object_or_404(
                Member,
                id=member_id
            )

            # Check whether the member has a valid active membership
            membership_exists = member.memberships.filter(
                status=True,
                expiry_date__gte=timezone.localdate()
            ).exists()

            # Do not allow seat assignment without membership
            if not membership_exists:
                return redirect("SeatManagementPage")

            # Create the seat assignment
            SeatAssignment.objects.create(
                seat=seat,
                member=member,
                assigned_date=assigned_date,
                status=True
            )

            return redirect("SeatManagementPage")

        if action == "release_seat":

            seat = get_object_or_404(
                Seat,
                id=seat_id
            )

            assignment = SeatAssignment.objects.filter(
                seat=seat,
                status=True
            ).first()

            if assignment:

                assignment.status = False
                assignment.save()

            return redirect("SeatManagementPage")

        if action == "change_member":

            member_id = request.POST.get("member_id")

            seat = get_object_or_404(
                Seat,
                id=seat_id
            )

            member = get_object_or_404(
                Member,
                id=member_id
            )

            # Check whether the new member has a valid active membership
            membership_exists = member.memberships.filter(
                status=True,
                expiry_date__gte=timezone.localdate()
            ).exists()

            # Do not allow changing to a member without membership
            if not membership_exists:
                return redirect("SeatManagementPage")

            assignment = SeatAssignment.objects.filter(
                seat=seat,
                status=True
            ).first()

            if assignment:

                assignment.status = False
                assignment.save()

                SeatAssignment.objects.create(
                    seat=seat,
                    member=member,
                    assigned_date=timezone.localdate(),
                    status=True
                )

            return redirect("SeatManagementPage")


    members = Member.objects.filter(status=True,memberships__status=True,memberships__expiry_date__gte=timezone.localdate()).distinct()

    # Send the seat data to SeatManagement.html
    return render(
        request,
        "SeatManagement.html",
        {
            "seat_rows": seat_rows,
            "configuration": configuration,
            "selected_seat": selected_seat,
            "members": members
        }
    )






def SettingsPage(request):
    plans = MemberShipPlans.objects.all()
    configuration = SeatConfiguration.objects.first()

    if request.method == "POST":
        rows = int(request.POST.get("rows"))
        seats_per_row = int(request.POST.get("seats_per_row"))

        if configuration:
            configuration.rows = rows
            configuration.seats_per_row = seats_per_row
            configuration.save()
        else:
            configuration = SeatConfiguration.objects.create(
                rows=rows,
                seats_per_row=seats_per_row,
            )

        # Remove existing seats
        Seat.objects.all().delete()
        # Generate new seats
        for row_index in range(rows):
            row_letter = chr(ord("A") + row_index)
            for seat_number in range(1, seats_per_row + 1):
                Seat.objects.create(seat_number=f"{row_letter}{seat_number}")
        return redirect("SettingsPage")

    return render(request,"SettingsPage.html",{
            "plans": plans,
            "configuration": configuration
        }
    )






def Dashboard(request):


    update_expired_memberships()


    total_members = Member.objects.all().count()
    total_seats = Seat.objects.all().count()
    occupied_seats = Seat.objects.filter(assignments__status=True).count()               
    vacant_seats = Seat.objects.exclude(assignments__status=True).count()
    today = timezone.localdate()

    birthdays = Member.objects.filter(
    date_of_birth__month=today.month,
    date_of_birth__day=today.day,
)

    # seat------------------map
    seats = Seat.objects.all().order_by("seat_number")

    for seat in seats:

        assignment = SeatAssignment.objects.filter(
            seat=seat,
            status=True
        ).select_related("member").first()

        seat.assignment = assignment

        if assignment:

            membership = assignment.member.memberships.filter(
                status=True
            ).first()

            seat.membership = membership

            if membership:

                days_remaining = (
                    membership.expiry_date - today
                ).days

                if days_remaining <=7:
                    seat.state = "expired"
                else:
                    seat.state = "occupied"

            else:
                seat.membership = None
                seat.state = "occupied"

        else:
            seat.membership = None
            seat.state = "vacant"

 # Membership Overview

    active_memberships = Memberships.objects.filter(
        status=True,
        expiry_date__gte=today
    ).count()

    expiring_memberships = Memberships.objects.filter(
        status=True,
        expiry_date__gte=today,
        expiry_date__lte=today + timedelta(days=7)
    ).count()

    expired_memberships = Memberships.objects.filter(
        expiry_date__lt=today
    ).count()

    no_membership = Member.objects.filter(
        status=True,
        memberships__isnull=True
    ).count()




    


    return render(request,"Dashbaord.html",{
        "total_members":total_members,
        "total_seats":total_seats,
        "occupied_seats":occupied_seats,
        "vacant_seats":vacant_seats,
        "birthdays":birthdays,"seats": seats,
        "seats": seats,

        "active_memberships": active_memberships,
        "expiring_memberships": expiring_memberships,
        "expired_memberships": expired_memberships,
        "no_membership": no_membership,


    })

