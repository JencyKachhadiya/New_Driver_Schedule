from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import shutil, os, colorama, subprocess, csv, re, pytz
from django.views.decorators.csrf import csrf_protect
from datetime import datetime , time, timedelta, timezone
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
from Account_app.models import *
from GearBox_app.models import *
from Appointment_app.models import *
from django.http import FileResponse
from CRUD import *
from .models import RCTI
from Account_app.reconciliationUtils import *
from django.urls import reverse
from django.db.models import Q
from itertools import chain

from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'Account/dashboard.html')

def getForm1(request):
    if request.user.is_authenticated:
        params = {}
        driver = Driver.objects.filter(email=request.user.email).first()
        if driver:
            driver_id = str(driver.driverId) + '-' + str(driver.name)
            preStart_data = PreStart.objects.filter(curDate__date=date.today(), driver=driver).first()
            if preStart_data:
                existingTodayTrip = DriverTrip.objects.filter(driverId=driver, partially=True).first()
                if existingTodayTrip:
                    existingTodayTrip.shiftDate = dateConverterFromTableToPageFormate(existingTodayTrip.shiftDate)
                    params['existingTodayTrip'] = existingTodayTrip
            
                params['driver_ids'] = driver_id
            else:
                messages.error(request,'Please fill up Pre-start first.')
                return redirect('Account:timeOfStart') 
        else:
            params['client_ids'] =  Client.objects.values_list('name', flat=True).distinct()
            params['admin_truck_no'] =  AdminTruck.objects.values_list('adminTruckNumber', flat=True).distinct()
            params['client_truck_no'] =  ClientTruckConnection.objects.values_list('clientTruckId', flat=True).distinct()
            params['drivers'] = Driver.objects.all()
            
        return render(request, 'Trip_details/form1.html', params)
    else:
        return redirect('login')

def getForm2(request, id=None):
    if not id:
        params = {
            'loads': [i+1 for i in range(int(request.session['data'].get('numberOfLoads')))]
        }
    else:
        dockets = DriverDocket.objects.filter(tripId=id)
        params = {
            'dockets': dockets
        }
        
    return render(request, 'Trip_details/Form2.html', params)

def createFormSession(request):
    loadSheet = request.FILES.get('loadSheet')
    driverId = request.POST.get('driverId').split('-')[0]
    truckNo = request.POST.get('truckNum').split('-')[0]
    driverObj = Driver.objects.filter(pk=driverId).first()
    existingTodayTrip = DriverTrip.objects.filter(driverId=driverObj, shiftDate=request.POST.get('shiftDate'), truckNo=truckNo, partially=True).first()
    if existingTodayTrip:
        existingTodayTrip.dispute = True if request.POST.get('dispute') == 'dispute' else False
        existingTodayTrip.save()
    
    data = {}  
    clientName = request.POST.get('clientName')
    if loadSheet:
        load_sheet_folder_path = 'Temp_Load_Sheet'
        fileName = loadSheet.name.replace(" ", "").replace("\t", "")
        time = getCurrentTimeInString()

        load_sheet_new_filename = 'Load_Sheet' + time + '!_@' + fileName
        lfs = FileSystemStorage(location=load_sheet_folder_path)
        lfs.save(load_sheet_new_filename, loadSheet)
           
        data = {
            'driverId': request.POST.get('driverId').split('-')[0],
            'clientName': clientName,
            'truckNum': truckNo,
            'startTime': request.POST.get('startTime'),
            'endTime': request.POST.get('endTime'),
            'shiftDate': request.POST.get('shiftDate'),
            'shiftType': request.POST.get('shiftType'),
            'numberOfLoads': request.POST.get('numberOfLoads'),
            'comments': request.POST.get('comments'),
        }
        
    data['docketGiven'] = not Client.objects.get(name=clientName).docketGiven,
    data['docketGiven'] =  not Client.objects.get(name=clientName).docketGiven,
    data['loadSheet'] = load_sheet_new_filename
    
    request.session['data'] = data
       
    if Client.objects.get(name=clientName).docketGiven:
        return redirect('Account:formsSave') 
    elif existingTodayTrip:
        return redirect('Account:existingForm2', id=existingTodayTrip.id)
    else:
        return redirect('Account:getForm2')

# @csrf_protect
# @api_view(['POST'])
def formsSave(request):
    driverId = request.session['data']['driverId']
    clientName = Client.objects.get(name=request.session['data']['clientName'])
    shiftType = request.session['data']['shiftType']
    numberOfLoads = request.session['data']['numberOfLoads']
    truckNo = request.session['data']['truckNum']
    startTime = request.session['data']['startTime']
    endTime = request.session['data']['endTime']
    shiftDate = request.session['data']['shiftDate']
    loadSheet = request.session['data']['loadSheet']
    comment = request.session['data']['comments']
    temp_loadSheet = ''
    Docket_no, Docket_file = [], []
    time = getCurrentTimeInString()
    driver = Driver.objects.get(driverId=driverId)
    comment2 = request.POST.get('comments')
    
    existingTodayTrip = DriverTrip.objects.filter(driverId=driver, shiftDate=shiftDate, truckNo=truckNo, partially=True).first()
        
    if not os.path.exists('static/img/finalloadSheet/' + loadSheet):
        shutil.move('Temp_Load_Sheet/' + loadSheet, 'static/img/finalloadSheet/' + loadSheet)
        
    if not existingTodayTrip:
        if not request.session['data']['docketGiven']:
            for i in range(1, int(numberOfLoads)+1):
                key = f"docketNumber[{i}]"
                docket_number = request.POST.get(key)
                Docket_no.append(docket_number)
                key_files = f"docketFile[{i}]"
                docket_files = request.FILES.get(key_files)
                temp_loadSheet = temp_loadSheet + '-' + docket_number
                if docket_files:
                    fileName = docketFileSave(docket_files, docket_number, returnVal='file_name')
                    Docket_file.append(fileName)

        tripObj = DriverTrip()
        tripObj.driverId=driver
        tripObj.clientName=clientName
        tripObj.shiftType=shiftType
        tripObj.numberOfLoads=numberOfLoads
        tripObj.truckNo=truckNo
        tripObj.startTime=startTime
        tripObj.endTime=endTime
        tripObj.loadSheet = f'static/img/finalloadSheet/{loadSheet}'
        tripObj.comment=comment
        tripObj.shiftDate=shiftDate  
        tripObj.save()

        if not request.session['data']['docketGiven']:
            BasePlantVal = BasePlant.objects.get_or_create(basePlant="NOT SELECTED")[0]
            for i in range(len(Docket_no)):
                docket_ = DriverDocket(
                    tripId=tripObj,
                    docketNumber=Docket_no[i],
                    docketFile='static/img/docketFiles/' + Docket_file[i],
                    basePlant=BasePlantVal
                )
                docket_.surcharge_type = Surcharge.objects.get_or_create(surcharge_Name = 'No Surcharge')[0]
                docket_.save()

    else:
        existingTodayTrip.loadSheet = f'static/img/finalloadSheet/{loadSheet}'
        existingTodayTrip.comment=comment
        existingTodayTrip.shiftDate=shiftDate        
        existingTodayTrip.partially = False
        existingTodayTrip.comment2 = comment2
        existingTodayTrip.save()
        
    del request.session['data']

    messages.success(request, "Form Successfully Filled Up")
    return redirect('index')


def assignedJobShow(request):
    driverObj = Driver.objects.filter(name = request.user.username).first()
    today = date.today()
    preStart_data = PreStart.objects.filter(curDate__date=today, driver=driverObj).first()

    if preStart_data:
        appointmentObjs = Appointment.objects.filter(Start_Date_Time__date=today,appointmentdriver__driverName__name=driverObj.name).order_by('Start_Date_Time')
        indian_timezone = pytz.timezone('Asia/Kolkata')
        
        currentTime = datetime.now(tz=indian_timezone)

        for obj in appointmentObjs:
            if obj.Status != "Dispatched":
                maxTime = obj.Start_Date_Time + timedelta(minutes=20)
                minTime = obj.Start_Date_Time - timedelta(minutes=20)
                # print(f"startTime:{obj.Start_Date_Time}, max:{maxTime}, min:{minTime}, Current:{datetime.now(tz=indian_timezone)}\n")
                if obj.Status != "Complete" and  str(currentTime) > str(maxTime):
                    obj.lateForStart = True   
                elif obj.Status != "Complete" and  str(currentTime) < str(minTime): 
                    obj.notAcceptable = True  
                
        params = {'jobs':appointmentObjs}
        return render(request, 'Trip_details/assignedJobs.html',params)
    else:
        messages.error(request,'Please fill up Pre-start first.')
        return redirect('Account:timeOfStart')



def assignedJobAccept(request,id):
    # Check wether any job is currently open or not start
    driverObj = Driver.objects.filter(name = request.user.username).first()
    driverAppointments = AppointmentDriver.objects.filter(driverName = driverObj)
    jobs = 0
    today_date = timezone.now().date()
    preStart_data = PreStart.objects.filter(curDate__date=today_date, driver=driverObj).first()
    
    if preStart_data:
        for obj in driverAppointments:
            if obj.appointmentId.Status == "Dispatched":
                jobs += 1 
        if jobs > 0 :
            messages.error(request,'Please finish your current job before starting a new one.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        # Check wether any job is currently open or not end
        appObj = Appointment.objects.filter(pk=id).first()
        appObj.Status = "Dispatched"
        appObj.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request,'You have to filled up pre-start first.')
        return redirect(request.META.get('HTTP_REFERER'))
        
        
def singleJobView(request,id):
    job = Appointment.objects.filter(pk=id).first()
    driver = AppointmentDriver.objects.filter(appointmentId = job).first()
    truck = AppointmentTruck.objects.filter(appointmentId = job).first()
    indian_timezone = pytz.timezone('Asia/Kolkata')
    currentTime = datetime.now(tz=indian_timezone)
    maxTime = job.Start_Date_Time + timedelta(minutes=20)
    minTime = job.Start_Date_Time - timedelta(minutes=20)

    if job.Status != "Complete" and  str(currentTime) > str(maxTime):
        job.lateForStart = True   
    if job.Status != "Complete" and  str(currentTime) < str(minTime): 
        job.notAcceptable = True   
    
    params = {
        'job':job,
        'driver':driver,
        'truck':truck
    }
    return render(request,'Trip_details/jobView.html',params)

# @login_required
def openJobShow(request):
    driverObj = Driver.objects.filter(name = request.user.username).first()
    driverAppointments = AppointmentDriver.objects.filter(driverName = driverObj)
    jobs = []
    for obj in driverAppointments:
        print(obj.appointmentId.Status)
        if obj.appointmentId.Status == "Dispatched":
            jobs.append(obj.appointmentId)
            
    params = {'jobs':jobs}    
    return render(request, 'Trip_details/openJobs.html',params)
    
def finishJob(request, id):
    if id:
        appObj = Appointment.objects.filter(pk=id).first()
        if not appObj.stop.docketGiven:
            return redirect('Account:uploadDocketView', id)
        else:
            return redirect('Account:getHolcimTripDataView', id)

@login_required
def uploadDocketView(request,id):
    params = {'id':id}
    return render(request, 'Trip_details/uploadDocket.html',params)

@csrf_protect
def uploadDocketSave(request, id):
    appointmentObj = Appointment.objects.filter(pk=id).first()
    startDateObj = datetime.strptime(str(appointmentObj.Start_Date_Time), "%Y-%m-%d %H:%M:%S%z")
    endDateObj = datetime.strptime(str(appointmentObj.End_Date_Time), "%Y-%m-%d %H:%M:%S%z")
    AppointmentTruckObject = AppointmentTruck.objects.filter(appointmentId = appointmentObj).first()

    docketFile = request.FILES.get('docketImage')
    docketNumber = request.POST.get('docketNumber')
    comment = request.POST.get('comment')
    driverObj = Driver.objects.filter(name = request.user.username).first()
    
    # Trip save start
    tripObj = DriverTrip.objects.filter(driverId = driverObj, shiftDate=startDateObj.date(),clientName = appointmentObj.stop).first()
    if not tripObj:
        tripObj = DriverTrip()
        tripObj.driverId = driverObj
        tripObj.clientName = appointmentObj.stop
        tripObj.shiftType = appointmentObj.shiftType
        tripObj.truckNo = AppointmentTruckObject.truckNo.adminTruckNumber
        tripObj.shiftDate = startDateObj.date()
        
    tripObj.partially = True
    startTime = tripObj.startTime
    endTime = tripObj.endTime
    time_pattern = re.compile(r'^\d{2}:\d{2}$')
    
    if time_pattern.match(startTime):
        startTime = startTime+":00"
    if time_pattern.match(endTime):
        startTime = startTime+":00"

    # Set startTime  
    if not startTime:
        tripObj.startTime = startDateObj.time()
    else:
        if not isinstance(startTime, datetime):
            startTime = datetime.strptime(startTime, "%H:%M:%S")
        if startTime.time() < startDateObj.time():
            tripObj.startTime = startDateObj.time()
    # Set startTime  

    # Set endTime 
    if not endTime:
        tripObj.endTime = endDateObj.time()
    else:
        if not isinstance(endTime, datetime):
            endTime = datetime.strptime(endTime, "%H:%M:%S")
        if endTime.time() < endDateObj.time():
            tripObj.endTime = endDateObj.time()
    # Set endTime
    
    tripObj.save()    
    # Trip save end

    # Docket save start
    docketObj = DriverDocket.objects.filter(tripId = tripObj ,docketNumber=docketNumber).first()
    if docketObj:
        messages.error(request, "This docket is already exist, please check docket number.")
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        docketObj = DriverDocket()
        docketObj.docketNumber = docketNumber
        if docketFile:
            docketObj.docketFile = docketFileSave(docketFile, docketNumber)
        
        docketObj.basePlant = appointmentObj.Origin
        docketObj.comment = comment
        docketObj.tripId = tripObj
        docketObj.shiftDate = startDateObj.date()

        docketObj.surcharge_type = Surcharge.objects.filter(surcharge_Name = "No Surcharge").first()

        tripObj.numberOfLoads += 1
        tripObj.save()

        docketObj.save()
        
    # Docket save end

    appointmentObj.Status = "Complete"
    appointmentObj.save()
    messages.success(request, "Docket Updated")
    
    return redirect('Account:assignedJobShow')

@login_required
def getHolcimDataView(request,id):
    params = {'id':id}
    return render(request, 'Trip_details/getHolcimData.html',params)

@login_required
def getHolcimDataSave(request,id):
    appointmentObj = Appointment.objects.filter(pk=id).first()
    startDateObj = datetime.strptime(str(appointmentObj.Start_Date_Time), "%Y-%m-%d %H:%M:%S%z")
    endDateObj = datetime.strptime(str(appointmentObj.End_Date_Time), "%Y-%m-%d %H:%M:%S%z")
    AppointmentTruckObject = AppointmentTruck.objects.filter(appointmentId = appointmentObj).first()
    driverObj = Driver.objects.filter(name = request.user.username).first()
    
    tripObj = DriverTrip.objects.filter(driverId = driverObj, shiftDate=startDateObj.date(),clientName = appointmentObj.stop).first()
    if not tripObj:
        tripObj = DriverTrip()
        tripObj.driverId = driverObj
        tripObj.clientName = appointmentObj.stop
        tripObj.shiftType = appointmentObj.shiftType
        tripObj.truckNo = AppointmentTruckObject.truckNo.adminTruckNumber
        tripObj.numberOfLoads = 1
        tripObj.shiftDate = startDateObj.date()
    else:
        tripObj.numberOfLoads += 1

    tripObj.partially = True
    startTime = tripObj.startTime
    endTime = tripObj.endTime
    time_pattern = re.compile(r'^\d{2}:\d{2}$')
    
    if time_pattern.match(startTime):
        startTime = startTime+":00"
    if time_pattern.match(endTime):
        startTime = startTime+":00"
    
    # Set startTime  
    if not startTime:
        tripObj.startTime = startDateObj.time()
    else:
        if not isinstance(startTime, datetime):
            startTime = datetime.strptime(startTime, "%H:%M:%S")
        if startTime.time() < startDateObj.time():
            tripObj.startTime = startDateObj.time()
    # Set startTime  

    # Set endTime 
    if not endTime:
        tripObj.endTime = endDateObj.time()
    else:
        if not isinstance(endTime, datetime):
            endTime = datetime.strptime(endTime, "%H:%M:%S")
        if endTime.time() < endDateObj.time():
            tripObj.endTime = endDateObj.time()
    # Set endTime
    
    tripObj.save()    
    # Trip save end

    appointmentObj.Status = "Complete"
    appointmentObj.save()
    messages.success(request, "Docket Updated")
    return redirect('Account:assignedJobShow')

def timeOfStart(request):
    today_date = timezone.now().date()
    driver = Driver.objects.filter(email=request.user.email).first()

    preStart_data = PreStart.objects.filter(curDate__date=today_date, driver=driver).first()
    if not preStart_data:
        return render(request, 'Trip_details/pre-startForm.html')
    else:
        messages.error(request, "You already filled Pre-start.")
        return redirect(request.META.get('HTTP_REFERER'))


@csrf_protect 
def timeOfStartSave(request):
    driver = Driver.objects.filter(email=request.user.email).first()
    if driver:
        preStart_data = PreStart.objects.filter(curDate__date=datetime.now().date(), driver=driver).first()

        if not preStart_data:
            dataSet = {
                'fitForWork' : True if request.POST.get('fitForWork') == 'Yes' else False,
                'vehicleStatus' : True if request.POST.get('vehicleStatus') == 'Yes' else False,
                'vehiclePaper' : True if request.POST.get('papersReady') == 'Yes' else False,
                'comment' : request.POST.get('comment').strip(),
                'curDate' : datetime.now(),
                'driver' : driver
            }  
        
            insert = insertIntoTable(tableName='PreStart',dataSet=dataSet)
            if insert == True:
                messages.success(request, "Pre-start filled up.")
                return redirect('Account:assignedJobShow')
            else:
                messages.error(request, "something went wrong, please try again")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "You already filled Pre-start.")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You have no access for fill up Pre-start.")
        return redirect(request.META.get('HTTP_REFERER'))

    
