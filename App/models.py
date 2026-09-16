from django.db import models

# Create your models here.



class Member(models.Model):
    full_name = models.CharField(max_length=100)
    MemberID = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    joined_date = models.DateField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["MemberID"],
                condition=models.Q(MemberID__isnull=False),
                name="unique_member_id")
            ]
        
    def __str__(self):
        return self.full_name

class MemberShipPlans(models.Model):
    Plan_Name = models.CharField(max_length=100)
    Duration  = models.PositiveIntegerField()
    Plan_price = models.PositiveIntegerField()
    Plan_Status = models.BooleanField(default=True)

    
    def __str__(self):
        return self.Plan_Name



class Memberships(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE, related_name="memberships")
    plan = models.ForeignKey(MemberShipPlans, on_delete=models.PROTECT)
    start_date = models.DateField()
    expiry_date = models.DateField()
    status = models.BooleanField(default=True)
    amount = models.PositiveIntegerField()
    Payment_Status = models.BooleanField(default = False)
    Payment_Date = models.DateField(null=True, blank=True)



class Seat(models.Model):
    seat_number = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.seat_number

class SeatAssignment(models.Model):
    seat = models.ForeignKey(Seat,on_delete=models.PROTECT,related_name="assignments")
    member = models.ForeignKey(Member,on_delete=models.CASCADE,related_name="seat_assignments")
    assigned_date = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.seat.seat_number} - {self.member.full_name}"




class SeatConfiguration(models.Model):
    rows = models.PositiveIntegerField(default=1)
    seats_per_row = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "Seat Configuration"
