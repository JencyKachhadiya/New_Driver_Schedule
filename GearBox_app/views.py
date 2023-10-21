from django.shortcuts import render
from Account_app.models import *
from GearBox_app.models import *
from django.conf import settings
from .models import *
from CRUD import *
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from django.contrib import messages
from django.http import Http404



# Create your views here.
def leaveReq(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'gearBox/table/LeaveReq.html', {'leave_requests': leave_requests})

def natureOfLeaves(request):
    nature_of_leaves = NatureOfLeave.objects.all()
    return render(request, 'gearBox/table/NatureOfLeaves.html', {'nature_of_leaves': nature_of_leaves})

def natureOfLeavesForm(request,id=None):
    data = None
    if id:
        try:
            data = NatureOfLeave.objects.get(id=id)
        except NatureOfLeave.DoesNotExist:
            raise Http404("NatureOfLeave does not exist")
    return render(request,'gearBox/NatureOfLeavesForm.html',{'data': data}) 

@csrf_protect
@api_view(['POST'])
def changeNatureOfLeaves(request,id=None):
    data = {
        'reason' : request.POST.get('Reason'),
    }
    if id == None:
        insert = insertIntoTable(tableName='NatureOfLeave',dataSet=data)
        messages.success(request,'Adding successfully')
    else:
        update = updateIntoTable(id,tableName='NatureOfLeave',dataSet=data)
        messages.success(request, 'Updating successfully')
    return redirect('gearBox:natureOfLeaves')

def leaveReqForm(request,id=None):
    natureOfLeaves = NatureOfLeave.objects.all()
    drivers = Driver.objects.all()
    params = {
            "natureOfLeaves" : natureOfLeaves,
            "drivers" : drivers,
        }
    if id:
        data = LeaveRequest.objects.get(id=id)
        data.start_date = dateConverterFromTableToPageFormate(data.start_date)
        data.end_date = dateConverterFromTableToPageFormate(data.end_date)
        params["data"] = data
        
    return render(request,'gearBox/LeaveReqForm.html',params)
        
@csrf_protect
@api_view(['POST'])
def changeLeaveRequest(request,id=None):
    
    employee = Driver.objects.get(driverId = request.POST.get('driverId'))
    reason = NatureOfLeave.objects.get(id = request.POST.get('Reason'))
    
    data = {
        'employee' : employee,
        'start_date' : request.POST.get('StartDate'),
        'end_date' : request.POST.get('EndDate'),
        'reason' :reason,
    }
    if id == None:
        data['status'] = 'Pending'
        insert = insertIntoTable(tableName='LeaveRequest',dataSet=data)
        messages.success(request,'Adding successfully')
    else:
        data['status'] = request.POST.get('Status')
        update = updateIntoTable(record_id=id,tableName='LeaveRequest',dataSet=data)
        messages.success(request,'Updated successfully')
        
        
    return redirect('gearBox:leaveReq')


def driversView(request):
    drivers = Driver.objects.all()
    params = {
        'drivers' : drivers
    }
    return render(request,'GearBox/table/driverTable.html',params)


def driverForm(request, id=None):
    data = None
    if id:
        data = Driver.objects.get(pk = id)   
    params = {
        'data' : data
    }
    return render(request, 'GearBox/driverForm.html',params)


@csrf_protect
@api_view(['POST'])
def driverFormSave(request, id= None):
    dataList = {
        'driverId' : request.POST.get('driverId'),
        'name' : request.POST.get('name'),
        'phone' : request.POST.get('phone'),
        'email' : request.POST.get('email')
    }
    if id:
        updateIntoTable(record_id=id,tableName='Driver',dataSet=dataList)
        messages.success(request,'Updated successfully')
    else:
        insertIntoTable(tableName='Driver',dataSet=dataList)
        messages.success(request,'Adding successfully')

    return redirect('gearBox:driversTable')
