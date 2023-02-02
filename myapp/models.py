from django.db import models

# Create your models here.
class Hiace(models.Model):
    hiace_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    name_seats = models.TextField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.hiace_name

class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    userid =models.DecimalField(decimal_places=0, max_digits=2)
    hiaceid=models.DecimalField(decimal_places=0, max_digits=2)
    hiace_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    name_seats = models.TextField(null=True)
    hiace = models.ForeignKey(Hiace, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=255)

    def update_name_seats(self, selected_seats):
        # convert both data into list of strings
        hiace_seats = self.hiace.name_seats.split(',')
        selected_seats = selected_seats.split(',')

        # filter the data from hiace_seats that is present in selected_seats
        filtered_seats = [seat for seat in hiace_seats if seat in selected_seats]

        # join the filtered_seats back into a string and save it in name_seats field
        self.name_seats = ','.join(filtered_seats)
        self.save()        

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email