def mapFormView(request):
    driverObj = Driver.objects.filter(name=request.user.username).first()
    shiftObj = DriverShift.objects.filter(endDateTime=None, driverId=driverObj.driverId).first()
    
    if shiftObj:
        existingTrip = DriverShiftTrip.objects.filter(shiftId=shiftObj.id, endDateTime=None).first()
        if existingTrip:
            preStart = DriverPreStart.objects.filter(tripId=existingTrip.id)
            if len(preStart) > 0:
                return redirect('Account:driverShiftView', shiftObj.id)
            else:
                return redirect('Account:showPreStartForm', shiftId=shiftObj.id, tripId=existingTrip.id)
        else:
            return redirect('Account:showClientAndTruckNumGet', shiftObj.id)
    else:
        currentDate = getCurrentDateTimeObj()
        params = {
            'date':dateConverterFromTableToPageFormate(currentDate),
            'time':str(currentDate.time()).split('.')[0],
        }
        return render(request, 'Trip_details/DriverShift/mapForm.html', params)

@csrf_protect
def mapDataSave(request, recurring=None):
    driverObj = Driver.objects.filter(name=request.user.username).first()
    shiftObj = DriverShift.objects.filter(endDateTime=None, driverId=driverObj.driverId).first()
    
    if not recurring:
        currentDateTime = getCurrentDateTimeObj()
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        shiftObj = DriverShift()
        shiftObj.latitude = lat
        shiftObj.longitude = lng
        shiftObj.shiftDate = date
        shiftObj.startDateTime = currentDateTime
        shiftObj.driverId = driverObj.driverId
        shiftObj.save()
        
    return redirect('Account:showClientAndTruckNumGet', shiftObj.id)


def showClientAndTruckNumGet(request, shiftId):
    client_ids = Client.objects.all()
    params = {
        'client_ids' : client_ids
    }
    
    shiftObj = DriverShift.objects.filter(pk=shiftId).first()
    if shiftObj:
        params['shiftObj'] = shiftObj
        existingTrip = DriverShiftTrip.objects.filter(shiftId=shiftObj.id, endDateTime=None).first()
        if existingTrip:
            return redirect('Account:showPreStartForm',shiftId=shiftObj.id, tripId=existingTrip.id)

        
    return render(request, 'Trip_details/DriverShift/clientForm.html', params)

def showPreStartForm(request, shiftId, tripId):
    tripObj = DriverShiftTrip.objects.filter(pk=tripId).first()
    truckConnectionObj = ClientTruckConnection.objects.filter(pk=tripObj.truckConnectionId).first()
    preStart = PreStart.objects.filter(pk=truckConnectionObj.pre_start_name).first()
    preStartQuestions = PreStartQuestion.objects.filter(preStartId=preStart.id)
    
    params = {
        'preStartQuestions':preStartQuestions,
        'shiftId' : shiftId,
        'tripObj' : tripObj
    }
     
    return render(request, 'Trip_details/pre-startForm.html',params)
    
@csrf_protect
def clientAndTruckDataSave(request, id):
    tripObj = DriverShiftTrip.objects.filter(shiftId=id, endDateTime=None).first()
    if tripObj:
        messages.error(request, "Please complete your current trip first.")
        return redirect('Account:mapFormView')
        
    clientName = request.POST.get('clientId')
    truckNum = request.POST.get('truckNum').split('-')
    
    adminTruckNum = AdminTruck.objects.filter(adminTruckNumber=truckNum[0]).first()
    clientTruckNum = truckNum[1]
    clientObj = Client.objects.filter(name=clientName).first()
    truckConnectionObj = ClientTruckConnection.objects.filter(truckNumber=adminTruckNum,clientTruckId=clientTruckNum).first()
    currentDateTime = getCurrentDateTimeObj()
    
    tripObj = DriverShiftTrip()
    tripObj.shiftId = id
    tripObj.startDateTime = currentDateTime
    tripObj.clientId = clientObj.clientId
    tripObj.truckConnectionId = truckConnectionObj.id
    tripObj.save()
    
    return redirect('Account:showPreStartForm', shiftId=tripObj.shiftId, tripId=tripObj.id)

def checkQuestionRequired(request):
    status = False
    questionId = request.GET.get('questionId')
    optionNumber = request.GET.get('optionNumber')
    questionObj = PreStartQuestion.objects.filter(pk=questionId).first()
    
    if int(optionNumber) == 1 and questionObj.wantFile1 == True:
        status = True
    elif int(optionNumber) == 2 and questionObj.wantFile2 == True:
        status = True
    elif int(optionNumber) == 3 and questionObj.wantFile3 == True:
        status = True
    elif int(optionNumber) == 4 and questionObj.wantFile4 == True:
        status = True
        
    return JsonResponse({'status': status})
    
@csrf_protect
def DriverPreStartSave(request, tripId):
    
    tripObj = DriverShiftTrip.objects.filter(pk=tripId).first()
    shiftObj = DriverShift.objects.filter(pk=tripObj.shiftId).first()
    truckConnectionObj = ClientTruckConnection.objects.filter(id=tripObj.truckConnectionId).first()
    preStartObj = PreStart.objects.filter(pk=truckConnectionObj.pre_start_name).first()
    preStartQuestions = PreStartQuestion.objects.filter(preStartId=preStartObj.id)
    driverObj = Driver.objects.filter(name=request.user.username).first()
    currentDateTime = getCurrentDateTimeObj()
    currentTrips = DriverShiftTrip.objects.filter(shiftId=shiftObj.id).order_by('-startDateTime')
    
    for trip in currentTrips:
        trip.clientName = Client.objects.filter(pk=trip.clientId).first().name
        trip.truckNum = ClientTruckConnection.objects.filter(pk=trip.truckConnectionId).first().clientTruckId

    driverPreStartObj = DriverPreStart.objects.filter(shiftId=shiftObj, tripId=tripObj, truckConnectionId=truckConnectionObj).first()
   
    msg = None
    if not driverPreStartObj:
        driverPreStartObj = DriverPreStart()
        driverPreStartObj.shiftId = shiftObj
        driverPreStartObj.tripId = tripObj
        driverPreStartObj.truckConnectionId = truckConnectionObj
        driverPreStartObj.clientId = truckConnectionObj.clientId
        driverPreStartObj.preStartId = preStartObj
        driverPreStartObj.driverId = driverObj
        driverPreStartObj.curDateTime = currentDateTime
        driverPreStartObj.comment = request.POST.get('comment')
        driverPreStartObj.save()

        for question in preStartQuestions:
            queFile, queComment = None, None
            answerObj = DriverPreStartQuestion()
            ansText = request.POST.get(f'selector{question.id}')
            answerObj.preStartId = driverPreStartObj
            answerObj.questionId = question
            answerObj.answer = ansText

            if ansText == question.optionTxt1 and question.wantFile1:
                queFile =  request.FILES.get(f'f{question.id}o1')
                queComment = request.POST.get(f'c{question.id}o1')
            elif ansText == question.optionTxt2 and question.wantFile2:
                queFile =  request.FILES.get(f'f{question.id}o2')
                queComment = request.POST.get(f'c{question.id}o2')
            elif ansText == question.optionTxt3 and question.wantFile3:
                queFile =  request.FILES.get(f'f{question.id}o3')
                queComment = request.POST.get(f'c{question.id}o3')
            elif ansText == question.optionTxt4 and question.wantFile4:
                queFile =  request.FILES.get(f'f{question.id}o4')
                queComment = request.POST.get(f'c{question.id}o4')

            if queFile:  
                curTimeStr = getCurrentTimeInString()
                path = 'static/img/preStartImages'
                fileName = queFile.name
                newFileName = 'Pre-start' + curTimeStr + '!_@' + fileName
                pfs = FileSystemStorage(location=path)
                pfs.save(newFileName, queFile)
                answerObj.answerFile = f'{path}/{newFileName}'
                answerObj.comment = queComment        
            answerObj.save()
           
    return redirect('Account:driverShiftView', shiftObj.id)
    
    
def driverShiftView(request, shiftId):
    tripObj = None
    shiftObj = DriverShift.objects.filter(pk=shiftId).first()
    currentTrips = DriverShiftTrip.objects.filter(shiftId=shiftObj.id).order_by('-startDateTime')

    for trip in currentTrips:
        trip.clientName = Client.objects.filter(pk=trip.clientId).first().name
        trip.truckNum = ClientTruckConnection.objects.filter(pk=trip.truckConnectionId).first().clientTruckId
        
        if trip.endDateTime == None:
            tripObj = trip
            
    truckConnectionObj = ClientTruckConnection.objects.filter(id=tripObj.truckConnectionId).first()
    breaks = DriverBreak.objects.filter(shiftId=shiftObj)
    
    for breakObj in breaks:
        breakObj.clientName = Client.objects.filter(pk=breakObj.tripId.clientId).first().name
        breakObj.truckNum = ClientTruckConnection.objects.filter(pk=breakObj.tripId.truckConnectionId).first().clientTruckId

         
    params = {
        'tripObj' : tripObj,
        'currentTrips' : currentTrips,
        'shiftObj' : shiftObj,
        'clientObj' : truckConnectionObj.clientId,
        'truckObj' : truckConnectionObj,
        'breaks' : breaks
    }
    return render(request, 'Trip_details/DriverShift/shiftPage.html', params)


def addDriverBreak(request, shiftId, tripId):
    
    shiftObj = DriverShift.objects.filter(pk=shiftId).first()
    tripObj = DriverShiftTrip.objects.filter(pk=tripId).first()
    tripObj.startDateTime = str(tripObj.startDateTime).split('.')[0]
    tripObj.currentTime = str(getCurrentDateTimeObj()).split('.')[0]
    # print(str(tripObj.startDateTime).split('.')[0])
    truckNo = ClientTruckConnection.objects.filter(pk=tripObj.truckConnectionId).first().clientTruckId
    clientName = Client.objects.filter(pk=tripObj.clientId).first().name
    params = {
        'shiftObj' : shiftObj,
        'tripObj' : tripObj,
        'truckNo' : truckNo,
        'clientName' : clientName
    }
    return render(request, 'Trip_details/DriverShift/addBreak.html', params)


@csrf_protect
def saveDriverBreak(request, shiftId, tripId):
    shiftObj = DriverShift.objects.filter(pk=shiftId).first()
    tripObj = DriverShiftTrip.objects.filter(pk=tripId).first()
    driverId = Driver.objects.filter(name=request.user.username).first()
    breakObj = DriverBreak()
    breakObj.shiftId = shiftObj
    breakObj.tripId = tripObj
    breakObj.driverId = driverId
    breakObj.startDateTime = request.POST.get('startDateTime') 
    breakObj.endDateTime = request.POST.get('endDateTime')
    breakObj.location = request.POST.get('curLocation')
    breakObj.description = request.POST.get('description')

    breakFile = request.FILES.get('breakFile')
    if breakFile:
        curTimeStr = getCurrentTimeInString()
        path = 'static/img/breakFiles'
        fileName = breakFile.name
        newFileName = 'break-file' + curTimeStr + '!_@' + fileName
        pfs = FileSystemStorage(location=path)
        pfs.save(newFileName, breakFile)
        breakObj.breakFile = f'{path}/{newFileName}'
    
    breakObj.save()
    return redirect('Account:DriverPreStartSave', tripId)
    
    
def collectDockets(request, shiftId, tripId, endShift=None):
    tripObj = DriverShiftTrip.objects.filter(pk=tripId).first()
    clientObj = Client.objects.filter(pk=tripObj.clientId).first()

    params = {
        'docket' : 1 if clientObj.docketGiven else 0,
        'shiftId' : shiftId,
        'tripId' : tripId,
        'endShift': endShift
    }
    return render(request, 'Trip_details/DriverShift/collectDockets.html', params)

@csrf_protect
def collectedDocketSave(request,  shiftId, tripId, endShift):
    curTimeStr = getCurrentTimeInString()
    currentDateTime = getCurrentDateTimeObj()
    docketPath = 'static/img/docketFiles'
    loadPath = 'static/img/finalloadSheet'
    shiftObj = DriverShift.objects.filter(pk=shiftId).first()
    tripObj = DriverShiftTrip.objects.filter(pk=tripId).first()
    clientObj = Client.objects.filter(pk=tripObj.clientId).first()

    loadSheetFile = request.FILES.get('loadSheet')
    noOfLoads = int(request.POST.get('noOfLoads'))
    tripObj.numberOfLoads = noOfLoads
    tripObj.dispute = True if request.POST.get('dispute') == 'dispute' else False
    tripObj.endDateTime = currentDateTime
    
    if loadSheetFile:
        fileName = loadSheetFile.name
        newFileName = 'load-sheet' + curTimeStr + '!_@' + fileName
        pfs = FileSystemStorage(location=loadPath)
        pfs.save(newFileName, loadSheetFile)
        tripObj.loadSheet = f'{loadPath}/{newFileName}'
    
    if not clientObj.docketGiven:
        for load in range(1,noOfLoads+1):
            docketObj = DriverShiftDocket()
            docketObj.tripId = tripObj.id
            docketObj.shiftId = shiftId
            docketObj.shiftDate = shiftObj.shiftDate
            docketObj.clientId = clientObj.clientId
            docketObj.docketNumber = request.POST.get(f'docketNumber{load}')
            docketObj.comment = request.POST.get(f'comment{load}')
            docketFile = request.FILES.get(f'docketFile{load}')
            
            print(tripObj.id,request.POST.get(f'docketNumber{load}'),request.POST.get(f'comment{load}'))
            if docketFile:
                fileName = loadSheetFile.name
                newFileName = 'load-sheet' + curTimeStr + '!_@' + fileName
                pfs = FileSystemStorage(location=docketPath)
                pfs.save(newFileName, loadSheetFile)
                docketObj.docketFile = f'{docketPath}/{newFileName}'
            docketObj.save()
    else:
        for load in range(1,noOfLoads+1):
            noOfKm = request.POST.get(f'noOfKm{load}')
            transferKm = request.POST.get(f'transferKm{load}')
            standByTimeStart = formatDateTimeForDBSave(request.POST.get(f'standByTimeStart{load}'))
            standByTimeEnd = formatDateTimeForDBSave(request.POST.get(f'standByTimeEnd{load}'))
            
            docketObj = DriverShiftDocket()
            docketObj.tripId = tripObj.id
            docketObj.shiftId = shiftId
            docketObj.shiftDate = shiftObj.shiftDate
            docketObj.clientId = clientObj.clientId
            docketObj.docketNumber = request.POST.get(f'docketNumber{load}')

            docketObj.noOfKm = noOfKm if noOfKm else 0
            docketObj.transferKM = transferKm if transferKm else 0
            docketObj.standByStartTime = standByTimeStart if standByTimeStart else None
            docketObj.standByEndTime = standByTimeEnd if standByTimeEnd else None
            docketObj.save()
    
    tripObj.save()  
    if endShift == 1:
        shiftObj.endDateTime = currentDateTime
        shiftObj.save()  
        messages.success(request, "Shift completed successfully.")
        return redirect('index')
    else:
        
        return redirect('Account:recurringTrip', 1)
    
    
@csrf_protect
@api_view(['POST'])
def getTrucks(request):
    connections = []
    clientName = request.POST.get('clientName')
    client = Client.objects.get(name=clientName)
    shiftObj = DriverShift.objects.filter(pk=request.POST.get('shiftId')).first()
    
    currentTripObjs = DriverShiftTrip.objects.filter(shiftId=shiftObj.id)
    for trip in currentTripObjs:
        connections.append(trip.truckConnectionId)
    
    allCurrentTrips = DriverShiftTrip.objects.filter(endDateTime=None)
    for trip in allCurrentTrips:
        connections.append(trip.truckConnectionId)
    
    truckList = []
    truck_connections = ClientTruckConnection.objects.filter(clientId=client.clientId)
    docket = client.docketGiven

    for truck_connection in truck_connections:
        if truck_connection.id in connections:
            truckList.append(str(truck_connection.truckNumber) + '-' + str(truck_connection.clientTruckId) + ' Occupied')
        else:
            truckList.append(str(truck_connection.truckNumber) + '-' + str(truck_connection.clientTruckId))
            
    return JsonResponse({'status': True, 'trucks': truckList, 'docket': docket})


def rcti(request):

    rctiErrors = RctiErrors.objects.filter(status = False).values()
    rctiSolve = RctiErrors.objects.filter(status = True).values()
    client = Client.objects.all()
    BasePlant_ = BasePlant.objects.all()
    params = {
        'rctiErrors' : rctiErrors,
        'rctiSolve' :rctiSolve,
        # 'archiveError':archiveError,
        'client':client,
        'basePlants': BasePlant_
    }
    
    return render(request, 'Account/rctiForm.html',params)

# def rctiErrorSolve(request ,id): 
           
#     rctiErrorsObj = RctiErrors.objects.get(id = id)
#     rctiErrorsObj.status = True
#     rctiErrorsObj.save()
#     messages.success(request, "Docket status change ")
#     return redirect(request.META.get('HTTP_REFERER'))
    

def rctiForm(request, id= None):
    rcti = None

    clientName = Client.objects.all()
    rctiReport = RctiReport.objects.all()
    basePlant = BasePlant.objects.all()
    if id:
        rcti = RCTI.objects.filter(pk=id).first()
        rcti.docketDate = rcti.docketDate.strftime("%d-%m-%Y")
        
    params = {
        'rcti': rcti,
        'clientNames':clientName,
        'rctiReports':rctiReport,
        'basePlants':basePlant
    }
    # return HttpResponse(params['basePlants'])
    return render(request, 'Account/Tables/rctiForm.html', params)
