from django.db import models
from django.utils.timezone import now


# Create your models here.
class HomeNode(models.Model):
    note_id = models.IntegerField(unique=True)
    note_date = models.DateField(default=now)
    note_title = models.CharField(max_length=255)
    note = models.TextField()


class AboutInfo(models.Model):
    note_id = models.IntegerField(unique=True)
    note_date = models.DateField(default=now)
    note_title = models.CharField(max_length=255)
    note = models.TextField()


class StudentNote(models.Model):
    note_id = models.IntegerField(unique=True)
    note_date = models.DateField(default=now)
    note_title = models.CharField(max_length=255)
    note = models.TextField()


class AdminNote(models.Model):
    note_id = models.IntegerField(unique=True)
    note_date = models.DateField(default=now)
    note_title = models.CharField(max_length=255)
    note = models.TextField()



class StudentAccounts(models.Model):
    roll=models.CharField(max_length=50, unique=True)
    passwd=models.CharField(max_length=255)


class Students(models.Model):
    account=models.OneToOneField(StudentAccounts, on_delete=models.CASCADE)
    roll=models.IntegerField(unique=True)
    firstname = models.CharField(max_length=255)
    middlename=models.CharField(max_length=255, null=True, blank=True)
    lastname=models.CharField(max_length=255)
    dob=models.DateField(default=now)


class Questions(models.Model):
    ans_choices = [
        (1, 'choice1'),
        (2, 'choice2'),
        (3, 'choice3'),
        (4, 'choice4'),
    ]
    qn_no = models.IntegerField(unique=True)
    questions = models.TextField(unique=True)
    choices = models.TextField(choices=ans_choices)

    
class AdminAccount(models.Model):
    user_name = models.CharField(max_length=50, unique=True)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)


class Administrator(models.Model):
    account = models.OneToOneField(AdminAccount, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255)
    dob = models.DateField(default=now)
    username=models.CharField(max_length=255)


class ans_1234(models.Model):
    qn_no = models.IntegerField(unique=True)
    choice = models.IntegerField(null=True)
