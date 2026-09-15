from django.contrib import admin

from .models import (
    Member,
    MemberShipPlans,
    Memberships,
    Seat,
    SeatAssignment,
    SeatConfiguration,
)


# =========================================================
# MEMBER
# =========================================================

class MemberAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "MemberID",
        "phone",
        "joined_date",
        "status",
    )

    list_filter = (
        "status",
        "joined_date",
    )

    search_fields = (
        "full_name",
        "MemberID",
        "phone",
        "email",
    )


# =========================================================
# MEMBERSHIP PLANS
# =========================================================

class MemberShipPlansAdmin(admin.ModelAdmin):

    list_display = (
        "Plan_Name",
        "Duration",
        "Plan_price",
        "Plan_Status",
    )

    list_filter = (
        "Plan_Status",
    )

    search_fields = (
        "Plan_Name",
    )


# =========================================================
# MEMBERSHIPS
# =========================================================

class MembershipsAdmin(admin.ModelAdmin):

    list_display = (
        "member",
        "plan",
        "start_date",
        "expiry_date",
        "status",
    )

    list_filter = (
        "status",
        "plan",
        "start_date",
        "expiry_date",
    )

    search_fields = (
        "member__full_name",
        "member__MemberID",
    )


# =========================================================
# SEATS
# =========================================================

class SeatAdmin(admin.ModelAdmin):

    list_display = (
        "seat_number",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "seat_number",
    )


# =========================================================
# SEAT ASSIGNMENTS
# =========================================================

class SeatAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "seat",
        "member",
        "assigned_date",
        "status",
    )

    list_filter = (
        "status",
        "assigned_date",
    )

    search_fields = (
        "seat__seat_number",
        "member__full_name",
        "member__MemberID",
    )


# =========================================================
# SEAT CONFIGURATION
# =========================================================

class SeatConfigurationAdmin(admin.ModelAdmin):

    list_display = (
        "rows",
        "seats_per_row",
    )


# =========================================================
# REGISTER MODELS
# =========================================================

admin.site.register(Member, MemberAdmin)
admin.site.register(MemberShipPlans, MemberShipPlansAdmin)
admin.site.register(Memberships, MembershipsAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(SeatAssignment, SeatAssignmentAdmin)
admin.site.register(SeatConfiguration, SeatConfigurationAdmin)