def rctiErrorSolveView(request,solveId):
    rcti = None
    rctiErrorObj = RctiErrors.objects.filter(pk=solveId).first()
    clientName = Client.objects.all()
    rctiReport = RctiReport.objects.all()
    rcti = RCTI.objects.filter(docketNumber=rctiErrorObj.docketNumber , docketDate = rctiErrorObj.docketDate).first()
    rcti.docketDate = rcti.docketDate.strftime("%d-%m-%Y")
        
    params = {
        'rcti': rcti,
        'clientNames':clientName,
        'rctiReports':rctiReport,
    }
    return render(request, 'Account/Tables/rctiForm.html', params)

def rctiErrorForm(request ,errorId ):
    errorObj = RctiErrors.objects.filter(pk=errorId).first()
    clientName = Client.objects.all()
    basePlant = BasePlant.objects.all()
    rctiReport = RctiReport.objects.all()

    reportId = int(errorObj.data.split('@_!')[1])

    params = {
        'errorObj': errorObj,
        'clientNames':clientName,
        'rctiReports':rctiReport,
        'reportId':reportId,
        'basePlants':basePlant,
        
    }
    return render(request, 'Account/Tables/rctiForm.html', params)

def convertIntoFloat(str):
    cleaned_string = str.strip('()')
    return float(cleaned_string)

@csrf_protect
def rctiFormSave(request , errorId = None):
    # return HttpResponse(request.POST.get('clientName'))
    RCTIobj = None
    RCTIobj = RCTI.objects.filter(docketNumber = request.POST.get('docketNumber'), docketDate = request.POST.get('docketDate')).first()
    if RCTIobj is None:
        RCTIobj = RCTI()
    rctiErrorObj = RctiErrors.objects.filter(pk=errorId).first()
    
    if rctiErrorObj:
        reportId = int(rctiErrorObj.data.split('@_!')[1])
        clientObj= Client.objects.filter(name = rctiErrorObj.clientName).first()
        RCTIobj.clientName =clientObj
        RCTIobj.rctiReport = RctiReport.objects.filter(pk=reportId).first()
        
    else:
        clientObj = Client.objects.filter(pk = request.POST.get('clientName')).first()
        RCTIobj.clientName =clientObj
        RCTIobj.rctiReport = RctiReport.objects.filter(pk=request.POST.get('rctiReport')).first()
        
    
    RCTIobj.truckNo = request.POST.get('truckNo')
    RCTIobj.docketNumber = request.POST.get('docketNumber')
    RCTIobj.docketDate = request.POST.get('docketDate')
    RCTIobj.docketYard = request.POST.get('docketYard')
    RCTIobj.noOfKm = request.POST.get('noOfKm')
    RCTIobj.unit = request.POST.get('unit')
    RCTIobj.paidQty = request.POST.get('paidQty')
    # return HttpResponse(request.POST.get('docketYard'))
    RCTIobj.cubicMl = request.POST.get('cubicMl')
    RCTIobj.cubicMiAndKmsCost = request.POST.get('cubicMiAndKmsCost')
    RCTIobj.destination = request.POST.get('destination')
    RCTIobj.cartageGSTPayable = request.POST.get('cartageGSTPayable')
    RCTIobj.cartageTotalExGST = request.POST.get('cartageTotalExGST')
    RCTIobj.cartageTotal = request.POST.get('cartageTotal')
    
    RCTIobj.transferKM = request.POST.get('transferKM')
    RCTIobj.transferKMCost = request.POST.get('transferKMCost')
    RCTIobj.transferKMGSTPayable = request.POST.get('transferKMGSTPayable')
    RCTIobj.transferKMTotalExGST = request.POST.get('transferKMTotalExGST')
    RCTIobj.transferKMTotal = request.POST.get('transferKMTotal')
    
    RCTIobj.returnKm = request.POST.get('returnKm')
    RCTIobj.returnPerKmPerCubicMeterCost = request.POST.get('returnPerKmPerCubicMeterCost')
    RCTIobj.returnKmGSTPayable = request.POST.get('returnKmGSTPayable')
    RCTIobj.returnKmTotalExGST = request.POST.get('returnKmTotalExGST')
    RCTIobj.returnKmTotal = request.POST.get('returnKmTotal')
    
    RCTIobj.waitingTimeSCHED = request.POST.get('waitingTimeSCHED')
    RCTIobj.waitingTimeSCHEDCost = request.POST.get('waitingTimeSCHEDCost')
    RCTIobj.waitingTimeSCHEDGSTPayable = request.POST.get('waitingTimeSCHEDGSTPayable')
    RCTIobj.waitingTimeSCHEDTotalExGST = request.POST.get('waitingTimeSCHEDTotalExGST')
    RCTIobj.waitingTimeSCHEDTotal = request.POST.get('waitingTimeSCHEDTotal')
    
    RCTIobj.waitingTimeInMinutes = request.POST.get('waitingTimeInMinutes')
    RCTIobj.waitingTimeCost = request.POST.get('waitingTimeCost')
    RCTIobj.waitingTimeGSTPayable = request.POST.get('waitingTimeGSTPayable')
    RCTIobj.waitingTimeTotalExGST = request.POST.get('waitingTimeTotalExGST')
    RCTIobj.waitingTimeTotal = request.POST.get('waitingTimeTotal')
    
    RCTIobj.standByNoSlot = request.POST.get('standByNoSlot')
    RCTIobj.standByPerHalfHourDuration = request.POST.get('standByPerHalfHourDuration')
    RCTIobj.standByUnit = request.POST.get('standByUnit')
    RCTIobj.standByGSTPayable = request.POST.get('standByGSTPayable')
    RCTIobj.standByTotalExGST = request.POST.get('standByTotalExGST')
    RCTIobj.standByTotal = request.POST.get('standByTotal')
    
    RCTIobj.minimumLoad = request.POST.get('minimumLoad')
    RCTIobj.loadCost = request.POST.get('loadCost')
    RCTIobj.minimumLoadGSTPayable = request.POST.get('minimumLoadGSTPayable')
    RCTIobj.minimumLoadTotalExGST = request.POST.get('minimumLoadTotalExGST')
    RCTIobj.minimumLoadTotal = request.POST.get('minimumLoadTotal')
    
    RCTIobj.blowBack = request.POST.get('blowBack')
    RCTIobj.blowBackCost = request.POST.get('blowBackCost')
    RCTIobj.blowBackGSTPayable = request.POST.get('blowBackGSTPayable')
    RCTIobj.blowBackTotalExGST = request.POST.get('blowBackTotalExGST')
    RCTIobj.blowBackTotal = request.POST.get('blowBackTotal')
    
    RCTIobj.callOut = request.POST.get('callOut')
    RCTIobj.callOutCost = request.POST.get('callOutCost')
    RCTIobj.callOutGSTPayable = request.POST.get('callOutGSTPayable')
    RCTIobj.callOutTotalExGST = request.POST.get('callOutTotalExGST')
    RCTIobj.callOutTotal = request.POST.get('callOutTotal')
    
    RCTIobj.surcharge = request.POST.get('surcharge')
    RCTIobj.surchargeCost = request.POST.get('surchargeCost')
    RCTIobj.surchargeGSTPayable = request.POST.get('surchargeGSTPayable')
    RCTIobj.surchargeTotalExGST = request.POST.get('surchargeTotalExGST')
    RCTIobj.surchargeTotal = request.POST.get('surchargeTotal')
    
    RCTIobj.otherDescription = request.POST.get('otherDescription')
    RCTIobj.others = request.POST.get('others')
    RCTIobj.othersCost = request.POST.get('othersCost')
    RCTIobj.othersGSTPayable = request.POST.get('othersGSTPayable')
    RCTIobj.othersTotalExGST = request.POST.get('othersTotalExGST')
    RCTIobj.othersTotal = request.POST.get('othersTotal')
    
    RCTIobj.save()
    
    reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = RCTIobj.docketNumber , docketDate = RCTIobj.docketDate ).first()

    rctiTotalCost =   convertIntoFloat(RCTIobj.cartageTotal) + convertIntoFloat(RCTIobj.waitingTimeTotal) + convertIntoFloat(RCTIobj.transferKMTotal)  +  convertIntoFloat(RCTIobj.returnKmTotal) + convertIntoFloat(RCTIobj.standByTotal) + convertIntoFloat(RCTIobj.minimumLoadTotal) + convertIntoFloat(RCTIobj.surchargeTotalExGST)+convertIntoFloat(RCTIobj.othersTotalExGST) + convertIntoFloat(RCTIobj.blowBackTotal) +convertIntoFloat(RCTIobj.callOutTotal) 
    
    if not reconciliationDocketObj :
        reconciliationDocketObj = ReconciliationReport()
    
    reconciliationDocketObj.docketNumber =  RCTIobj.docketNumber
    reconciliationDocketObj.docketDate =  RCTIobj.docketDate
    reconciliationDocketObj.rctiLoadAndKmCost =  RCTIobj.cartageTotalExGST
    reconciliationDocketObj.rctiSurchargeCost =   RCTIobj.surchargeTotalExGST
    reconciliationDocketObj.rctiWaitingTimeCost = RCTIobj.waitingTimeTotal  
    reconciliationDocketObj.rctiTransferKmCost = RCTIobj.transferKMTotal 
    reconciliationDocketObj.rctiReturnKmCost =  RCTIobj.returnKmTotal
    reconciliationDocketObj.rctiOtherCost =  RCTIobj.othersTotalExGST 
    reconciliationDocketObj.rctiStandByCost =  RCTIobj.standByTotal
    reconciliationDocketObj.rctiLoadDeficit =  RCTIobj.minimumLoadTotal
    reconciliationDocketObj.rctiBlowBack =  RCTIobj.blowBackTotal
    reconciliationDocketObj.rctiCallOut =  RCTIobj.callOutTotal
    reconciliationDocketObj.rctiTotalCost =  round(rctiTotalCost,2)
    reconciliationDocketObj.fromRcti = True 
    
    reconciliationDocketObj.save()
    checkMissingComponents(reconciliationDocketObj)
    if errorId:
        rctiErrorObj.docketNumber = request.POST.get('docketNumber')
        rctiErrorObj.docketDate = request.POST.get('docketDate')
        rctiErrorObj.status = True
        rctiErrorObj.save()
        
    messages.success( request, "RCTI entry successfully done.")
    return redirect('Account:rcti')

@csrf_protect
def rctiHolcimFormSave(request):
    driverObj = Driver.objects.filter(pk = request.POST.get('driverId')).first()
    holcimTripObj = HolcimTrip()
    existingDocket = HolcimDocket.objects.filter(ticketedDate = request.POST.get('ticketedDate'),jobNo = request.POST.get('jobNo'), truckNo = request.POST.get('truckNo')).first()
    if existingDocket:
            messages.error( request, "Job no already exist")
            return redirect(request.META.get('HTTP_REFERER'))
    existingTrip = HolcimTrip.objects.filter(truckNo = request.POST.get('truckNo'),shiftDate = request.POST.get('ticketedDate')).first()
    if existingTrip:
        existingTrip.numberOfLoads = existingTrip.numberOfLoads + 1
        existingTrip.save()
        holcimTripObj = existingTrip
    else:
        holcimTripObj.truckNo = request.POST.get('truckNo')
        holcimTripObj.shiftDate = request.POST.get('ticketedDate')
        holcimTripObj.numberOfLoads = 1
        holcimTripObj.save()
        
        

    holcimDocketObj =HolcimDocket()
    holcimDocketObj.truckNo = request.POST.get('truckNo')
    holcimDocketObj.tripId = holcimTripObj
    holcimDocketObj.orderNo  = request.POST.get('orderNo')
    holcimDocketObj.jobNo = request.POST.get('jobNo')
    holcimDocketObj.status = request.POST.get('status')
    holcimDocketObj.ticketedDate =  request.POST.get('ticketedDate')
    holcimDocketObj.ticketedTime =  request.POST.get('ticketedTime')
    holcimDocketObj.load = holcimDateConvertStr(request.POST.get('load'))
    holcimDocketObj.loadComplete = request.POST.get('loadComplete')
    holcimDocketObj.toJob = holcimDateConvertStr(request.POST.get('toJob'))
    holcimDocketObj.timeToDepart = request.POST.get('timeToDepart')
    holcimDocketObj.onJob = holcimDateConvertStr(request.POST.get('onJob'))
    holcimDocketObj.timeToSite = request.POST.get('timeToSite')
    holcimDocketObj.beginUnload = holcimDateConvertStr(request.POST.get('beginUnload'))
    holcimDocketObj.waitingTime = request.POST.get('waitingTime')
    holcimDocketObj.endPour = holcimDateConvertStr(request.POST.get('endPour'))
    holcimDocketObj.wash = holcimDateConvertStr(request.POST.get('wash'))
    holcimDocketObj.toPlant = holcimDateConvertStr(request.POST.get('toPlant'))
    holcimDocketObj.timeOnSite = request.POST.get('timeOnSite')
    holcimDocketObj.atPlant = holcimDateConvertStr(request.POST.get('atPlant'))
    holcimDocketObj.leadDistance = request.POST.get('leadDistance')
    holcimDocketObj.returnDistance = request.POST.get('returnDistance')
    holcimDocketObj.totalDistance = request.POST.get('totalDistance')
    holcimDocketObj.totalTime = request.POST.get('totalTime')
    holcimDocketObj.waitTimeBetweenJob = request.POST.get('waitTimeBetweenJob')
    holcimDocketObj.driverName = driverObj
    holcimDocketObj.quantity = request.POST.get('quantity')
    holcimDocketObj.slump = request.POST.get('slump')
    holcimDocketObj.waterAdded = request.POST.get('waterAdded')
    holcimDocketObj.save()
    messages.success( request, "RCTI holcim entry successfully done.")
    return redirect('Account:rcti')


