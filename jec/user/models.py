from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, name,   password, **extra_fields):
        values = [username, name]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        user = self.model(
            username=username,
            name=name, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, name, password, **extra_fields)

    def create_superuser(self, username, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, name, password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):

    username=models.CharField(primary_key=True,max_length=20)
    name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined=models.DateTimeField( auto_now=False, auto_now_add=True)
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        PROFESSOR = " PROFESSOR", " Professor"

    base_role = Role.STUDENT
    role = models.CharField(max_length=50, choices=Role.choices)
    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS=['name','role']

    # def __str__(self):
    #     return self.username

    # def save(self, *args, **kwargs):
    #     # if not self.pk:
    #     #     self.role = self.base_role
    #         return super().save(*args, **kwargs)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):

    base_role = User.Role.STUDENT

    student = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for students"


# @receiver(post_save, sender=Student)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "STUDENT":
#         StudentProfile.objects.create(user=instance)


class StudentProfile(models.Model):
    SEMESTER_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    )

    CATEGORY_CHOICES=(
    ("1", "GEN"),
    ("2", "OBC"),
    ("3", "EWS"),
    ("4", "SC"),
    ("5", "ST"),
    )

    BRANCH_CHOICES=(
    ("1", "cS"),
    ("2", "IT"),
    ("3", "EE"),
    ("4", "EC"),
    ("5", "MECH"),
    ("6", "CIVIL"),
    ("7", "IP"),
    ("8", "AI"),
    ("9","DS"),
    )

    BLOOD_CHOICES=(
    ("1", "A+"),
    ("2", "A-"),
    ("3", "B+"),
    ("4", "B-"),
    ("5", "O+"),
    ("6", "O-"),
    ("7", "AB+"),
    ("8", "AB-"),
    )

    STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),
    ("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),
    ("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),
    ("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),
    ("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),
    ("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),
    ("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),
    ("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
    ("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),
    ("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

    YEAR_CHOICES = [(r,r) for r in range(1984, datetime.date.today().year)]

    rollno = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=30,blank=False)
    semester = models.CharField(
        max_length = 5,
        choices = SEMESTER_CHOICES,
        blank=False
        )
    contact= models.IntegerField(blank=False)
    category= models.CharField(
        max_length = 7,
        choices = CATEGORY_CHOICES,
        blank=False
        )
    income= models.IntegerField(blank=False)
    dob=models.DateField(blank=False)
    father=models.CharField(max_length=30,blank=False)
    mother=models.CharField(max_length=30,blank=False)
    religion=models.CharField(max_length=10,blank=False)
    branch=models.CharField(
        max_length = 7,
        choices = BRANCH_CHOICES,
        blank=False
        )
    bloodGroup=models.CharField(
        max_length = 5,
        choices = BLOOD_CHOICES,
        blank=False
        )
    permanentAddress=models.TextField(blank=False)
    temporaryAddress=models.TextField(blank=False)
    state=models.CharField(
        max_length=35,
        choices = STATE_CHOICES,
        blank=False
        )
    city=models.CharField(max_length=20,blank=False)
    pincode=models.IntegerField(blank=False)
    admYear=models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    # objects=models.Manager()

    
    def calculate_age(self):
        bd = self.birthday
        if bd:
            td = datetime.today()
            return td.year - bd.year - ((td.month, td.day) < (bd.month, bd.day))

    # def __str__(self):
    #     # Built-in attribute of django.contrib.auth.models.User !
    #     return self.user.username


class  ProfessorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role. PROFESSOR)


class  Professor(User):

    base_role = User.Role. PROFESSOR

    professor =  ProfessorManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for  professors"


class  ProfessorProfile(models.Model):
    CATEGORY_CHOICES=(
    ("1", "GEN"),
    ("2", "OBC"),
    ("3", "EWS"),
    ("4", "SC"),
    ("5", "ST"),
    )

    DEPT_CHOICES=(
        ("1", "CS"),
        ("2", "IT"),
        ("3", "EE"),
        ("4", "EC"),
        ("5", "MECH"),
        ("6", "CIVIL"),
        ("7", "IP"),
        ("8", "PHY"),
        ("9","CHEM"),
        ("10","MATHS"),
        ("11","OTHER")
        )

    BLOOD_CHOICES=(
        ("1", "A+"),
        ("2", "A-"),
        ("3", "B+"),
        ("4", "B-"),
        ("5", "O+"),
        ("6", "O-"),
        ("7", "AB+"),
        ("8", "AB-"),
        )

    STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),
        ("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),
        ("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),
        ("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),
        ("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),
        ("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),
        ("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),
        ("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
        ("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),
        ("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

    user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=30,blank=False)
    dept=models.CharField(
        max_length = 5,
        choices = DEPT_CHOICES,
        blank=False
        )
    state=models.CharField(
        max_length=35,
        choices = STATE_CHOICES,
        blank=False
        )
    category= models.CharField(
        max_length = 7,
        choices = CATEGORY_CHOICES,
        blank=False
        )
    bloodGroup=models.CharField(
        max_length = 5,
        choices = BLOOD_CHOICES,
        blank=False
        )
    temporaryAddress=models.TextField(blank=False)
    # objects=models.Manager()

# @receiver(post_save, sender= Professor)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == " PROFESSOR":
#          ProfessorProfile.objects.create(user=instance)
