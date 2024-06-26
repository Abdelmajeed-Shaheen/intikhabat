from django.db import models


class Governorate(models.Model):

    name=models.CharField(max_length=50)
    timestamp=models.DateTimeField(auto_now=True, auto_now_add=False)
    updated=models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name
class Department(models.Model):
    name=models.CharField(max_length=50)
    governorate=models.ForeignKey(Governorate,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True, auto_now_add=False)
    updated=models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return (self.name+"/"+self.governorate.name)

class Area(models.Model):
    name=models.CharField(max_length=50)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    sector=models.ForeignKey("Sector", on_delete=models.SET_NULL,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now=True, auto_now_add=False)
    updated=models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name    

class District(models.Model):

    name=models.CharField(max_length=50)
    description=models.TextField(null=True)
    timestamp=models.DateTimeField(auto_now=True, auto_now_add=False)
    updated=models.DateTimeField(auto_now=False, auto_now_add=True)
    area=models.ForeignKey(Area,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name

class Street(models.Model):

    name=models.CharField(max_length=50)
    description=models.TextField(null=True)
    timestamp=models.DateTimeField(auto_now=True, auto_now_add=False)
    updated=models.DateTimeField(auto_now=False, auto_now_add=True)
    district=models.ForeignKey(District,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name


class Address(models.Model):

    governorate=models.ForeignKey(Governorate,on_delete=models.CASCADE)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True)
    area=models.ForeignKey(Area,on_delete=models.CASCADE,null=True,blank=True)
    district=models.ForeignKey(District,on_delete=models.CASCADE,null=True,blank=True)
    street=models.ForeignKey(Street,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return (self.governorate.name+"/"+self.department.name)


class ElectionAddress(models.Model):
    governorate=models.ForeignKey(Governorate, on_delete=models.CASCADE)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.governorate.name+"/"+self.department.name)


class Sector(models.Model):
    governorate=models.ForeignKey(Governorate, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Residence(models.Model):
    governorate=models.ForeignKey(Governorate,on_delete=models.CASCADE)
    area=models.ForeignKey(Area, on_delete=models.CASCADE)
    district=models.ForeignKey(District, on_delete=models.CASCADE)
    sector=models.ForeignKey(Sector, on_delete=models.CASCADE)


    