@csrf_protect
def rctiSave(request):
    rctiPdf = request.FILES.get('rctiPdf')
    clientName = request.POST.get('clientName')
    time = getCurrentTimeInString()
    location = None
    if rctiPdf:
        rctiPdfName = time + "@_!" + (str(rctiPdf.name)).replace(' ','')
        pdfLocation = 'static/Account/RCTI/uplodedRctiPdf'
        savePdfObj = FileSystemStorage(location=pdfLocation)
        savePdfObj.save(rctiPdfName,rctiPdf)
        
    invoiceFile = request.FILES.get('RctiFile')
    save_data = request.POST.get('save')
    
    if not invoiceFile:
        return HttpResponse("No file uploaded")
    try:
        folderName = None
        newFileName = time + "@_!" + (str(invoiceFile.name)).replace(' ','')
        if clientName == 'boral':
            folderName = 'tempRCTIInvoice'
        elif clientName == 'holcim':
            folderName = 'RCTIInvoice'
            
        location = f'static/Account/RCTI/{folderName}'

        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, invoiceFile)
        if clientName == 'boral' and save_data == '1':
            cmd = ["python", "Account_app/utils.py", newFileName]
            subprocess.Popen(cmd, stdout=subprocess.PIPE)
        fileDetails = [] 
        date_ = 0
        total = 0
        clientNameID  = Client.objects.filter(name = clientName).first()
        if save_data == '1':
            if clientName == 'boral':
                with open( f'static/Account/RCTI/tempRCTIInvoice/{newFileName}' , 'r') as f:
                    fileData = csv.reader(f)
                    for data in fileData:
                        data = data[0]
                        dataList = data.split()
                        if 'documentnumber' in data.lower().strip().replace(" ",""):
                            date_ += 1
                        elif 'date' in data.lower().strip().replace(" ","") and date_ == 1 :
                            fileDetails.insert(0,str(invoiceFile))
                            fileDetails.insert(1,dataList[-1])
                        elif 'totalexcludinggst' in data.lower().strip().replace(" ","") and date_ == 1:
                            fileDetails.insert(2,float(dataList[-1].replace(",","").replace('$','')))
                        elif 'gstpayable' in data.lower().strip().replace(" ","") and date_ == 1:
                            fileDetails.insert(3,float(dataList[-1].replace(",","").replace('$','')))
                        elif 'total' in data.lower().strip().replace(" ","") and date_ == 1:
                            fileDetails.insert(4,float(dataList[-1].replace(",","").replace('$','')))
                            date_ = 0
                date_object = datetime.strptime(fileDetails[1], '%y/%m/%d').strftime('%Y-%m-%d')
                rctiReport = RctiReport.objects.filter(reportDate= date_object, total= fileDetails[-1] ,  fileName= fileDetails[0]).first()
                if rctiReport:
                    messages.error(request, "This file already exists!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    rctiReport = RctiReport()
                    rctiReport.fileName = fileDetails[0]
                    rctiReport.clientName = clientNameID
                    rctiReport.reportDate = date_object
                    rctiReport.gstPayable = fileDetails[2]
                    rctiReport.totalExGST = fileDetails[3]
                    rctiReport.total = fileDetails[4]
                    rctiReport.save()
                    with open('rctiReportId.txt','w')as f:
                        f.write(str(rctiReport.id))
                    colorama.AnsiToWin32.stream = None
                    os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
                    cmd = ["python", "manage.py", "runscript", 'csvToModel.py']
                    subprocess.Popen(cmd, stdout=subprocess.PIPE)
            elif clientName == 'holcim':
                with open( f'static/Account/RCTI/RCTIInvoice/{newFileName}' , 'r') as f:
                    fileData = csv.reader(f)
                    for row in fileData:
                        row = row[0]
                        splitRow = row.split()
                        if 'grosscartageincomestatement' in row.lower().strip().replace(" ","") and len(fileDetails) == 0:
                            fileDetails.insert(0,str(invoiceFile))
                            fileDetails.insert(1,splitRow[-2])
                        elif 'totalforvendor' in row.lower().strip().replace(" ",""):
                            total = 1
                        elif total == 1:
                            fileDetails.insert(2,float(splitRow[-1].replace(',','')))
                            total = 0
                date_object = datetime.strptime(fileDetails[1], '%d.%m.%Y').date()
                rctiReport = RctiReport.objects.filter(reportDate= date_object, total= fileDetails[-1] ,  fileName= fileDetails[0]).first()
                if rctiReport:
                    messages.error(request, "This file entry already exists!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    rctiReport = RctiReport()
                    rctiReport.reportDate = date_object
                    rctiReport.fileName =  fileDetails[0]
                    rctiReport.clientName = clientNameID
                    rctiReport.total = fileDetails[-1]
                    rctiReport.save()
                    with open('rctiReportId.txt','w')as f:
                        f.write(str(rctiReport.id))
                with open("File_name_file.txt",'w+',encoding='utf-8') as f:
                    file_name = f.write(newFileName)
                colorama.AnsiToWin32.stream = None
                os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
                cmd = ["python", "manage.py", "runscript", 'holcimUtils','--continue-on-error']
                
                subprocess.Popen(cmd, stdout=subprocess.PIPE)
        messages.success( request, "Please wait 5 minutes. The data conversion process continues")
        return redirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        messages.error( request, "Please enter valid file")
        return redirect(request.META.get('HTTP_REFERER'))
        return HttpResponse(f"Error: {str(e)}")

def uplodedRCTI(request):
   
    rctiFile = os.listdir('static/Account/RCTI/uplodedRctiPdf')
    rctiFileNameLists = []
    for file in rctiFile:
        rctiFileNameLists.append([file.split('@_!')[0],file.split('@_!')[1]])
        
    return render(request, 'Account/uplodedRCTI.html', {'rctiFileNameLists' : rctiFileNameLists})

@csrf_protect
def getRctiError(request):
    rctiErrorData = RctiErrors.objects.filter(pk=request.POST.get('id')).values().first()
    return JsonResponse({'status': True,'data': rctiErrorData})


def expanseForm(request, id = None):
    rctiExpense = None
    if id:
        rctiExpense = RctiExpense.objects.filter(id = id).first()
        rctiExpense.docketDate = dateConverterFromTableToPageFormate(rctiExpense.docketDate)
    params = {
        'rcti' : rctiExpense
    }
    
    return render(request, 'Account/expanseForm.html',params)

@csrf_protect
def expanseSave(request):
    clientNameObj = Client.filter(name = 'boral').first()
    RctiExpenseObj = RctiExpense()
    RctiExpenseObj.clientName  = clientNameObj
    RctiExpenseObj.truckNo = request.POST.get('truckNo')
    RctiExpenseObj.docketNumber = request.POST.get('docketNumber')
    RctiExpenseObj.docketDate = request.POST.get('docketDate')
    RctiExpenseObj.docketYard = request.POST.get('docketYard')
    RctiExpenseObj.description = request.POST.get('description')
    RctiExpenseObj.paidKm = request.POST.get('paidKm')
    RctiExpenseObj.invoiceQuantity = request.POST.get('invoiceQuantity')
    RctiExpenseObj.unit = request.POST.get('unit')
    RctiExpenseObj.unitPrice = request.POST.get('unitPrice')
    RctiExpenseObj.gstPayable = request.POST.get('gstPayable')
    RctiExpenseObj.totalExGST = request.POST.get('totalExGST')
    RctiExpenseObj.total = request.POST.get('total')
    RctiExpenseObj.save()
    
    messages.success( request, "RCTI Expense Entry successfully done.")
    return redirect('Account:rcti')

def driverEntry(request):
    return render(request, 'Account/driverEntryForm.html')

@csrf_protect
def driverEntrySave(request):
    Driver_csv_file = request.FILES.get('driverEntryFile')
    if not Driver_csv_file:
        return HttpResponse("No file uploaded")
    try:
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]
        newFileName = time + "@_!" + str(Driver_csv_file.name)

        location = 'static/Account/DriverEntry'
        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, Driver_csv_file)
        with open("Driver_reg_file.txt", 'w') as f:
            f.write(newFileName)
            f.close()
        colorama.AnsiToWin32.stream = None
        os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
        cmd = ["python", "manage.py", "runscript", 'DriverCsvToModel','--continue-on-error']
        subprocess.Popen(cmd, stdout=subprocess.PIPE)
        messages.success(
            request, "Please wait 5 minutes. The data conversion process continues")
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def driverDocketEntry(request, tripId , errorId = None):
    surcharges = Surcharge.objects.all()   
    docketData = None
    if errorId:
        docketData = PastTripError.objects.filter(pk = errorId).first()

    tripObj = DriverShiftTrip.objects.filter(pk=tripId).first()
    shiftObj = DriverShift.objects.filter(pk=tripObj.shiftId).first()
    if tripObj:
        driver = Driver.objects.all()
        clientName = Client.objects.all()
        clientTruck = ClientTruckConnection.objects.all()
        base_plant = BasePlant.objects.all()
        params = {
            'basePlants': base_plant,
            'tripObj': tripObj,
            'surcharges': surcharges,
            'errorId':errorId,
            'clientTruck':clientTruck,
            'Driver': driver,
            'shiftObj':shiftObj
        }
        return render(request, 'Account/driverDocketEntry.html', params)
    else:
        messages.warning(request, "Invalid Request ")
        return redirect('Account:driverTripsTable')
    # shiftObj = DriverShift.objects.filter(pk=shiftId).first()
    # shiftObj.shiftDate = dateConverterFromTableToPageFormate(shiftObj.shiftDate)
    
    # superUser = False
    # driver = Driver.objects.all()
    # clientName = Client.objects.all()
    # clientTruck = ClientTruckConnection.objects.all()
    # base_plant = BasePlant.objects.all()
    # if request.user.is_superuser:
    #     superUser = True
    # else:
    #     messages.warning('Only SuperUser Add Trip.. ')
    #     return redirect(request.META.get('HTTP_REFERER'))
    # params = {

    #     'clientTruck':clientTruck,
    #     'Driver': driver,
    #     'Client': clientName,
    #     'shiftObj':shiftObj,
    #     'superUser':superUser,
    #     'basePlants': base_plant,
    # }

@csrf_protect
def countDocketWaitingTime(request):
    tripId = request.POST.get('tripId')
    print(tripId)
    waitingTimeStart = request.POST.get('waitingTimeStart')
    waitingTimeEnd = request.POST.get('waitingTimeEnd')
    tripObj = DriverShiftTrip.objects.filter(pk=tripId).first()
    totalWaitingTime =0
    if tripObj:
        clientTruckConnectionObj = ClientTruckConnection.objects.filter(pk=tripObj.truckConnectionId).first()
        adminTruckObj = clientTruckConnectionObj.truckNumber
        clientTruckObj = ClientTruckConnection.objects.filter(truckNumber = adminTruckObj).first()
        rateCardObj = RateCard.objects.filter(rate_card_name = clientTruckObj.rate_card_name.rate_card_name).first()
        graceObj = Grace.objects.filter(rate_card_name = rateCardObj).first()

        totalWaitingTime = getTimeDifference(waitingTimeStart,waitingTimeEnd)
        if totalWaitingTime > graceObj.chargeable_waiting_time_starts_after:
            totalWaitingTime = totalWaitingTime - graceObj.waiting_time_grace_in_minutes
            if totalWaitingTime < 0:
                totalWaitingTime = 0
        else:
            totalWaitingTime = 0
                    
    return JsonResponse({'status': True,'totalWaitingTime':totalWaitingTime})


@csrf_protect
def countDocketStandByTime(request):
    standBySlot= 0
    tripId = request.POST.get('tripId')
    standByStartTime = request.POST.get('standByStartTime')
    standByEndTime = request.POST.get('standByEndTime')

    tripObj = DriverShiftTrip.objects.filter(pk=tripId).first()
    
    if tripObj:
        clientTruckConnectionObj = ClientTruckConnection.objects.filter(pk=tripObj.truckConnectionId).first()
        adminTruckObj = clientTruckConnectionObj.truckNumber
        clientTruckObj = ClientTruckConnection.objects.filter(truckNumber = adminTruckObj).first()
        rateCardObj = RateCard.objects.filter(rate_card_name = clientTruckObj.rate_card_name.rate_card_name).first()
        costParameterObj = CostParameters.objects.filter(rate_card_name = rateCardObj).first()
        graceObj = Grace.objects.filter(rate_card_name = rateCardObj).first()

        totalStandByTime = getTimeDifference(standByStartTime,standByEndTime)
        if totalStandByTime > graceObj.chargeable_standby_time_starts_after:
            totalStandByTime = totalStandByTime - graceObj.standby_time_grace_in_minutes
            standBySlot = totalStandByTime//costParameterObj.standby_time_slot_size
        
                    
    return JsonResponse({'status': True,'standBySlot':standBySlot})

    
@csrf_protect
def getSinglePastTripError(request):
    print('here')
    pastTripErrorData = PastTripError.objects.filter(pk=request.POST.get('id')).values().first()
    print(pastTripErrorData)
    return JsonResponse({'status': True,'data':pastTripErrorData})

def driverDocketEntrySave(request, tripId, errorId=None):
    
    # return HttpResponse(errorId)
    tripObj = DriverShiftTrip.objects.filter(pk=tripId).first()
    shiftObj = DriverShift.objects.filter(pk=tripObj.shiftId).first()

    docketNumber_ = int(float(request.POST.get('docketNumber')))
    surchargeId = Surcharge.objects.filter(pk=request.POST.get('surcharge_type')).first().id
    
    docketNumbers = DriverShiftDocket.objects.filter(docketNumber=docketNumber_, shiftDate=shiftObj.shiftDate, tripId = tripId).first()
    if docketNumbers:
        messages.error(request, "This docket number  already exists!")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        docketFile = request.FILES.get('docketFile')
        docketObj = DriverShiftDocket(
            shiftDate=shiftObj.shiftDate,
            tripId=tripId,
            docketNumber=docketNumber_,
            docketFile=docketFileSave(docketFile, docketNumber_),
            basePlant=BasePlant.objects.filter(pk=request.POST.get('basePlant')).first().id,
            noOfKm=request.POST.get('noOfKm'),
            transferKM=request.POST.get('transferKM'),
            surchargeType=surchargeId,
            surcharge_duration=request.POST.get('surcharge_duration'),
            cubicMl=request.POST.get('cubicMl'),
            others=request.POST.get('others')
        )
        # return HttpResponse(DriverDocketObj.shiftDate)
        if request.POST.get('returnToYard') == 'returnToYard':
            docketObj.returnQty = request.POST.get('returnQty')
            docketObj.returnKm = request.POST.get('returnKm')
            docketObj.returnToYard = True
        elif request.POST.get('returnToYard') == 'tippingToYard':
            docketObj.returnQty = request.POST.get('returnQty')
            docketObj.returnKm = request.POST.get('returnKm')
            docketObj.tippingToYard = True

        docketObj.waitingTimeStart = request.POST.get('waitingTimeStart')
        docketObj.waitingTimeEnd = request.POST.get('waitingTimeEnd')
        # docketObj.totalWaitingInMinute = getTimeDifference(docketObj.waitingTimeStart, docketObj.waitingTimeEnd)
        docketObj.totalWaitingInMinute = request.POST.get('totalWaitingInMinute')
        docketObj.standByStartTime = request.POST.get('standByStartTime')
        docketObj.standByEndTime = request.POST.get('standByEndTime')
        docketObj.standBySlot = request.POST.get('standBySlot')
        docketObj.comment = request.POST.get('comment')
        docketObj.save()
        driver_dockets = DriverShiftDocket.objects.filter(tripId=tripId)

        # Count the number of objects in the queryset
        tripObj.numberOfLoads = driver_dockets.count()

        tripObj.save()
        # if errorId:
        #     DriverDocketObj.shiftDate = datetime.strptime(DriverDocketObj.shiftDate, "%Y-%m-%d").date()
        #     driverDocketNumber = DriverDocketObj.docketNumber
        #     reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = driverDocketNumber , docketDate = DriverDocketObj.shiftDate ).first()
                    
        #     if not  reconciliationDocketObj :
        #         reconciliationDocketObj = ReconciliationReport()
        #     reconciliationDocketObj.driverId = driver_trip_id.id  
        #     reconciliationDocketObj.clientId = driver_trip_id.id 
        #     reconciliationDocketObj.truckId = driver_trip_id.truckNo 
                
        #     driverLoadAndKmCost = checkLoadAndKmCost(driverDocketNumber,DriverDocketObj.shiftDate)
        #     driverSurchargeCost = checkSurcharge(driverDocketNumber,DriverDocketObj.shiftDate)
        #     # return HttpResponse(driverSurchargeCost)
        #     driverWaitingTimeCost = checkWaitingTime(driverDocketNumber,DriverDocketObj.shiftDate)
        #     slotSize = DriverTripCheckStandByTotal(driverDocketNumber,DriverDocketObj.shiftDate)
        #     driverStandByCost = checkStandByTotal(driverDocketNumber,DriverDocketObj.shiftDate,slotSize)
        #     driverTransferKmCost = checkTransferCost(driverDocketNumber,DriverDocketObj.shiftDate)
        #     driverReturnKmCost = checkReturnCost(driverDocketNumber,DriverDocketObj.shiftDate)
        #     # minLoad 
        #     driverLoadDeficit = checkMinLoadCost(driverDocketNumber,DriverDocketObj.shiftDate)
        #     # TotalCost 
        #     driverTotalCost = driverLoadAndKmCost +driverSurchargeCost + driverWaitingTimeCost + driverStandByCost + driverTransferKmCost + driverReturnKmCost +driverLoadDeficit
        #     reconciliationDocketObj.docketNumber = driverDocketNumber  
        #     reconciliationDocketObj.docketDate = DriverDocketObj.shiftDate  
        #     reconciliationDocketObj.driverLoadAndKmCost = driverLoadAndKmCost 
        #     reconciliationDocketObj.driverSurchargeCost = driverSurchargeCost 
        #     reconciliationDocketObj.driverWaitingTimeCost = driverWaitingTimeCost 
        #     reconciliationDocketObj.driverStandByCost = driverStandByCost 
        #     reconciliationDocketObj.driverLoadDeficit = driverLoadDeficit 
        #     reconciliationDocketObj.driverTransferKmCost = driverTransferKmCost 
        #     reconciliationDocketObj.driverReturnKmCost = driverReturnKmCost  
        #     reconciliationDocketObj.driverTotalCost = round(driverTotalCost,2)
        #     reconciliationDocketObj.fromDriver = True 
        #     reconciliationDocketObj.save()
        #     # missingComponents 
        #     checkMissingComponents(reconciliationDocketObj)

        #     errorObj = PastTripError.objects.filter(pk =errorId).first()
        #     errorObj.status = True
        #     errorObj.save()

        url = reverse('Account:DriverTripEdit', kwargs={'id': shiftObj.id})
        messages.success(request, "Docket Added successfully")
        return redirect(url)


def rctiCsvForm(request):
    BasePlant_ = BasePlant.objects.all()
    return render(request, 'Account/rctiCsvForm.html', {'basePlants': BasePlant_})


def driverSampleCsv(request):
    return FileResponse(open(f'static/Account/sampleDriverEntry.xlsx', 'rb'), as_attachment=True)


@csrf_protect
# @api_view(['POST'])
def rctiTable(request):
    # return HttpResponse(id)
    
    startDate_ = request.POST.get('startDate')
    endDate_ = request.POST.get('endDate')
    clientName = request.POST.get('clientName')
    clientNameObj = Client.objects.filter(name=clientName).first()
    dataType = request.POST.get('RCTI')
    holcimData =None
    rctiData = None
    # return HttpResponse(clientNameObj)
    # print(clientNameObj)
    if clientNameObj:
        if dataType== 'rctiDocket':
            # return HttpResponse('here')
            rctiData = RCTI.objects.filter(docketDate__range=(startDate_, endDate_), clientName = clientNameObj)
        else:
            rctiData = RctiExpense.objects.filter(docketDate__range=(startDate_, endDate_), clientName = clientNameObj)
    else:
            rctiData = RCTI.objects.filter(docketDate__range=(startDate_, endDate_))
    
    params = {
        'RCTIs': rctiData,
        'dataType':dataType,
        'holcimData':holcimData,
    }
    # return HttpResponse(params['holcimData'])
    return render(request, 'Account/Tables/rctiTable.html', params)



def HolcimDocketView(request,id):
    holcimTripObj = HolcimTrip.objects.filter(pk = id).first()
    holcimDocketObj = HolcimDocket.objects.filter(tripId = holcimTripObj.id)
    params = {
        'docketData':holcimDocketObj,
        'holcimTripObj':holcimTripObj,
    }
    return render(request, 'Account/Holcim/docketView.html',params)
def basePlantTable(request):
    basePlants = BasePlant.objects.all()
    # locations = Location.objects.all()
    return render(request, 'Account/Tables/basePlantTable.html', {'basePlants': basePlants})

def basePlantForm(request, id=None):
    
    basePlant = None
    if id:
        basePlant = BasePlant.objects.get(pk=id)
        
    params = {
        'basePlant': basePlant,
    }
    return render(request, "Account/basePlantForm.html", params)

# def locationEditForm(request, id=None):
#     basePlant = location = None
#     if id:
#         location = Location.objects.get(pk=id)
#     params = {
#         'basePlant': basePlant,
#         'location': location,
#     }
#     return render(request, "Account/basePlantForm.html", params)

# def locationTable(request):
#     locations = Location.objects.all()
#     return render(request, 'GearBox/truckForm.html', {'locations': locations})

