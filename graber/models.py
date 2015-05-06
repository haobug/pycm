# -*- coding: utf-8 -*-
from django.db import models
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return '%s' % self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    department_id = models.ForeignKey(Department)
    def __str__(self):
        return '%s' % self.name

class Employee(models.Model):
    email = models.CharField(max_length=1024)
    name =  models.CharField(max_length=200)
#    nick = models.CharField(max_length=200,null=True)
#    name_en = models.CharField(max_length=200,null=True)
    team_id = models.ForeignKey(Team,null=True)
    def display(self):
        return self

    def __str__(self):
        return '%s<%s>' % (self.name, self.email)

class Community(models.Model):
    name = models.CharField(max_length=200)
    review_base = models.CharField(max_length=2048)
    enabled = models.BooleanField(default=True)
    def __str__(self):
        return '%s' % self.name

class Contribution(models.Model):
    employee_id = models.ForeignKey(Employee)
    review_id = models.IntegerField()
    community_id = models.ForeignKey(Community)
    merge_date = models.DateTimeField(null=True)

#class Question(models.Model):
#    question_text = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
