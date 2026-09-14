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