@csrf_protect
@api_view(['POST'])
def basePlantSave(request, id=None):
    dataList = {
        'basePlant': request.POST.get('basePlant').upper(),
        'address': request.POST.get('address'),
        'phone': request.POST.get('phone'),
        'personOnName': request.POST.get('personOnName'),
        'managerName': request.POST.get('managerName'),
        'lat': request.POST.get('lat'),
        'long': request.POST.get('long'),
        'basePlantType' : False if  request.POST.get('basePlantType') == "typeLocation" else True
    }

    
    result = None
    if id:
        result = updateIntoTable(record_id=id, tableName='BasePlant', dataSet=dataList)
    else:
        result = insertIntoTable(tableName='BasePlant', dataSet=dataList)
        with open("scripts/addPastTripForMissingBasePlant.txt", 'w') as f:
                f.write(dataList['basePlant'])
                
        # colorama.AnsiToWin32.stream = None
        # os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
        # cmd = ["python", "manage.py", "runscript", 'addPastTripForMissingBasePlant','--continue-on-error']
        # subprocess.run(cmd)
        colorama.AnsiToWin32.stream = None
        os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
        cmd = ["python", "manage.py", "runscript", 'addPastTripForMissingBasePlant','--continue-on-error']
        subprocess.Popen(cmd, stdout=subprocess.PIPE)

    if result is not True:
        messages.error(request, 'This location already exist.')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'Depot Add successfully')
        return redirect('Account:basePlantTable')


# @csrf_protect
# # @api_view(['POST'])
# def locationSave(request, id=None):
#     locationObj = None
#     if id:
#         locationObj = Location.objects.filter(pk=id).first()
#     else:
#         locationObj = Location()
    
#     locationObj.location = request.POST.get('location').upper()
#     locationObj.address = request.POST.get('locationAddress')
#     locationObj.phone = request.POST.get('locationPhone')
#     locationObj.personOnName = request.POST.get('locationPersonOnName')
#     locationObj.managerName = request.POST.get('locationManagerName')
#     locationObj.lat = request.POST.get('locationLat')
#     locationObj.long = request.POST.get('locationLong')
#     locationObj.save()
    
#     if id:
#         messages.success(request, 'Location updated successfully')
#     else:
#         messages.success(request, 'Location added successfully')

#     return redirect('Account:basePlantTable')

def foreignKeySet(dataset):
    for data in dataset:
        data['clientName_id'] = Client.objects.filter(
            pk=data['clientName_id']).first().name
        data['driverId_id'] = Driver.objects.filter(
            pk=data['driverId_id']).first().name
    return dataset

@csrf_protect
@api_view(['POST'])
def verifiedFilter(request):
    verified = int(request.POST.get('verified'))
    if verified == 1:
        dataList = DriverTrip.objects.filter(verified=True).values()
    else:
        dataList = DriverTrip.objects.filter(verified=False).values()
    foreignKeySet(dataList)
    return JsonResponse({'status': True, 'data': list(dataList)})


@csrf_protect
@api_view(['POST'])
def clientFilter(request):
    dataList = DriverTrip.objects.filter(
        clientName=request.POST.get('id')).values()
    foreignKeySet(dataList)
    return JsonResponse({'status': True, 'data': list(dataList)})


@api_view(['POST'])
def dateRangeFilter(request):
    startDate_values = request.POST.getlist('startDate[]')
    endDate_values = request.POST.getlist('endDate[]')
    startDate = date(int(startDate_values[0]), int(
        startDate_values[1]), int(startDate_values[2]))
    endDate = date(int(endDate_values[0]), int(
        endDate_values[1]), int(endDate_values[2]))
    dataList = DriverTrip.objects.filter(
        shiftDate__range=(startDate, endDate)).values()
    foreignKeySet(dataList)
    return JsonResponse({'status': True, 'data': list(dataList)})


@csrf_protect
def DriverTripEditForm(request, id):
    superUser = False
    if request.user.is_superuser:
        superUser = True
    else:
        superUser = False
    shiftObj = DriverShift.objects.filter(pk=id).first()
    shiftObj.shiftDate = dateConverterFromTableToPageFormate(shiftObj.shiftDate)
    tripObj = DriverShiftTrip.objects.filter(shiftId=id)
    for i in tripObj:
        i.tripDockets = DriverShiftDocket.objects.filter(tripId = i.id)
        for docket in i.tripDockets:
            if docket.waitingTimeStart:
                docket.waitingTimeStart = docket.waitingTimeStart.strftime("%H:%M:%S")
            if docket.waitingTimeEnd:
                docket.waitingTimeEnd = docket.waitingTimeEnd.strftime("%H:%M:%S")
            if docket.standByStartTime:
                docket.standByStartTime = docket.standByStartTime.strftime("%H:%M:%S")
            if docket.standByEndTime:
                docket.standByEndTime = docket.standByEndTime.strftime("%H:%M:%S")
        
    driver = Driver.objects.all()
    clientName = Client.objects.all()
    clientTruck = ClientTruckConnection.objects.all()
    surcharges = Surcharge.objects.all()
        
    base_plant = BasePlant.objects.all()

    params = {
        'driverTrip': tripObj,
        'shiftObj':shiftObj,
        'clientTruck':clientTruck,
        'basePlants': base_plant,
        'Driver': driver,
        'Client': clientName,
        'surcharges' : surcharges,
        'superUser':superUser
    }
    # return HttpResponse(params['driverTrip'])
    return render(request, 'Account/Tables/DriverTrip&Docket/tripEditForm.html', params)


@csrf_protect
def driverDocketUpdate(request):
    docketId = request.POST.get('docketId')
    docketObj = DriverShiftDocket.objects.filter(pk=docketId).first()
    docketNumber = request.POST.get('docketNumber')

    tempDocketObj = DriverShiftDocket.objects.filter(docketNumber = docketNumber, shiftDate = docketObj.shiftDate , clientId = docketObj.clientId).first()
    print(tempDocketObj)
    if tempDocketObj:
        print(docketId,docketNumber)
        return JsonResponse({'status': False})
        
    docketObj.docketNumber = docketNumber
    docketObj.save()
    return JsonResponse({'status': True})
