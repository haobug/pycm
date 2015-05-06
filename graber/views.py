from django.shortcuts import render
from django.http import HttpResponse
from graber.models import Department, Team, Employee, Community, Contribution
# use system-wide one, uncomment for debug purpose only
#import sys
#import os
#sys.path.append(os.path.abspath('./pygerrit'))
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import pil

from requests.auth import HTTPDigestAuth
from pygerrit.rest import GerritRestAPI
from pygerrit import escape_string
from urllib import urlencode
import time
from requests import HTTPError
from django.db import connection

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def average(value):
    output = "Hello, average: %s" % ( value)
    total = get_contribution_total(value)
    emp_count = get_employee_count(value)
    output += "<br/>\nTotal: %d" % (total)
    output += "<br/>\nEmployees: %d" % (emp_count)
    if total == 0 or emp_count == 0:
        avg = 0
    else:
        avg = total / emp_count
    output += "<br/>\nAverage: %d" % (avg)
    return HttpResponse(output)

def get_employee_count(value):
    cursor = connection.cursor()
    sql="""SELECT count(id) FROM graber_employee
            WHERE team_id_id in (
		SELECT id FROM graber_team
		WHERE UPPER(name)=UPPER(%s)
		union all
		SELECT id FROM graber_team
		WHERE department_id_id==(SELECT id FROM graber_department
			WHERE UPPER(name)=UPPER(%s))
            )"""
    return int("%d" % cursor.execute(sql, [value, value]).fetchone())

def get_contribution_total(value):
    cursor = connection.cursor()
    sql = """SELECT count(*) as count FROM graber_contribution
        WHERE employee_id_id in (SELECT id FROM graber_employee
            WHERE team_id_id in (
                SELECT id FROM graber_team
                    WHERE UPPER(name)=UPPER(%s)
                union all
                SELECT id FROM graber_team
                    WHERE department_id_id==(SELECT id FROM graber_department
                        WHERE UPPER(name)=UPPER(%s)
                    )
            )
        )"""
    #output += sql
    return int("%d" % cursor.execute(sql, [value, value]).fetchone())

def summary(value):
    output = "Hello, summary: %s" % ( value)
    count = get_contribution_total(value)
    output += "<br/>\nTotal: %d" % count
    return HttpResponse(output)

def respond_pic(name,value):
    file = pil.get_pic(name, value)
    if file:
        response = HttpResponse(content_type="image/png")
        image = Image.open(file)
        image.save(response, "PNG")
    return response

def summary_pic(value):
    #output = "Hello, summary_pic: %s" % ( value)
    count = get_contribution_total(value)
    #output= """<img src="%s"/>""" % file
    #return HttpResponse(output)
    return respond_pic(value, count)

def average_pic(value):
    output = "Hello, average_pic: %s" % ( value)
    total = get_contribution_total(value)
    emp_count = get_employee_count(value)
    output += "<br/>\nTotal: %d" % (total)
    output += "<br/>\nEmployees: %d" % (emp_count)
    if total == 0 or emp_count == 0:
        avg = 0
    else:
        avg = total / emp_count
    return respond_pic(value, avg)


def query(request,category,value):
    category = category.lower()
    value_query = value
    if '/' in value:
        value_query = value.split('/')[-1]
    ext=''
    if '.' in value_query:
        ext = value_query.split('.')[-1]
        value_query = value_query.split('.')[0]
    if ext:
        switch = {
            'avg': average_pic,
            'sum': summary_pic,
            'all': summary_pic}
    else:
        switch = {
            'avg': average,
            'sum': summary,
            'all': summary}
    return switch[category](value_query)
    #return HttpResponse("Hello, query: %s=%s" % (category, value))

def update(request):
    output=""
    for emp in Employee.objects.order_by('email'):
        if not emp.team_id:
            continue
        output += '' + str('<h1>%s</h1>' % emp.name)
        for comm in Community.objects.order_by('name'):
            if not comm.enabled :
                continue
            output += '<h2>%s</h2>' % comm.name
            #rest = GerritRestAPI(url='http://review.cyanogenmod.org/')
            rest = GerritRestAPI(url=comm.review_base)
            output += "%s<br/>\n" % emp.email
            query_url ="/changes/?q=owner:"+emp.email+"+status:merged"
            output +=  query_url  + "<br/>\n" 
            changes=''
            try:
                #proxies = {
                #    "http": "http://127.0.0.1:8087",
                #    "https": "https://127.0.0.1:8087",
                #}
                #changes = rest.get(query_url, proxies=proxies)
                changes = rest.get(query_url)
            except HTTPError as he:
                output += '' + str(he.message)
            output += time.strftime('%Y-%m-%d %H:%M:%S') + "==> %d changes<br/>\n" % len(changes)
            for change in changes:
                subject = str(change['subject'])
                num =  str(change['_number'])
                date =  str(change['updated'])

                q = Contribution.objects.filter(employee_id=emp,review_id=num, community_id=comm)
                if len(q) < 1:
                    cont = Contribution(employee_id=emp,review_id=num, community_id=comm, merge_date=date)
                    cont.save()
                else:
                    continue
                output += "<br/>\n" 
                output += subject
                output += "<br/>\n" 
                output += comm.review_base + num
                output += "<br/>\n" 
                time.sleep(1)
    return HttpResponse(output)
