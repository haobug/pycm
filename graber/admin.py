# -*- coding: utf-8 -*-
from django.contrib import admin
from graber.models import Department, Team, Employee, Community, Contribution
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Register your models here.
admin.site.register(Department)

class TeamAdmin(admin.ModelAdmin):
    fields = ['name', 'department_id']
    list_display = fields
admin.site.register(Team, TeamAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'team_id']
    list_display = ('display', 'team_id')
    search_fields = ['email', 'name']
    
admin.site.register(Employee,EmployeeAdmin)

class CommunityAdmin(admin.ModelAdmin):
    fields = ['name', 'review_base','enabled']
    list_display = fields
    
admin.site.register(Community, CommunityAdmin)

class ContributionAdmin(admin.ModelAdmin):
    fields = ['employee_id', 'review_id', 'community_id']
    list_display = fields

admin.site.register(Contribution, ContributionAdmin)