@csrf_protect
def driverEntryUpdate(request, shiftId):
    # Update Trip Save
    shiftObj = DriverShift.objects.filter(pk=shiftId).first()
    tripObj = DriverShiftTrip.objects.filter(shiftId=shiftObj.id)
    
    for trip in tripObj:
        trip.truckConnectionId = request.POST.get(f'truckNo{trip.id}')
        if request.FILES.get(f'loadSheet{trip.id}'):
            loadSheet = request.FILES.get(f'loadSheet{trip.id}')
            trip.loadSheet = loadFileSave(loadSheet)

        trip.comment = request.POST.get(f'comment{trip.id}')
        trip.save()
        # print(trip.id,trip.truckConnectionId)
        # return HttpResponse(trip)
        docketObj = DriverShiftDocket.objects.filter(shiftId=shiftId,tripId = trip.id)
        for docket in docketObj:
            if request.FILES.get(f'docketFile{docket.id}'):
                docketFiles = request.FILES.get(f'docketFile{docket.id}')
                docket.docketFile = docketFileSave(docketFiles, docket.driverDocketNumber)
            docket.basePlant = request.POST.get(f'basePlant{docket.id}')
            docket.noOfKm = request.POST.get(f'noOfKm{docket.id}')
            docket.transferKM = request.POST.get(f'transferKM{docket.id}')
            docket.surcharge_type = request.POST.get(f'surcharge_type{docket.id}')
            if request.POST.get(f'returnToYard{docket.id}') == f'returnToYard{docket.id}':
                docket.returnQty = request.POST.get(f'returnQty{docket.id}')
                docket.returnKm = request.POST.get(f'returnKm{docket.id}')
                docket.returnToYard = True
            elif request.POST.get(f'returnToYard{docket.id}') == f'tippingToYard{docket.id}':
                docket.returnQty = request.POST.get(f'returnQty{docket.id}')
                docket.returnKm = request.POST.get(f'returnKm{docket.id}')
                docket.tippingToYard = True
            
            docket.waitingTimeStart = request.POST.get(f'waitingTimeStart{docket.id}')
            docket.waitingTimeEnd = request.POST.get(f'waitingTimeEnd{docket.id}')
            docket.totalWaitingInMinute = request.POST.get(f'totalWaitingInMinute{docket.id}')
            docket.surchargeType = Surcharge.objects.filter(pk = request.POST.get(f'surcharge_type{docket.id}')).first().id
            docket.surcharge_duration = request.POST.get(f'surcharge_duration{docket.id}')
            docket.cubicMl = request.POST.get(f'cubicMl{docket.id}')
            docket.standByStartTime = request.POST.get(f'standByStartTime{docket.id}')
            docket.standByEndTime = request.POST.get(f'standByEndTime{docket.id}')
            docket.standBySlot = request.POST.get(f'standBySlot{docket.id}')
            docket.others = request.POST.get(f'others{docket.id}')
            docket.comment = request.POST.get(f'comment{docket.id}')
            
            docket.save()

            verified = request.POST.get('verified')
            
            if verified == 'True' :
                trip.verified = True
                trip.save()

                # tripObj = DriverShiftTrip.objects.filter(shiftId=shiftObj)
                reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = docket.docketNumber, docketDate=docket.shiftDate , clientId = docket.clientId).first()
                        
                if not  reconciliationDocketObj :
                    reconciliationDocketObj = ReconciliationReport()
                    
                    
                reconciliationDocketObj.driverId = shiftObj.driverId  
                reconciliationDocketObj.clientId = docket.clientId
                reconciliationDocketObj.truckId = trip.truckConnectionId
                
                # for ReconciliationReport 
                clientTruckConnectionObj = ClientTruckConnection.objects.filter(pk=trip.truckConnectionId,startDate__lte = docket.shiftDate,endDate__gte = docket.shiftDate, clientId = trip.clientId).first()
                rateCard = clientTruckConnectionObj.rate_card_name
                costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lte = docket.shiftDate,end_date__gte = docket.shiftDate).first()
                graceObj = Grace.objects.filter(rate_card_name = rateCard.id,start_date__lte = docket.shiftDate,end_date__gte = docket.shiftDate).first()
                
                driverLoadAndKmCost = checkLoadAndKmCost(docketObj=docket, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                
                driverSurchargeCost = checkSurcharge(docketObj=docket, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)

                driverWaitingTimeCost = checkWaitingTime(docketObj=docket, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                slotSize = DriverTripCheckStandByTotal(docketObj=docket, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                driverStandByCost = checkStandByTotal(docketObj=docket, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj,slotSize =slotSize)
                driverTransferKmCost = checkTransferCost(docketObj=docket, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                driverReturnKmCost = checkReturnCost(docketObj=docket, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                # minLoad 
                driverLoadDeficit = checkMinLoadCost(docketObj=docket, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                # TotalCost 
                driverTotalCost = driverLoadAndKmCost +driverSurchargeCost + driverWaitingTimeCost + driverStandByCost + driverTransferKmCost + driverReturnKmCost +driverLoadDeficit
                reconciliationDocketObj.docketNumber = docket.docketNumber  
                reconciliationDocketObj.docketDate = shiftObj.shiftDate 
                reconciliationDocketObj.driverLoadAndKmCost = driverLoadAndKmCost 
                reconciliationDocketObj.driverSurchargeCost = driverSurchargeCost 
                reconciliationDocketObj.driverWaitingTimeCost = driverWaitingTimeCost 
                reconciliationDocketObj.driverStandByCost = driverStandByCost 
                reconciliationDocketObj.driverLoadDeficit = driverLoadDeficit 
                reconciliationDocketObj.driverTransferKmCost = driverTransferKmCost 
                reconciliationDocketObj.driverReturnKmCost = driverReturnKmCost  
                reconciliationDocketObj.driverTotalCost = round(driverTotalCost,2)
                reconciliationDocketObj.fromDriver = True 
                reconciliationDocketObj.save()
                # missingComponents 
                checkMissingComponents(reconciliationDocketObj)
                shiftObj.verified = True
                shiftObj.save()
    
    messages.success(request, "Docket Updated successfully")
    return redirect('Account:DriverTripEdit',shiftId)
    return redirect(request.META.get('HTTP_REFERER'))
@csrf_protect
def tripEntry(request,shiftId):
    shiftObj = DriverShift.objects.filter(pk=shiftId).first()
    shiftObj.shiftDate = dateConverterFromTableToPageFormate(shiftObj.shiftDate)
    
    superUser = False
    driver = Driver.objects.all()
    clientName = Client.objects.all()
    clientTruck = ClientTruckConnection.objects.all()
    base_plant = BasePlant.objects.all()
    if request.user.is_superuser:
        superUser = True
    else:
        messages.warning('Only SuperUser Add Trip.. ')
        return redirect(request.META.get('HTTP_REFERER'))
    params = {

        'clientTruck':clientTruck,
        'Driver': driver,
        'Client': clientName,
        'shiftObj':shiftObj,
        'superUser':superUser,
        'basePlants': base_plant,
    }
    return render(request,'Account/shiftTripEntry.html',params)
# ````````````````````````````````````
# Reconciliation

# ```````````````````````````````````

def reconciliationForm(request, dataType):
    
    drivers = Driver.objects.all()
    clients = Client.objects.all()
    trucks = AdminTruck.objects.all()
    
    params = {
        'drivers': drivers,
        'clients': clients,
        'trucks': trucks ,
    }

    if dataType == 0:
        params['dataType'] = 'Reconciliation Report'
        params['dataTypeInt'] = 0
    elif dataType ==  1:
        params['dataType'] = 'Short paid Report'
        params['dataTypeInt'] = 1
        
        
    return render(request, 'Reconciliation/reconciliation.html', params)

@csrf_protect
def reconciliationAnalysis(request,dataType):
    startDate = dateConvert(request.POST.get('startDate'))
    endDate = dateConvert(request.POST.get('endDate'))
    
    params = {}
    if dataType == 0:
        dataList = ReconciliationReport.objects.filter(docketDate__range=(startDate, endDate),reconciliationType = 0).values()
        params['dataType'] = 'Reconciliation'
        params['dataTypeInt'] = 0
    elif dataType == 1:
        dataList = ReconciliationReport.objects.filter(docketDate__range=(startDate, endDate),reconciliationType = 1).values()
        params['dataType'] = 'Short paid'
        params['dataTypeInt'] = 1
        
    params['dataList'] = dataList
    
    return render(request, 'Reconciliation/reconciliation-result.html', params)
     


def reconciliationDocketView(request, docketNumber):
    # try:
    rctiDocket = RCTI.objects.filter(docketNumber=docketNumber).first()
    # for driverDocket view 
    driverDocket = DriverDocket.objects.filter(docketNumber=docketNumber).first()
    surcharges = Surcharge.objects.all()
    base_plant = BasePlant.objects.all()
    # trip_ = DriverTrip.objects.filter(id = driverDocket.tripId).first()
    # return HttpResponse(trip_)
    # AdminTruckNo = AdminTruck.objects.filter(adminTruckNumber = trip_.truckNo).first()
    # clientTruck = ClientTruckConnection.objects.filter(truckNumber = AdminTruckNo.adminTruckNumber).first()
    # return HttpResponse(clientTruck)
    # rateCard = RateCard.objects.filter(rate_card_name = clientTruck.rate_card_name ).first()
    # return HttpResponse(rateCard)
    
    if rctiDocket:
        rctiDocket.docketDate = dateConverterFromTableToPageFormate(rctiDocket.docketDate)
    if driverDocket:
        driverDocket.shiftDate = dateConverterFromTableToPageFormate(driverDocket.shiftDate)
        driverDocket.docketNumber = str(driverDocket.docketNumber)

    params = {
        'rctiDocket': rctiDocket,
        'driverDocket': driverDocket,
        'surcharges': surcharges,
        'basePlants': base_plant,
    }

    return render(request, 'Reconciliation/reconciliation-docket.html', params)

@csrf_protect
@api_view(['POST'])
def reconciliationSetMark(request):
    dockets = request.POST.getlist('dockets[]')
    for docket in dockets:
        getDocket = ReconciliationReport.objects.filter(docketNumber = docket).first()
        getDocket.reconciliationType = 1
        getDocket.save()
    
    return JsonResponse({'status': True})

@csrf_protect
@api_view(['POST'])
def escalationClientCheck(request):
    dockets = request.POST.getlist('dockets[]')
    clientNames = set()
    reconciliationId = []
    available = True
    msg = None
    for docket in dockets:
        getDocket = ReconciliationReport.objects.filter(docketNumber = docket).first()
        clientNames.add(getDocket.clientName)
        existDocket = EscalationDocket.objects.filter(docketNumber=ReconciliationReport.docketNumber, docketDate=getDocket.docketDate).first()
        reconciliationId.append(getDocket.id)
        if getDocket.fromDriver == False:
            msg = "Driver data missing from any docket."
            available = False
            break
        elif getDocket.fromRcti == False:
            msg = "RCTI data missing from any docket."
            available = False
            break
        elif existDocket:
            msg = "Docket is already escalate."
            available = False
            break
        
    return JsonResponse({'status':True, 'msg':msg,'clientName' : list(clientNames)[0] ,'reconciliationId': reconciliationId }) if len(clientNames) == 1 and available else JsonResponse({'status':False, 'msg':msg})

def showReconciliationEscalation1(request, reconciliationId, clientName):
    reconciliationList = reconciliationId.split(',')
    reconciliationDockets = []
    for i in reconciliationList:
        obj = ReconciliationReport.objects.filter(pk=i).first()
        obj.docketDate = dateConverterFromTableToPageFormate(obj.docketDate)
        reconciliationDockets.append(obj)
        
    params = {
        'currentClient' : clientName,
        'reconciliationDockets' : reconciliationDockets,
        'clientNames' : Client.objects.all(),
        'reconciliationIdStr' : reconciliationId
    }
    return render(request, 'Reconciliation/escalation-form1.html', params)
    
@csrf_protect
@api_view(['POST'])
def getCostDifference(request):
    reconciliationId = request.POST.get('reconciliationId')
    print(reconciliationId)
    params = {}
    reconciliationData = ReconciliationReport.objects.filter(pk=reconciliationId).first()

    loadKmCostDifference= reconciliationData.driverLoadAndKmCost - reconciliationData.rctiLoadAndKmCost
    if loadKmCostDifference != 0:
        params['loadKmCostDifference'] = [reconciliationData.driverLoadAndKmCost, reconciliationData.rctiLoadAndKmCost, round(loadKmCostDifference,2)]
    surchargeCostDifference= reconciliationData.driverSurchargeCost - reconciliationData.rctiSurchargeCost
    if surchargeCostDifference != 0:
        params['surchargeCostDifference'] = [reconciliationData.driverSurchargeCost, reconciliationData.rctiSurchargeCost, round(surchargeCostDifference,2)]
    waitingTimeCostDifference= reconciliationData.driverWaitingTimeCost - reconciliationData.rctiWaitingTimeCost
    if waitingTimeCostDifference != 0:
        params['waitingTimeCostDifference'] = [reconciliationData.driverWaitingTimeCost, reconciliationData.rctiWaitingTimeCost, round(waitingTimeCostDifference,2)]
    transferKmCostDifference= reconciliationData.driverTransferKmCost - reconciliationData.rctiTransferKmCost
    if transferKmCostDifference != 0:
        params['transferKmCostDifference'] = [reconciliationData.driverTransferKmCost, reconciliationData.rctiTransferKmCost, round(transferKmCostDifference,2)]
    returnKmCostDifference= reconciliationData.driverReturnKmCost - reconciliationData.rctiReturnKmCost
    if returnKmCostDifference != 0:
        params['returnKmCostDifference'] = [reconciliationData.driverReturnKmCost, reconciliationData.rctiReturnKmCost, round(returnKmCostDifference,2)]
    otherCostDifference= reconciliationData.driverOtherCost - reconciliationData.rctiOtherCost
    if otherCostDifference != 0:
        params['otherCostDifference'] = [reconciliationData.driverOtherCost, reconciliationData.rctiOtherCost, round(otherCostDifference,2)]
    standByCostDifference= reconciliationData.driverStandByCost - reconciliationData.rctiStandByCost
    if standByCostDifference != 0:
        params['standByCostDifference'] = [reconciliationData.driverStandByCost, reconciliationData.rctiStandByCost, round(standByCostDifference,2)]
    loadDeficitDifference= reconciliationData.driverLoadDeficit - reconciliationData.rctiLoadDeficit
    if loadDeficitDifference != 0:
        params['loadDeficitDifference'] = [reconciliationData.driverLoadDeficit, reconciliationData.rctiLoadDeficit, loadDeficitDifference]
    totalCostDifference= reconciliationData.driverTotalCost - reconciliationData.rctiTotalCost
    if totalCostDifference != 0:
        params['totalCostDifference'] = [reconciliationData.driverTotalCost, reconciliationData.rctiTotalCost, round(totalCostDifference,2)]
    
    return JsonResponse({ 'status':True, 'params':params })
    
    
@csrf_protect
def createReconciliationEscalation(request, reconciliationIdStr, clientName):
    escalationType = request.POST.get('escalation')
    reconciliationList = reconciliationIdStr.split(',')
    totalAmt = 0
    escalationObj = Escalation()
    escalationObj.userId = request.user
    escalationObj.escalationDate = getCurrentDateTimeObj().date()
    escalationObj.escalationType = escalationType
    escalationObj.clientName = Client.objects.filter(name=clientName).first()
    escalationObj.save()

    for rId in reconciliationList:
        recObj = ReconciliationReport.objects.filter(pk=rId).first()

        # Move to short paid or write-of 
        
        recObj.reconciliationType = 3 if escalationType == 'Internal' else 2
        recObj.save()

        driverDocketObj = DriverDocket.objects.filter(docketNumber=recObj.docketNumber, shiftDate=recObj.docketDate).first()
        escalationDocketObj = EscalationDocket()
        escalationDocketObj.docketNumber = recObj.docketNumber
        escalationDocketObj.docketDate = recObj.docketDate
        escalationDocketObj.escalationId = escalationObj
        escalationDocketObj.amount = round(recObj.driverTotalCost - recObj.rctiTotalCost, 2)
        escalationDocketObj.invoiceFile = driverDocketObj.docketFile
        escalationDocketObj.save()
        totalAmt += escalationDocketObj.amount

    escalationObj.escalationAmount = totalAmt
    escalationObj.save()
    return redirect('Account:showReconciliationEscalation2', escalationObj.id)


def showReconciliationEscalation2(request, escalationId):
    escalationObj = Escalation.objects.filter(pk=escalationId).first()
    oldMail = EscalationMail.objects.filter(escalationId=escalationObj)
    
    params = {
        'oldMail' : oldMail,
        'escalationObj' : escalationObj
    }
    return render(request, 'Reconciliation/escalation-form2.html', params)


@csrf_protect
def reconciliationEscalationForm3(request ,id):
    escalationObj = Escalation.objects.filter(pk=id).first()

    remark = request.POST.get('remark')
    if remark:
        escalationObj.remark = remark
        
    if escalationObj.escalationStep <= 3:
        escalationObj.escalationStep = 3
        
    escalationObj.save()
    params = {
        'escalationObj':escalationObj
    }
    return render(request, 'Reconciliation/escalation-form3.html',params)
    

@csrf_protect
def reconciliationEscalationMailAdd(request, id):
    escalationObj = Escalation.objects.filter(pk=id).first()
    mailTo = request.POST.get('mailTo')
    mailFrom = request.POST.get('mailFrom')
    mailSubject = request.POST.get('mailSubject')
    mailDescription = request.POST.get('mailDescription')
    mailType = request.POST.get('mailType')
   
    currentDate = getCurrentDateTimeObj().date()
    oldMailCount = EscalationMail.objects.filter(escalationId=escalationObj).count()
    
    escalationMailObj = EscalationMail()
    escalationMailObj.escalationId = escalationObj
    escalationMailObj.userId = request.user
    escalationMailObj.mailTo = mailTo
    escalationMailObj.mailFrom = mailFrom 
    escalationMailObj.mailSubject = mailSubject
    escalationMailObj.mailDescription = mailDescription
    escalationMailObj.mailType = mailType
    escalationMailObj.mailDate = currentDate
    escalationMailObj.mailCount = oldMailCount + 1    

    mailFile = request.FILES.get('mailAttechment')
    if mailFile:
        time = getCurrentTimeInString()
        attachmentPath = 'static/img/mailAttachment'
        fileName = mailFile.name
        convertedFileName = time + '!_@' + fileName
        pfs = FileSystemStorage(location=attachmentPath)
        pfs.save(convertedFileName, mailFile)
        escalationMailObj.mailAttachment = f'static/img/mailAttachment/{convertedFileName}'
    
    escalationMailObj.save()
    
    messages.success(request, "Mail added successfully.")
    return redirect(request.META.get('HTTP_REFERER'))


@csrf_protect
def reconciliationEscalationComplete(request, id):
    escalationObj = Escalation.objects.filter(pk=id).first()
    if request.POST.get('remark'):
        escalationObj.remark = request.POST.get('remark')
        
    escalationObj.escalationStep = 4
    escalationObj.save()
        
    messages.success(request, "Escalation completed successfully.")
    # return redirect(request.META.get('HTTP_REFERER'))
    return redirect('Account:index')
    
    

# ```````````````````````````````````
# Public holiday
# ```````````````````````````````````

def publicHoliday(request):
    data = PublicHoliday.objects.all()
    params = {
        'data': data
    }
    return render(request, 'Account/Tables/PublicHoliday.html', params)


def publicHolidayForm(request, id=None):
    data = None
    if id:
        data = PublicHoliday.objects.get(pk=id)
        data.date = dateConverterFromTableToPageFormate(data.date)
    params = {
        'data': data
    }
    return render(request, 'Account/PublicHolidayForm.html', params)



@csrf_protect
@api_view(['POST'])
def publicHolidaySave(request, id=None):
    dataList = {
        'date': request.POST.get('date'),
        'stateName': request.POST.get('state'),
        'description': request.POST.get('description')
    }
    if id:
        updateIntoTable(
            record_id=id, tableName='PublicHoliday', dataSet=dataList)
        messages.success(request, 'Holiday updated successfully')
    else:
        insertIntoTable(tableName='PublicHoliday', dataSet=dataList)
        messages.success(request, 'Holiday added successfully')

    return redirect('Account:publicHoliday')


# ````````````````````````````````````
# Rate Card

# ```````````````````````````````````

def rateCardTable(request,clientId = None):
    
    RateCards = RateCard.objects.filter(clientName=clientId)
    params = {
        'rateCard': RateCards,
        'clientId':clientId,
    }
    return render(request, 'Account/Tables/rateCardTable.html', params)


def rateCardForm(request, id=None , clientId=None):
    rateCard = rateCardSurcharges = surchargesEntry = costParameters = thresholdDayShift = thresholdNightShift = grace = onLease = tds = startDate = endDate = None
    surchargesEntry =Surcharge.objects.all()
    rateCardDates = []
    if id:
        rateCard = RateCard.objects.get(pk=id)
        tds = rateCard.tds
        
        costParameters = CostParameters.objects.filter(rate_card_name=rateCard.id).order_by('-end_date').values()
       
        for obj in costParameters:
            rateCardDates.append(str(obj['start_date']) + ' to ' + str(obj['end_date']))
        
        getOldRateCard = request.POST.get('rateCard') 
        
        if getOldRateCard:
            oldRateCardStartDate = getOldRateCard.split('to')[0].strip()
            oldRateCardEndDate = getOldRateCard.split('to')[1].strip()

            costParameters = CostParameters.objects.filter(rate_card_name=rateCard.id, start_date = oldRateCardStartDate, end_date = oldRateCardEndDate).values().first()
            thresholdDayShift = ThresholdDayShift.objects.filter(rate_card_name=rateCard.id, start_date = oldRateCardStartDate, end_date = oldRateCardEndDate).values().first()
            thresholdNightShift = ThresholdNightShift.objects.filter(rate_card_name=rateCard.id, start_date = oldRateCardStartDate, end_date = oldRateCardEndDate).values().first()
            grace = Grace.objects.filter(rate_card_name=rateCard.id, start_date = oldRateCardStartDate, end_date = oldRateCardEndDate).values().first()
            rateCardSurcharges =RateCardSurchargeValue.objects.filter(rate_card_name= rateCard.id, start_date=oldRateCardStartDate, end_date= oldRateCardEndDate)
            
        else:
            costParameters = CostParameters.objects.filter(rate_card_name=rateCard.id).order_by('-end_date').values().first()
            thresholdDayShift = ThresholdDayShift.objects.filter(rate_card_name=rateCard.id).order_by('-end_date').values().first()
            thresholdNightShift = ThresholdNightShift.objects.filter(rate_card_name=rateCard.id).order_by('-end_date').values().first()
            grace = Grace.objects.filter(rate_card_name=rateCard.id).order_by('-end_date').values().first()
            rateCardSurcharges =RateCardSurchargeValue.objects.filter(rate_card_name= rateCard.id, start_date=costParameters['start_date'], end_date= costParameters['end_date'])

        # onLease = OnLease.objects.filter(rate_card_name = rateCard.id, end_date = None).values().first()

        startDate = dateConverterFromTableToPageFormate(costParameters['start_date'])
        endDate = dateConverterFromTableToPageFormate(costParameters['end_date'])

    # return HttpResponse(rateCard)
    params = {
        'rateCard': rateCard,
        'costParameters': costParameters,
        'thresholdDayShift': thresholdDayShift,
        'thresholdNightShift': thresholdNightShift,
        'grace': grace,
        'tds': tds,
        'rateCardSurcharges': rateCardSurcharges,
        'surchargesEntry': surchargesEntry,
        'startDate' : startDate,
        'endDate' : endDate,
        'rateCardDates' : rateCardDates,
        'clientId':clientId,
        # 'onLease' : onLease,
    }
    return render(request, 'Account/rateCardForm.html', params)

@csrf_protect
def getOldRateCards(request):
    rateCardDates = []
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    rateCard = RateCard.objects.filter(pk=request.POST.get('rateCardId')).first()
    costParameters = CostParameters.objects.filter(Q(rate_card_name=rateCard,end_date__gte = startDate,start_date__lte = endDate)|Q(rate_card_name=rateCard,start_date__gte = startDate,end_date__lte = endDate)).values()

    for obj in costParameters:
        rateCardDates.append(str(obj['start_date']) + ' to ' + str(obj['end_date']))

    return JsonResponse({'status':True, 'rateCardDates':rateCardDates})

def checkOnOff(val_):
    return True if str(val_) =='on' else False


@csrf_protect
@api_view(['POST'])
def rateCardSave(request, id=None, edit=0):

        # surcharge.id = request.POST.get('surcharge.id')
        # print(surcharge.surcharge_Name)
    # return HttpResponse(request.POST.get('clientName'))
    # print(type(request.POST.get('costParameters_start_date')))
    # return HttpResponse('work')
    # Rate Card
    rateCardID = None
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    surchargeEntry = Surcharge.objects.all()
    if not id:
        rateCard = RateCard()
        rateCard.rate_card_name=request.POST.get('rate_card_name')
        # tds = float(request.POST.get('rate_card_tds'))
        # rateCard.tds = tds
        clientId =request.POST.get('clientName')
        rateCard.clientName = Client.objects.filter(pk = clientId).first()
        rateCard.save()
        rateCardID = RateCard.objects.filter(rate_card_name=request.POST.get('rate_card_name')).first()

    else:
        rateCardID = RateCard.objects.filter(pk=id).first()
        
        # existingCostParameter = CostParameters.objects.filter(Q(rateCard=rateCardID) & (Q(start_date__range=(startDate, endDate)) | Q(end_date__range=(startDate, endDate))))
        if edit == 0:
            existingCostParameter = CostParameters.objects.filter(rate_card_name=rateCardID,start_date__lte = startDate,end_date__gte = startDate).first()
            existingThresholdDayShift = ThresholdDayShift.objects.filter(rate_card_name=rateCardID,start_date__lte = startDate,end_date__gte = startDate).first()
            existingThresholdNightShift = ThresholdNightShift.objects.filter(rate_card_name=rateCardID,start_date__lte = startDate,end_date__gte = startDate).first()
            existingGrace = Grace.objects.filter(rate_card_name=rateCardID,start_date__lte = startDate,end_date__gte = startDate).first()
            rateCardSurchargeObj = RateCardSurchargeValue.objects.filter(rate_card_name = rateCardID,start_date__lte = startDate,end_date__gte = startDate)
            for surcharge in rateCardSurchargeObj:
                surcharge.surchargeValue = request.POST.get(f'{surcharge.id}')
                surcharge.start_date = startDate
                surcharge.end_date = endDate
                surcharge.save()

            if existingCostParameter or existingThresholdDayShift or existingThresholdNightShift or existingGrace:
                messages.error(request, "Rate card rates already exist between given date.")
                return redirect(request.META.get('HTTP_REFERER'))

        # tds = float(request.POST.get('rate_card_tds'))
        # rateCardID.tds = tds
        # rateCardID.save()

        # oldCostParameters = CostParameters.objects.get(
        #     rate_card_name=rateCardID.id, end_date=None)
        # oldCostParameters.end_date = getYesterdayDate(
        #     request.POST.get('costParameters_start_date'))
        # oldCostParameters.save()

        # oldThresholdDayShift = ThresholdDayShift.objects.get(
        #     rate_card_name=rateCardID.id, end_date=None)
        # oldThresholdDayShift.end_date = getYesterdayDate(
        #     request.POST.get('thresholdDayShift_start_date'))
        # oldThresholdDayShift.save()

        # oldThresholdNightShift = ThresholdNightShift.objects.get(
        #     rate_card_name=rateCardID.id, end_date=None)
        # oldThresholdNightShift.end_date = getYesterdayDate(
        #     request.POST.get('thresholdNightShift_start_date'))
        # oldThresholdNightShift.save()

        # oldGrace = Grace.objects.get(
        #     rate_card_name=rateCardID.id, end_date=None)
        # oldGrace.end_date = getYesterdayDate(
        #     request.POST.get('grace_start_date'))
        # oldGrace.save()

        # oldOnLease = OnLease.objects.get(
        #     rate_card_name=rateCardID.id, end_date=None)
        # oldOnLease.end_date = getYesterdayDate(
        #     request.POST.get('onLease_start_date'))
        # oldOnLease.save()

    # CostParameters
    # surchargeObj = Surcharge.objects.get(pk=request.POST.get('costParameters_surcharge_type'))
    updatedValues= []
    
    #  Get object according to type of save
    if edit == 0:
        costParameters = CostParameters()
        thresholdDayShifts = ThresholdDayShift()
        thresholdNightShifts = ThresholdNightShift()
        grace = Grace()
        
        for surcharge in surchargeEntry:
            rateCardSurchargeObj = RateCardSurchargeValue() 
            rateCardSurchargeObj.rate_card_name = rateCardID
            rateCardSurchargeObj.surcharge = surcharge
            rateCardSurchargeObj.surchargeValue = request.POST.get(f'{surcharge.id}')
            rateCardSurchargeObj.start_date = startDate
            rateCardSurchargeObj.end_date = endDate
            rateCardSurchargeObj.save()
        
    else:
        costParameters = CostParameters.objects.filter(rate_card_name = rateCardID,start_date__lte = startDate,end_date__gte = startDate).first()
        thresholdDayShifts = ThresholdDayShift.objects.filter(rate_card_name = rateCardID,start_date__lte = startDate,end_date__gte = startDate).first()
        thresholdNightShifts = ThresholdNightShift.objects.filter(rate_card_name = rateCardID,start_date__lte = startDate,end_date__gte = startDate).first()
        grace = Grace.objects.filter(rate_card_name = rateCardID,start_date__lte = startDate,end_date__gte = startDate).first()
        rateCardSurchargeObj = RateCardSurchargeValue.objects.filter(rate_card_name = rateCardID,start_date__lte = startDate,end_date__gte = startDate)
        for surcharge in rateCardSurchargeObj:
            surcharge.surchargeValue = request.POST.get(f'{surcharge.id}')
            surcharge.start_date = startDate
            surcharge.end_date = endDate
            surcharge.save()

        # Edit Reconciliation and Past trips
        # Cost parameters
        
        updatedValues.append('costParameters_loading_cost_per_cubic_meter') if costParameters.loading_cost_per_cubic_meter != float(request.POST.get('costParameters_loading_cost_per_cubic_meter')) else None
        updatedValues.append('costParameters_km_cost') if costParameters.km_cost != float(request.POST.get('costParameters_km_cost')) else None
        updatedValues.append('costParameters_transfer_cost') if costParameters.transfer_cost != float(request.POST.get('costParameters_transfer_cost')) else None
        updatedValues.append('costParameters_return_load_cost') if costParameters.return_load_cost != float(request.POST.get('costParameters_return_load_cost')) else None
        updatedValues.append('costParameters_return_km_cost') if costParameters.return_km_cost != float(request.POST.get('costParameters_return_km_cost')) else None
        updatedValues.append('costParameters_standby_time_slot_size') if costParameters.standby_time_slot_size != float(request.POST.get('costParameters_standby_time_slot_size')) else None
        updatedValues.append('costParameters_standby_cost_per_slot') if costParameters.standby_cost_per_slot != float(request.POST.get('costParameters_standby_cost_per_slot')) else None
        updatedValues.append('costParameters_waiting_cost_per_minute') if costParameters.waiting_cost_per_minute != float(request.POST.get('costParameters_waiting_cost_per_minute')) else None
        updatedValues.append('costParameters_call_out_fees') if costParameters.call_out_fees != float(request.POST.get('costParameters_call_out_fees')) else None
        updatedValues.append('costParameters_demurrage_fees') if costParameters.demurrage_fees != float(request.POST.get('costParameters_demurrage_fees')) else None
        updatedValues.append('costParameters_cancellation_fees') if costParameters.cancellation_fees != float(request.POST.get('costParameters_cancellation_fees')) else None

        # ThresholdDayShift 
        updatedValues.append('thresholdDayShift_threshold_amount_per_day_shift') if thresholdDayShifts.threshold_amount_per_day_shift != float(request.POST.get('thresholdDayShift_threshold_amount_per_day_shift')) else None
        updatedValues.append('thresholdDayShift_min_load_in_cubic_meters') if thresholdDayShifts.min_load_in_cubic_meters != float(request.POST.get('thresholdDayShift_min_load_in_cubic_meters')) else None
        updatedValues.append('thresholdDayShift_min_load_in_cubic_meters_return_to_yard') if thresholdDayShifts.min_load_in_cubic_meters_return_to_yard != float(request.POST.get('thresholdDayShift_min_load_in_cubic_meters_return_to_yard')) else None
        updatedValues.append('thresholdDayShift_return_to_yard_grace') if thresholdDayShifts.return_to_yard_grace != float(request.POST.get('thresholdDayShift_return_to_yard_grace')) else None
        updatedValues.append('thresholdDayShift_return_to_tipping_grace') if thresholdDayShifts.return_to_tipping_grace != float(request.POST.get('thresholdDayShift_return_to_tipping_grace')) else None
        
        updatedValues.append('thresholdDayShift_loading_cost_per_cubic_meter_included') if thresholdDayShifts.loading_cost_per_cubic_meter_included != checkOnOff(request.POST.get('thresholdDayShift_loading_cost_per_cubic_meter_included')) else None
        updatedValues.append('thresholdDayShift_km_cost_included') if thresholdDayShifts.km_cost_included != checkOnOff(request.POST.get('thresholdDayShift_km_cost_included')) else None
        updatedValues.append('thresholdDayShift_surcharge_included') if thresholdDayShifts.surcharge_included != checkOnOff(request.POST.get('thresholdDayShift_surcharge_included')) else None
        updatedValues.append('thresholdDayShift_transfer_cost_included') if thresholdDayShifts.transfer_cost_included != checkOnOff(request.POST.get('thresholdDayShift_transfer_cost_included')) else None
        updatedValues.append('thresholdDayShift_return_cost_included') if thresholdDayShifts.return_cost_included != checkOnOff(request.POST.get('thresholdDayShift_return_cost_included')) else None
        updatedValues.append('thresholdDayShift_standby_cost_included') if thresholdDayShifts.standby_cost_included != checkOnOff(request.POST.get('thresholdDayShift_standby_cost_included')) else None
        updatedValues.append('thresholdDayShift_waiting_cost_included') if thresholdDayShifts.waiting_cost_included != checkOnOff(request.POST.get('thresholdDayShift_waiting_cost_included')) else None
        updatedValues.append('thresholdDayShift_call_out_fees_included') if thresholdDayShifts.call_out_fees_included != checkOnOff(request.POST.get('thresholdDayShift_call_out_fees_included')) else None
        
        # ThresholdNightShift 
        updatedValues.append('thresholdNightShift_threshold_amount_per_night_shift') if thresholdNightShifts.threshold_amount_per_night_shift != float(request.POST.get('thresholdNightShift_threshold_amount_per_night_shift')) else None
        updatedValues.append('thresholdNightShift_min_load_in_cubic_meters') if thresholdNightShifts.min_load_in_cubic_meters != float(request.POST.get('thresholdNightShift_min_load_in_cubic_meters')) else None
        updatedValues.append('thresholdNightShift_min_load_in_cubic_meters_return_to_yard') if thresholdNightShifts.min_load_in_cubic_meters_return_to_yard != float(request.POST.get('thresholdNightShift_min_load_in_cubic_meters_return_to_yard')) else None
        updatedValues.append('thresholdNightShift_return_to_yard_grace') if thresholdNightShifts.return_to_yard_grace != float(request.POST.get('thresholdNightShift_return_to_yard_grace')) else None
        updatedValues.append('thresholdNightShift_return_to_tipping_grace') if thresholdNightShifts.return_to_tipping_grace != float(request.POST.get('thresholdNightShift_return_to_tipping_grace')) else None
        
        updatedValues.append('thresholdNightShift_loading_cost_per_cubic_meter_included') if thresholdNightShifts.loading_cost_per_cubic_meter_included != checkOnOff(request.POST.get('thresholdNightShift_loading_cost_per_cubic_meter_included')) else None
        updatedValues.append('thresholdNightShift_km_cost_included') if thresholdNightShifts.km_cost_included != checkOnOff(request.POST.get('thresholdNightShift_km_cost_included')) else None
        updatedValues.append('thresholdNightShift_surcharge_included') if thresholdNightShifts.surcharge_included != checkOnOff(request.POST.get('thresholdNightShift_surcharge_included')) else None
        updatedValues.append('thresholdNightShift_transfer_cost_included') if thresholdNightShifts.transfer_cost_included != checkOnOff(request.POST.get('thresholdNightShift_transfer_cost_included')) else None
        updatedValues.append('thresholdNightShift_return_cost_included') if thresholdNightShifts.return_cost_included != checkOnOff(request.POST.get('thresholdNightShift_return_cost_included')) else None
        updatedValues.append('thresholdNightShift_standby_cost_included') if thresholdNightShifts.standby_cost_included != checkOnOff(request.POST.get('thresholdNightShift_standby_cost_included')) else None
        updatedValues.append('thresholdNightShift_waiting_cost_included') if thresholdNightShifts.waiting_cost_included != checkOnOff(request.POST.get('thresholdNightShift_waiting_cost_included')) else None
        updatedValues.append('thresholdNightShift_call_out_fees_included') if thresholdNightShifts.call_out_fees_included != checkOnOff(request.POST.get('thresholdNightShift_call_out_fees_included')) else None
        
        # Grace 
        updatedValues.append('load_km_grace') if grace.load_km_grace != float(request.POST.get('grace_load_km_grace')) else None
        updatedValues.append('transfer_km_grace') if grace.transfer_km_grace != float(request.POST.get('grace_transfer_km_grace')) else None
        updatedValues.append('return_km_grace') if grace.return_km_grace != float(request.POST.get('grace_return_km_grace')) else None
        updatedValues.append('standby_time_grace_in_minutes') if grace.standby_time_grace_in_minutes != float(request.POST.get('grace_standby_time_grace_in_minutes')) else None
        updatedValues.append('chargeable_standby_time_starts_after') if grace.chargeable_standby_time_starts_after != float(request.POST.get('grace_chargeable_standby_time_starts_after')) else None
        updatedValues.append('waiting_time_grace_in_minutes') if grace.waiting_time_grace_in_minutes != float(request.POST.get('grace_waiting_time_grace_in_minutes')) else None
        updatedValues.append('chargeable_waiting_time_starts_after') if grace.chargeable_waiting_time_starts_after != float(request.POST.get('grace_chargeable_waiting_time_starts_after')) else None
        
        # return HttpResponse(updatedValues) 

    costParameters.rate_card_name=rateCardID
    costParameters.loading_cost_per_cubic_meter=float(request.POST.get('costParameters_loading_cost_per_cubic_meter'))
    costParameters.km_cost=float(request.POST.get('costParameters_km_cost'))
    costParameters.transfer_cost=float(request.POST.get('costParameters_transfer_cost'))
    costParameters.return_load_cost=float(request.POST.get('costParameters_return_load_cost'))
    costParameters.return_km_cost=float(request.POST.get('costParameters_return_km_cost'))
    costParameters.standby_time_slot_size=float(request.POST.get('costParameters_standby_time_slot_size'))
    costParameters.standby_cost_per_slot=float(request.POST.get('costParameters_standby_cost_per_slot'))
    costParameters.waiting_cost_per_minute=float(request.POST.get('costParameters_waiting_cost_per_minute'))
    costParameters.call_out_fees=float(request.POST.get('costParameters_call_out_fees'))
    costParameters.demurrage_fees=float(request.POST.get('costParameters_demurrage_fees'))
    costParameters.cancellation_fees=float(request.POST.get('costParameters_cancellation_fees'))
    costParameters.start_date=startDate  
    costParameters.end_date=endDate
    costParameters.save()

    # ThresholdDayShift
    thresholdDayShifts.rate_card_name=rateCardID
    thresholdDayShifts.threshold_amount_per_day_shift=float(request.POST.get('thresholdDayShift_threshold_amount_per_day_shift'))
    thresholdDayShifts.loading_cost_per_cubic_meter_included=True if request.POST.get('thresholdDayShift_loading_cost_per_cubic_meter_included') == 'on' else False
    thresholdDayShifts.km_cost_included=True if request.POST.get('thresholdDayShift_km_cost_included') == 'on' else False
    thresholdDayShifts.surcharge_included=True if request.POST.get('thresholdDayShift_surcharge_included') == 'on' else False
    thresholdDayShifts.transfer_cost_included=True if request.POST.get('thresholdDayShift_transfer_cost_included') == 'on' else False
    thresholdDayShifts.return_cost_included=True if request.POST.get('thresholdDayShift_return_cost_included') == 'on' else False
    thresholdDayShifts.standby_cost_included=True if request.POST.get('thresholdDayShift_standby_cost_included') == 'on' else False
    thresholdDayShifts.waiting_cost_included=True if request.POST.get('thresholdDayShift_waiting_cost_included') == 'on' else False
    thresholdDayShifts.call_out_fees_included=True if request.POST.get('thresholdDayShift_call_out_fees_included') == 'on' else False
    thresholdDayShifts.min_load_in_cubic_meters=float(request.POST.get('thresholdDayShift_min_load_in_cubic_meters'))
    thresholdDayShifts.min_load_in_cubic_meters_return_to_yard=float(request.POST.get('thresholdDayShift_min_load_in_cubic_meters_return_to_yard'))
    thresholdDayShifts.return_to_yard_grace=float(request.POST.get('thresholdDayShift_return_to_yard_grace'))
    thresholdDayShifts.return_to_tipping_grace=float(request.POST.get('thresholdDayShift_return_to_tipping_grace'))
    thresholdDayShifts.start_date=startDate
    thresholdDayShifts.end_date=endDate
    thresholdDayShifts.save()

    # ThresholdNightShift
    thresholdNightShifts.rate_card_name=rateCardID
    thresholdNightShifts.threshold_amount_per_night_shift=float(request.POST.get('thresholdNightShift_threshold_amount_per_night_shift'))
    thresholdNightShifts.loading_cost_per_cubic_meter_included=True if request.POST.get('thresholdNightShift_loading_cost_per_cubic_meter_included') == 'on' else False
    thresholdNightShifts.km_cost_included=True if request.POST.get('thresholdNightShift_km_cost_included') == 'on' else False
    thresholdNightShifts.surcharge_included=True if request.POST.get('thresholdNightShift_surcharge_included') == 'on' else False
    thresholdNightShifts.transfer_cost_included=True if request.POST.get('thresholdNightShift_transfer_cost_included') == 'on' else False
    thresholdNightShifts.return_cost_included=True if request.POST.get('thresholdNightShift_return_cost_included') == 'on' else False
    thresholdNightShifts.standby_cost_included=True if request.POST.get('thresholdNightShift_standby_cost_included') == 'on' else False
    thresholdNightShifts.waiting_cost_included=True if request.POST.get('thresholdNightShift_waiting_cost_included') == 'on' else False
    thresholdNightShifts.call_out_fees_included=True if request.POST.get('thresholdNightShift_call_out_fees_included') == 'on' else False
    thresholdNightShifts.min_load_in_cubic_meters=float(request.POST.get('thresholdNightShift_min_load_in_cubic_meters'))
    thresholdNightShifts.min_load_in_cubic_meters_return_to_yard=float(request.POST.get('thresholdNightShift_min_load_in_cubic_meters_return_to_yard'))
    thresholdNightShifts.return_to_yard_grace=float(request.POST.get('thresholdNightShift_return_to_yard_grace'))
    thresholdNightShifts.return_to_tipping_grace=float(request.POST.get('thresholdNightShift_return_to_tipping_grace'))
    thresholdNightShifts.start_date=startDate
    thresholdNightShifts.end_date=endDate
    thresholdNightShifts.save()

    # Grace
    grace.rate_card_name=rateCardID
    grace.load_km_grace=float(request.POST.get('grace_load_km_grace'))
    grace.transfer_km_grace=float(request.POST.get('grace_transfer_km_grace'))
    grace.return_km_grace=float(request.POST.get('grace_return_km_grace'))
    grace.standby_time_grace_in_minutes=float(request.POST.get('grace_standby_time_grace_in_minutes'))
    grace.chargeable_standby_time_starts_after=float(request.POST.get('grace_chargeable_standby_time_starts_after'))
    grace.waiting_time_grace_in_minutes=float(request.POST.get('grace_waiting_time_grace_in_minutes'))
    grace.chargeable_waiting_time_starts_after=float(request.POST.get('grace_chargeable_waiting_time_starts_after'))
    grace.start_date=startDate
    grace.end_date=endDate
    grace.save()
    

    
    updatedValues.insert(0,rateCardID.id)
    updatedValues.insert(1,startDate)
    updatedValues.insert(2,endDate)

    with open("scripts/updateTripsAndReconciliationData.txt",'w+',encoding='utf-8') as f:
        for val in updatedValues:
            f.write(str(val) + ',')

    if edit != 0:

        colorama.AnsiToWin32.stream = None
        os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
        cmd = ["python", "manage.py", "runscript", 'updateTripsAndReconciliationData','--continue-on-error']
        subprocess.Popen(cmd, stdout=subprocess.PIPE)
    # onLease = OnLease(
    #     rate_card_name=rateCardID,
    #     hourly_subscription_charge = float(request.POST.get('onLease_hourly_subscription_charge')),
    #     daily_subscription_charge = float(request.POST.get('onLease_daily_subscription_charge')),
    #     monthly_subscription_charge = float(request.POST.get('onLease_monthly_subscription_charge')),
    #     quarterly_subscription_charge = float(request.POST.get('onLease_quarterly_subscription_charge')),
    #     surcharge_fixed_normal_cost_included = True if request.POST.get('onLease_surcharge_fixed_normal_cost_included') == 'on' else False,
    #     surcharge_fixed_sunday_cost_included = True if request.POST.get('onLease_surcharge_fixed_sunday_cost_included') == 'on' else False,
    #     surcharge_fixed_public_holiday_cost_included = True if request.POST.get('onLease_surcharge_fixed_public_holiday_cost_included') == 'on' else False,
    #     surcharge_per_cubic_meters_normal_cost_included = True if request.POST.get('onLease_surcharge_per_cubic_meters_normal_cost_included') == 'on' else False,
    #     surcharge_per_cubic_meters_sunday_cost_included = True if request.POST.get('onLease_surcharge_per_cubic_meters_sunday_cost_included') == 'on' else False,
    #     surcharge_per_cubic_meters_public_holiday_cost_included = True if request.POST.get('onLease_surcharge_per_cubic_meters_public_holiday_cost_included') == 'on' else False,
    #     transfer_cost_applicable = True if request.POST.get('onLease_transfer_cost_applicable') == 'on' else False,
    #     return_cost_applicable = True if request.POST.get('onLease_return_cost_applicable') == 'on' else False,
    #     standby_cost_per_slot_applicable = True if request.POST.get('onLease_standby_cost_per_slot_applicable') == 'on' else False,
    #     waiting_cost_per_minute_applicable = True if request.POST.get('onLease_waiting_cost_per_minute_applicable') == 'on' else False,
    #     call_out_fees_applicable = True if request.POST.get('onLease_call_out_fees_applicable') == 'on' else False,
    #     start_date = request.POST.get('onLease_start_date')

    # )
    # onLease.save()

    messages.success(request, 'Data successfully add ')
    return redirect('gearBox:clientTable')



# ```````````````````````````````````
# Past trip
# ```````````````````````````````````


def PastTripForm(request):
    pastTripErrors = PastTripError.objects.filter(status = False).values()
    pastTripSolved = PastTripError.objects.filter(status = True).values()
    params = {
       'pastTripErrors' : pastTripErrors ,
       'pastTripSolved' :pastTripSolved
    }
    return render(request, 'Account/pastTrip.html', params)

def pastTripErrorSolve(request, id):
    # print(f'message{id}')
    errorObj = PastTripError.objects.filter(pk=id).first()

    # Check if errorObj is not None before proceeding
    if errorObj:
        tripObj = DriverTrip.objects.filter(shiftDate=errorObj.tripDate, truckNo=errorObj.truckNo).first()
        if tripObj:
            url_name = reverse('Account:pastTripErrorResolve', kwargs={'ids': tripObj.id, 'errorId': errorObj.id})
            return redirect(url_name)
        else:
            return HttpResponse("Error: Trip not found")
    else:
        return HttpResponse("Error: PastTripError not found")


def resolveError(request, id):
    resolveErrorObj = PastTripError.objects.filter(pk=id).first()
    tripObj = DriverTrip.objects.filter(shiftDate=resolveErrorObj.tripDate, truckNo=resolveErrorObj.truckNo).first()
    # return HttpResponse(tripObj.id)
    # url_name = reverse('Account:DriverTripEditForm', kwargs={'id': tripObj.id})
    return redirect('Account:DriverTripEdit',id=tripObj.id)
    return redirect(url_name)
    


@csrf_protect
@api_view(['POST'])
def pastTripSave(request):

    monthAndYear = str(request.POST.get('monthAndYear'))
    save = int(request.POST.get('save'))
    clientName = request.POST.get('clientName')
    pastTrip_csv_file = request.FILES.get('pastTripFile')
    if not pastTrip_csv_file:
        return HttpResponse("No file uploaded")
    try:
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]
        
        newFileName = time + "@_!" + (str(pastTrip_csv_file.name)).replace(' ','')

        location = 'static/Account/PastTripsEntry'
        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, pastTrip_csv_file)
        with open("pastTrip_entry_month.txt",'w') as f:
            f.write(monthAndYear)
                        
        with open("pastTrip_entry.txt", 'w') as f:
            f.write(newFileName)
        if save == 1 :
            
            if clientName == 'boral':
                colorama.AnsiToWin32.stream = None
                os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
                cmd = ["python", "manage.py", "runscript", 'PastDataSave','--continue-on-error']
                subprocess.Popen(cmd, stdout=subprocess.PIPE)
            elif clientName == 'holcim':
                return HttpResponse('work in progress')
                colorama.AnsiToWin32.stream = None
                os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
                cmd = ["python", "manage.py", "runscript", 'holcim','--continue-on-error']
                subprocess.Popen(cmd, stdout=subprocess.PIPE)
        messages.success(request, "Please wait for some time, it takes some time to update the data.")
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def uplodedPastTrip(request):
   
    pastTripFile = os.listdir('static/Account/PastTripsEntry')
    pasrTripFileNameList = []
    for file in pastTripFile:
        pasrTripFileNameList.append([file.split('@_!')[0],file.split('@_!')[1]])
        
    return render(request, 'Account/uplodedPastTrip.html', {'pasrTripFileNameLists' : pasrTripFileNameList})
# --------------------------------------------
# Surcharge 
# ---------------------------------------------

def surchargeTable(request):
    surcharges = Surcharge.objects.all()
    # return HttpResponse(surcharge_)
    return render(request, 'Account/Tables/surchargeTable.html', {'surcharges': surcharges})


def surchargeForm(request, id=None):
    surcharge = None
    if id:
        surcharge = Surcharge.objects.get(pk=id)

    params = {
        'data': surcharge
    }
    # return HttpResponse(params['data'])
    return render(request, "Account/surchargeForm.html", params)


@csrf_protect
@api_view(['POST'])
def surchargeSave(request, id=None):
    dataList = {
        'surcharge_Name': (request.POST.get('surcharge_Name')).strip()
    }
    if id is not None:
        updateIntoTable(record_id=id, tableName='Surcharge', dataSet=dataList)
        messages.success(request, 'Surcharge updated successfully')
    else:
        # return HttpResponse(dataList['surcharge_Name'])
        insertIntoTable(tableName='Surcharge', dataSet=dataList)
        messages.success(request, 'Surcharge added successfully')

    return redirect('Account:surchargeTable')

def DriverShiftForm(request,id):
    pastTripFile = os.listdir('static/Account/PastTripsEntry')
    pasrTripFileNameList = []
    for file in pastTripFile:
        pasrTripFileNameList.append([file.split('@_!')[0],file.split('@_!')[1]])
        
    # return render(request, 'Account/uplodedPastTrip.html', {'pasrTripFileNameLists' : pasrTripFileNameList})
    client = Client.objects.all()
    pastTripErrors = PastTripError.objects.filter(status = False , errorType = 0).values()
    pastTripSolved = PastTripError.objects.filter(status = True , errorType = 0).values()
    # docketObj = DriverDocket.objects.filter(docketnumber = pastTripSolved.docketNumber).values9
    params ={
            'clients': client,
            'id':id,
            'pasrTripFileNameLists' : pasrTripFileNameList,
            'pastTripErrors' : pastTripErrors ,
            'pastTripSolved' :pastTripSolved,
        }      
    return render(request, 'Account/driverShiftForm.html',params)


@csrf_protect
def  ShiftDetails(request,id):
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    id_ = id
    shifts = DriverShift.objects.filter(shiftDate__range=(startDate, endDate), verified= False )
    for shift in shifts:
        shift.driverName = Driver.objects.filter(pk = shift.driverId).first().name
    # if id == 0:
    #     if clientId != 0:
    #         pass
    #     else:
    #         trips = DriverShiftTrip.objects.filter(shiftDate__range=(startDate, endDate) ,verified = False)
    # elif id == 1:
    #     if clientId != 0:
    #         trips = DriverShiftTrip.objects.filter(shiftDate__range=(startDate, endDate) ,verified = True , clientName = clientNameObj)
    #     else:
    #         trips = DriverShiftTrip.objects.filter(shiftDate__range=(startDate, endDate) ,verified = True)

    # else:
    #     messages.warning( request, "Invalid Request")
    #     return redirect(request.META.get('HTTP_REFERER'))
    params = {
        'shifts': shifts,
        'startDate': startDate,
        'endDate': endDate,
        'id_': id_,
        
        }
    return render(request, 'Account/Tables/driverTripsTable.html', params)
    
@csrf_protect
def driverShiftCsv(request):
    data_list = []
    temp_trip_data_list = []
    temp_docket_data_list = []
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    id_ = request.POST.get('id_')
    id_ =True if int(id_) == 1 else False

    # if verified_ == '1':
    #     driver_trip = DriverTrip.objects.filter(verified=True).values()
    # elif verified_ == '0':
    #     driver_trip = DriverTrip.objects.filter(verified=False).values()
    # elif ClientId:
    #     driver_trip = DriverTrip.objects.filter(clientName=ClientId).values()
    #     foreignKeySet(driver_trip)
    if startDate and endDate:
        
        driver_trip = DriverTrip.objects.filter(shiftDate__range=(startDate, endDate),verified = True if id_ ==1 else False).values()
        foreignKeySet(driver_trip)
    else:
        driver_trip = DriverTrip.objects.all().values()

    try:
        for trip in driver_trip:
            temp_trip_data_list.append([
                trip['verified'],
                trip['driverId_id'],
                trip['clientName_id'],
                trip['shiftType'],
                trip['numberOfLoads'],
                trip['truckNo'],
                trip['shiftDate'],
                trip['startTime'],
                trip['endTime'],
                trip['loadSheet'],
                trip['comment'],
            ])
            related_dockets = DriverDocket.objects.filter(
                tripId=trip['id']).values_list()
            if related_dockets:
                for docket in related_dockets:
                    basePlant_ = BasePlant.objects.filter(id = int(docket[5])).first()
                    docket = list(docket)
                    docket[5] = basePlant_.basePlant
                    temp_docket_data_list.append(docket)
                for i in range(len(temp_docket_data_list)):
                    data_list.append(
                        temp_trip_data_list[0] + temp_docket_data_list[i])
                temp_trip_data_list.clear()
                temp_docket_data_list.clear()
            else:
                data_list.extend(temp_trip_data_list)
                temp_trip_data_list.clear()
    except Exception as e:
        return HttpResponse(e)

    time = str(timezone.now()).replace(':', '').replace(
        '-', '').replace(' ', '').split('.')
    newFileName = time[0]
    location = 'static/Account/DriverTripCsvDownload/'
    lfs = FileSystemStorage(location=location)
    csv_filename = newFileName + '.csv'

    header = ['verified', 'driverId', 'clientName', 'shiftType', 'numberOfLoads', 'truckNo', 'shiftDate', 'startTime', 'endTime', 'loadSheet', 'comment', 'docketId', 'shiftDatetripId', 'tripId', 'docketNumber',
              'docketFile', 'basePlant', 'noOfKm', 'transferKM', 'returnToYard', 'tippingToYard', 'returnQty', 'returnKm', 'waitingTimeStart', 'waitingTimeEnd', 'totalWaitingInMinute', 'surcharge_type', 'surcharge_duration',
              'cubicMl', 'standByStartTime', 'standByEndTime','minimumLoad', 'others', 'comment'
            ]

    file_name = location + csv_filename

    # Open the CSV file in append mode ('a')
    myFile = open(file_name, 'a', newline='')
    writer = csv.writer(myFile)
    writer.writerow(header)
    writer.writerows(data_list)
    myFile.close()
    return FileResponse(open(f'static/Account/DriverTripCsvDownload/{csv_filename}', 'rb'), as_attachment=True)

def topUpForm(request,id , topUpDocket = None):
    escalationData = None
    rctiError = None
    client = Client.objects.all()
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    rctiError = RctiErrors.objects.filter(pk=id).first()
    clientNameObj = Client.objects.filter(name = rctiError.clientName).first()
    if topUpDocket:
        escalationData = Escalation.objects.filter(clientName = clientNameObj , escalationDate__range = (startDate , endDate ), escalationType = 'External', escalationStep = 3).values()
    formName = None 
    formName = 'Top Up' if rctiError.data else None
    formName = 'Accommodation' if rctiError.data else None
    params = {
        'errorId':rctiError,
        'formName':formName,
        'escalationData':escalationData,
        'client':client,
        'topUpDocket': topUpDocket
    }
    return render(request,'Account/topUpForm.html',params)

def topUpSolve(request):
    errorId  = request.GET.get('topUpId')
    remark  = request.GET.get('remark')
    dockets = request.GET.getlist('dockets[]')
    for docket in dockets:
        getDocket = Escalation.objects.filter(pk = docket).first()
        getDocket.escalationStep = 4
        getDocket.remark = remark
        getDocket.errorId = errorId
        getDocket.save()
    rctiError = RctiErrors.objects.filter(pk=errorId).first()
    rctiError.status = True
    rctiError.save()
        
    return JsonResponse({'status': True})
    
def report(request):
    reportError = PastTripError.objects.filter(status = False , errorType = 1).values()
    reportErrorSolved = PastTripError.objects.filter(status = True , errorType = 1).values()
    str_ = '45'
    params ={
            'str_':str_,
            'reportError' : reportError,
            'reportErrorSolved' :reportErrorSolved,
        }  
    # return HttpResponse(params['str_'])
    return render(request,'Account/report.html',params)

@csrf_protect
def reportSave(request):
    primaryFile = request.FILES.get('primaryFile')
    secondaryFile = request.FILES.get('secondaryFile')

    if primaryFile:
        time = getCurrentTimeInString()
        primaryFileName = time + "@_!" + (str(primaryFile.name)).replace(' ','')
        location = f'static/Account/RCTI/Report'
        lfs = FileSystemStorage(location=location)
        lfs.save(primaryFileName, primaryFile)
    if secondaryFile:
        time = getCurrentTimeInString()
        secondaryFileName = time + "@_!" + (str(secondaryFile.name)).replace(' ','')
        location = f'static/Account/RCTI/Report'
        lfs = FileSystemStorage(location=location)
        lfs.save(secondaryFileName, secondaryFile)
        
    with open("File_name_file.txt",'w+',encoding='utf-8') as f:
        f.write(f'{primaryFileName}<>{secondaryFileName}')
        f.close()
    colorama.AnsiToWin32.stream = None
    os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
    cmd = ["python", "manage.py", "runscript", 'holcim','--continue-on-error']
    subprocess.Popen(cmd, stdout=subprocess.PIPE)
    messages.success(request,'Successfully save')
    return redirect(request.META.get('HTTP_REFERER'))

def EscalationTable(request):
    escalationObj  = Escalation.objects.filter(Q(escalationStep = 1) | Q( escalationStep = 2) |Q(escalationStep = 3))
    completeEscalationObj  = Escalation.objects.filter(escalationStep = 4)
    params ={
        'escalationObj':escalationObj,
        'completeEscalationObj':completeEscalationObj,
    }
    return render(request,'Account/Tables/escalationTable.html' , params)
def EscalationForm(request ,id = None):
    escalationDocketObj = None
    escalationObj  = None
    clientNames = Client.objects.all()
    if id:
        escalationObj = Escalation.objects.filter(pk = id).first()
        escalationDocketObj = EscalationDocket.objects.filter(pk=id).first()
        escalationDocketObj.docketDate = dateConverterFromTableToPageFormate(escalationDocketObj.docketDate)


    params ={
        'escalationObj':escalationObj,
        'clientNames':clientNames,
        'escalationDocketObj':escalationDocketObj
    }
    return render(request , 'Account/manuallyEscalationForm1.html' , params)

@csrf_protect
def manuallyEscalationForm1Save(request):
    docketNumber = request.POST.get('docketNumber')
    docketDate = request.POST.get('docketDate')
    invoiceFile = request.FILES.get('invoiceFile')
    clientNameId = request.POST.get('clientName')
    escalationAmount = request.POST.get('escalationAmount')
    escalationType = request.POST.get('escalation')
    escalationDocketObj = EscalationDocket.objects.filter(docketNumber = docketNumber , docketDate= docketDate).first()
    if escalationDocketObj:
        escalationObj = Escalation.objects.filter(pk = escalationDocketObj.escalationId.id).first()
        return redirect('Account:showReconciliationEscalation2',escalationObj.id)
    
    currentDate = getCurrentDateTimeObj().date()
    clientObj = Client.objects.filter(clientId=clientNameId).first()
    
    escalationObj = Escalation()
    
    escalationObj.userId = request.user
    escalationObj.escalationDate = currentDate
    escalationObj.clientName = clientObj
    escalationObj.escalationStep = 1
    escalationObj.escalationAmount = escalationAmount
    escalationObj.escalationType = escalationType
    escalationObj.save()
    escalationDocketObj = EscalationDocket()

    escalationDocketObj.docketNumber = docketNumber
    escalationDocketObj.docketDate = docketDate
    escalationDocketObj.amount = escalationAmount
    escalationDocketObj.escalationId = escalationObj
    if invoiceFile:
        time = getCurrentTimeInString()
        attachmentPath = 'static/Account/manuallyEscalation/'
        fileName = invoiceFile.name
        convertedFileName = time + '!_@' + fileName
        pfs = FileSystemStorage(location=attachmentPath)
        try:
            pfs.save(convertedFileName, invoiceFile)
        except Exception as e:
            messages.error(request, "FileName Not Valid.")
            return redirect(request.META.get('HTTP_REFERER'))
            
        escalationDocketObj.invoiceFile = f'static/Account/manuallyEscalation/{convertedFileName}'
        escalationDocketObj.save()

    messages.success(request, "Escalation Entry Successfully.")
    return redirect('Account:showReconciliationEscalation2', escalationObj.id)
    

def ViewBulkEscalationData(request,escalationId):
    escalationObj = Escalation.objects.filter(pk=escalationId).first()
    escalationObj.escalationDate = dateConverterFromTableToPageFormate(escalationObj.escalationDate)
    
    escalationDocketObj = list(EscalationDocket.objects.filter(escalationId=escalationId).values())
    oldMail = EscalationMail.objects.filter(escalationId=escalationObj)

    manuallyEscalationDocketObj = None
    reconciliationDockets = []
    for i in escalationDocketObj:
        
        obj = ReconciliationReport.objects.filter(docketNumber = i['docketNumber'], docketDate= i['docketDate']).first()
        if obj != None:
            obj.docketDate = dateConverterFromTableToPageFormate(obj.docketDate)
            reconciliationDockets.append(obj)
        else:
            manuallyEscalationDocketObj = EscalationDocket.objects.filter(escalationId=escalationId).first()
            manuallyEscalationDocketObj.docketDate = dateConverterFromTableToPageFormate(manuallyEscalationDocketObj.docketDate)
            
            
    # return HttpResponse(manuallyEscalationDocketObj)
    params = {
        'reconciliationDockets' : reconciliationDockets,
        'escalationObj':escalationObj,
        'oldMail' : oldMail,
        'clientNames' : Client.objects.all(),
        'manuallyEscalationDocketObj':manuallyEscalationDocketObj
        

    }
    return render(request,'Account/EscalationView.html',params)
