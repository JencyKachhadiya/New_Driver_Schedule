from django.db import models
from django.utils import timezone
from GearBox_app.models import *
from django.contrib.auth.models import User



# -----------------------------------
# Plants section
# -----------------------------------

class BasePlant(models.Model):
    basePlant = models.CharField(unique= True,max_length=200)
    address = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=20, default='')
    personOnName = models.CharField(max_length=25, default='')
    managerName = models.CharField(max_length=25, default='')
    lat = models.CharField(max_length=20, default='')
    long = models.CharField(max_length=20, default='')
    
    #if not any select that means plant name is location
    clientDepot = models.BooleanField(default=False) 
    clientBasePlant = models.BooleanField(default=False) 
    depotCode = models.CharField(max_length=100, null=True , default='')
    email = models.CharField(max_length=100, null=True , default='')
    clientOfficeId = models.ForeignKey(ClientOffice, null=True, on_delete=models.CASCADE)
    history = HistoricalRecords()
    
    class Meta:
        unique_together = (('lat', 'long'),)

    def __str__(self) -> str:
        return str(self.basePlant)
    
# -----------------------------------
# Location 
# -----------------------------------

# class Location(models.Model):
#     location = models.CharField(max_length=200)
#     address = models.CharField(max_length=255, default='')
#     phone = models.CharField(max_length=20, default='')
#     personOnName = models.CharField(max_length=25, default='')
#     managerName = models.CharField(max_length=25, default='')
#     lat = models.CharField(max_length=20, default='')
#     long = models.CharField(max_length=20, default='')

#     class Meta:
#         unique_together = (('lat', 'long'),)

#     def __str__(self) -> str:
#         return str(self.location)

# -----------------------------------
# New Trips Section start
# -----------------------------------


class DriverShift(models.Model):
    verified = models.BooleanField(default=False)
    verifiedBy = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    shiftType = models.CharField(max_length=200,choices=(('Day','Day'),('Night','Night')),default = 'Day')
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    shiftDate = models.DateField(null=True, blank=True)
    startDateTime = models.DateTimeField(null=True, blank=True)
    endDateTime = models.DateTimeField(null=True, blank=True)
    driverId = models.IntegerField(null=True, blank=True)
    locationImg = models.FileField(upload_to='static/Account/driverLocationFiles', null=True)
    startTimeUTC = models.DateTimeField(null=True)
    endTimeUTC = models.DateTimeField(null=True)
    archive = models.BooleanField(default=False)
    lastEmailTime = models.DateTimeField(null=True)
    # end shift before trips start
    endShiftImg = models.FileField(upload_to='static/img/shiftImg', null=True)
    comment = models.CharField(max_length=2048, null=True) 
    endLatitude = models.CharField(max_length=20, null=True, blank=True)
    endLongitude = models.CharField(max_length=20, null=True, blank=True)
    endLocationImg = models.FileField(upload_to='static/Account/driverLocationFiles', null=True)
    totalRunTime = models.FloatField(default=0)
    totalBreakInMinute = models.FloatField(default=0)
    chargeJobEditReason = models.CharField(max_length=2048, null=True, blank=True)
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return str(self.shiftDate) + '-' + str(self.id)
    

class DriverShiftTrip(models.Model):
    verified = models.BooleanField(default=False)
    shiftId = models.IntegerField(null=True, blank=True)
    startDateTime = models.DateTimeField(null=True, blank=True)
    endDateTime = models.DateTimeField(null=True, blank=True)
    clientId = models.IntegerField(null=True, blank=True)
    truckConnectionId = models.IntegerField(null=True, blank=True)
    dispute = models.BooleanField(default = False)
    numberOfLoads = models.FloatField(default=0)
    basePlant = models.PositiveIntegerField(default=0)
    revenueDeficit = models.FloatField(default=0)
    loadSheet = models.FileField(upload_to='static/img/finalloadSheet',null=True, blank=True)
    comment = models.CharField(max_length=200, default='None')
    startTimeUTC = models.DateTimeField(null=True)
    endTimeUTC = models.DateTimeField(null=True)
    archive = models.BooleanField(default=False)
    startOdometerKms = models.FloatField(default=0, null=True)
    endOdometerKms = models.FloatField(default=0, null=True)
    startEngineHours = models.FloatField(default=0, null=True)
    endEngineHours = models.FloatField(default=0, null=True)
    lastEmailTime = models.DateTimeField(null=True)

    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return str(self.clientId) + str(self.startDateTime) + str(self.endDateTime) 
    
    
class DriverShiftDocket(models.Model):
    tripId = models.PositiveIntegerField(null=True, blank=True)
    shiftId = models.IntegerField(null=True, blank=True)
    shiftDate = models.DateField(null=True, blank=True)
    clientId = models.IntegerField(null=True, blank=True)
    truckConnectionId = models.IntegerField(null=True, blank=True)
    docketNumber = models.CharField(max_length=20, default='', null=True, blank=True)
    docketFile = models.FileField(upload_to='static/img/docketFiles', null=True, blank=True)
    basePlant = models.PositiveIntegerField(null=True, blank=True)
    noOfKm = models.FloatField(default=0)
    transferKM = models.FloatField(default=0)
    returnToYard = models.BooleanField(default=False)
    tippingToYard = models.BooleanField(default=False)
    returnQty = models.FloatField(default=0)
    returnKm = models.FloatField(default=0)
    waitingTimeStart = models.TimeField(default=None, null=True, blank=True)
    waitingTimeEnd = models.TimeField(default=None, null=True, blank=True)
    totalWaitingInMinute = models.FloatField(default=0)
    surchargeType = models.IntegerField(null=True, blank=True)
    surcharge_duration = models.FloatField(default=0)
    cubicMl = models.FloatField(default=0)
    standByStartTime = models.TimeField(default=None, null=True, blank=True)
    standByEndTime = models.TimeField(default=None, null=True, blank=True)
    standBySlot = models.PositiveIntegerField(default=0, null=True)
    blowBack = models.CharField(max_length=2048, default='', null=True)
    callOut = models.CharField(max_length=2048, default='', null=True)
    minimumLoad = models.FloatField(default=0)
    others = models.FloatField(default=0)
    comment = models.CharField(max_length=255, null=True, default='')
    archive = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self) -> str:
        return str(self.docketNumber) + str(self.tripId)
   
    class Meta:
        unique_together = (('docketNumber', 'shiftDate','clientId','truckConnectionId'))
# -----------------------------------
# New Trips Section end
# -----------------------------------



# -----------------------------------
# Breaks end
# -----------------------------------

class DriverBreak(models.Model):
    shiftId = models.ForeignKey(DriverShift, on_delete=models.CASCADE, default=None)
    tripId = models.ForeignKey(DriverShiftTrip, on_delete=models.CASCADE, default=None, null=True)
    # tripId = models.ForeignKey(DriverShiftTrip, on_delete=models.CASCADE, default=None)
    driverId = models.ForeignKey(Driver, on_delete=models.CASCADE, default=None)  
    startDateTime = models.DateTimeField(null=True)
    endDateTime = models.DateTimeField(null=True)
    breakFile = models.FileField(upload_to='static/img/breakFiles', null=True)
    durationInMinutes = models.FloatField(default=0, null=True) 
    location = models.CharField(max_length=2048, default='', null=True)
    description = models.CharField(max_length=2048, default='', null=True)
    nextBreakStartTime = models.DateTimeField( null=True )



    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return str(self.driverId.name)
    
    def save(self, *args, **kwargs):
        if self.startDateTime and self.endDateTime:
            duration = (self.endDateTime - self.startDateTime).total_seconds() / 60
            self.durationInMinutes = max(duration, 0) 
        else:
            self.durationInMinutes = 0  
        super().save(*args, **kwargs)


class DriverReimbursement(models.Model):
    shiftId = models.ForeignKey(DriverShift, on_delete=models.CASCADE, default=None, null=True)
    driverId = models.ForeignKey(Driver, on_delete=models.CASCADE, default=None, null=True)
    raiseDate = models.DateTimeField(default=None, null=True, blank=True)
    # driver notes
    notes = models.CharField(max_length=2048, default='', null=True, blank=True)
    # staff notes 
    comments = models.CharField(max_length=2048, default='', null=True, blank=True)

    amount = models.FloatField(default=0)
    reimbursementFile = models.FileField(upload_to='static/img/reimbursementFiles', null=True, blank=True)
    # 0:Pending, 1:Accepted, 2:Denied, 3:Partial
    status = models.PositiveBigIntegerField(default=0)
    actualAmount = models.PositiveBigIntegerField(default=0)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return str(self.shiftId.id) + '-' + str(self.driverId.driverId)
    

# -----------------------------------
# Breaks end
# -----------------------------------
 
    
    

# -----------------------------------
# Trips section
# -----------------------------------

class DriverTrip(models.Model):
    verified = models.BooleanField(default=False)
    partially = models.BooleanField(default=False)
    driverId = models.ForeignKey(Driver, on_delete=models.CASCADE)
    clientName = models.ForeignKey(Client,on_delete=models.CASCADE)
    shiftType = models.CharField(max_length=200,choices=(('Day','Day'),('Night','Night')))
    numberOfLoads = models.FloatField(default=0)
    truckNo = models.IntegerField()
    shiftDate = models.DateField(null=True, default=None)
    startTime = models.CharField(max_length=200)
    endTime = models.CharField(max_length=200)
    dispute = models.BooleanField(default = False)
    loadSheet = models.FileField(upload_to='static/img/finalloadSheet',null=True, blank=True)
    comment = models.CharField(max_length=200, default='None')
    comment2 = models.CharField(max_length=200, default='None')

    def __str__(self) -> str:
        return str(self.id)


class DriverDocket(models.Model):
    docketId = models.AutoField(primary_key=True)
    shiftDate = models.DateField(null=True, default=timezone.now())
    tripId = models.ForeignKey(DriverTrip, on_delete=models.CASCADE)
    docketNumber = models.IntegerField()
    docketFile = models.FileField(upload_to='static/img/docketFiles')
    basePlant = models.ForeignKey(BasePlant,on_delete=models.CASCADE)
    noOfKm = models.FloatField(default=0)
    transferKM = models.FloatField(default=0)
    returnToYard = models.BooleanField(default=False)
    tippingToYard = models.BooleanField(default=False)
    returnQty = models.FloatField(default=0)
    returnKm = models.FloatField(default=0)
    waitingTimeStart = models.CharField(max_length=200)
    waitingTimeEnd = models.CharField(max_length=200)
    totalWaitingInMinute = models.FloatField(default=0)
    surcharge_type = models.ForeignKey(Surcharge, on_delete=models.CASCADE)
    surcharge_duration = models.FloatField(default=0)
    cubicMl = models.FloatField(default=0)
    standByStartTime = models.CharField(max_length=200)
    standByEndTime = models.CharField(max_length=200)
    standBySlot = models.PositiveIntegerField(default=0, null=True)
    minimumLoad = models.FloatField(default=0)
    others = models.FloatField(default=0)
    comment = models.CharField(max_length=255, null=True, default='None')
    
    # Holcim 
    # jobNo = models.FloatField(default=0)
    # orderNo = models.FloatField(default=0)
    # status = models.CharField(max_length=200)
    # ticketedDate = models.DateField(null=True, default=None)
    # ticketedTime = models.TimeField(null=True, blank=True)
    # load = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    # loadComplete = models.CharField(max_length=200)
    # toJob = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    # timeToDepart = models.FloatField(default=0)
    # onJob = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    # timeToSite = models.FloatField(default=0)
    # beginUnload = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    # waitingTime = models.FloatField(default=0)
    # endPour = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    # wash = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    # toPlant = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    # timeOnSite = models.FloatField(default=0)
    # atPlant = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    # leadDistance = models.FloatField(default=0)
    # returnDistance = models.FloatField(default=0)
    # totalDistance = models.FloatField(default=0)
    # totalTime = models.FloatField(default=0)
    # waitTimeBetweenJob = models.FloatField(default=0)
    # driverName = models.ForeignKey(Driver, on_delete=models.CASCADE)
    # quantity = models.FloatField(default=0)
    # slump = models.FloatField(default=0)
    # waterAdded = models.FloatField(max_length=200)
    
    
    def __str__(self) -> str:
        return str(self.docketNumber)

    class Meta:
        unique_together = (('docketNumber', 'shiftDate','tripId'),)

class RctiReport(models.Model):
    reportDate = models.DateField()
    gstPayable = models.FloatField(default=0)
    clientName = models.ForeignKey(Client,on_delete=models.CASCADE ,default = None)
    totalExGST = models.FloatField(default=0)
    total = models.FloatField(default=0)
    fileName = models.CharField(max_length=255 , default='')
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        unique_together = (('reportDate', 'total','fileName'))

class RctiAdjustment(models.Model):
    truckNo = models.FloatField(default=0)
    docketNumber = models.CharField(max_length=10,default='', null=True)
    docketDate = models.DateField()
    docketYard = models.CharField(default='', max_length=255, null=True)
    clientName = models.ForeignKey(Client,on_delete=models.CASCADE)
    rctiReport = models.ForeignKey(RctiReport,on_delete=models.CASCADE , default =None)
    description = models.CharField(max_length=255,default='', null=True)
    noOfKm = models.FloatField(default=0)
    invoiceQuantity = models.FloatField(default=0)
    unit = models.CharField(max_length=10,default='',null=True)
    unitPrice= models.FloatField(default=0)
    totalExGST = models.FloatField(default=0)
    GSTPayable = models.FloatField(default=0)
    Total = models.FloatField(default=0)    
    # loadAndKmCost = models.FloatField(default=0)
    surchargeCost = models.FloatField(default=0)
    waitingTimeCost = models.FloatField(default=0)
    transferKmCost = models.FloatField(default=0)
    returnKmCost = models.FloatField(default=0)
    otherCost = models.FloatField(default=0)
    standByCost = models.FloatField(default=0)
    loadDeficit = models.FloatField(default=0)
    blowBack = models.FloatField(default=0)
    callOut = models.FloatField(default=0)
    cancellationCost = models.FloatField(default=0)
    demurageCost = models.FloatField(default=0)
    history = HistoricalRecords()

    
    def __str__(self) -> str:
        return str(self.docketNumber)
    
    # class Meta:
    #     unique_together = (('docketNumber', 'docketDate','rctiReport','truckNo'))
    
class RCTI(models.Model):
    
    UNIT_CHOICES = (
        ('minute','MINUTE'),
        ('slot','SLOT'),
    )

    # ClientTruck id
    truckNo = models.FloatField(default=0)
    docketNumber = models.CharField(max_length=10,default='')
    docketDate = models.DateField()
    docketYard = models.CharField(default='', max_length=255)
    clientName = models.ForeignKey(Client,on_delete=models.CASCADE)
    rctiReport = models.ForeignKey(RctiReport,on_delete=models.CASCADE , default =None)
    noOfKm = models.FloatField(default=0)
    
    cubicMl = models.FloatField(default=0)
    cubicMiAndKmsCost= models.FloatField(default=0)
    destination = models.CharField(max_length=255, default='Not given')
    cartageGSTPayable = models.FloatField(default=0)
    cartageTotalExGST = models.FloatField(default=0)
    cartageTotal = models.FloatField(default=0)
    
    # Holcim 
    unit = models.CharField(default='', max_length=10)
    paidQty = models.FloatField(default=0)
    
    
    transferKM = models.FloatField(default=0)
    transferKMCost = models.FloatField(default=0)
    transferKMGSTPayable = models.FloatField(default=0)
    transferKMTotalExGST = models.FloatField(default=0)
    transferKMTotal = models.FloatField(default=0)
    
    returnKm = models.FloatField(default=0)
    returnPerKmPerCubicMeterCost = models.FloatField(default=0)
    returnKmGSTPayable = models.FloatField(default=0)
    returnKmTotalExGST = models.FloatField(default=0)
    returnKmTotal = models.FloatField(default=0)
    
    waitingTimeSCHED = models.FloatField(default=0)
    waitingTimeSCHEDCost = models.FloatField(default=0)
    waitingTimeSCHEDGSTPayable = models.FloatField(default=0)
    waitingTimeSCHEDTotalExGST = models.FloatField(default=0)
    waitingTimeSCHEDTotal = models.FloatField(default=0)
    
    waitingTimeInMinutes = models.FloatField(default=0)
    waitingTimeCost = models.FloatField(default=0)
    waitingTimeGSTPayable = models.FloatField(default=0)
    waitingTimeTotalExGST = models.FloatField(default=0)
    waitingTimeTotal = models.FloatField(default=0)
    
    standByNoSlot = models.FloatField(default=0)
    standByPerHalfHourDuration = models.FloatField(default=0)
    standByUnit = models.CharField(choices=UNIT_CHOICES,default="minute",max_length=20)
    standByGSTPayable = models.FloatField(default=0)
    standByTotalExGST = models.FloatField(default=0)
    standByTotal = models.FloatField(default=0)
    
    minimumLoad = models.FloatField(default=0)
    loadCost = models.FloatField(default=0)
    minimumLoadGSTPayable = models.FloatField(default=0)
    minimumLoadTotalExGST = models.FloatField(default=0)
    minimumLoadTotal = models.FloatField(default=0)

    # Holcim 
    blowBack= models.FloatField(default=0)
    blowBackCost = models.FloatField(default=0)
    blowBackGSTPayable = models.FloatField(default=0)
    blowBackTotalExGST = models.FloatField(default=0)
    blowBackTotal = models.FloatField(default=0)
    
    callOut= models.FloatField(default=0)
    callOutCost = models.FloatField(default=0)
    callOutGSTPayable = models.FloatField(default=0)
    callOutTotalExGST = models.FloatField(default=0)
    callOutTotal = models.FloatField(default=0)

    surcharge = models.FloatField(default=0)
    surchargeCost = models.FloatField(default=0)
    surchargeGSTPayable = models.FloatField(default=0)
    surchargeTotalExGST = models.FloatField(default=0)
    surchargeTotal = models.FloatField(default=0)
   
    otherDescription = models.CharField(max_length=500,default= '', null= True , blank=True)
    others = models.FloatField(default=0)
    othersCost = models.FloatField(default=0)
    othersGSTPayable = models.FloatField(default=0)
    othersTotalExGST = models.FloatField(default=0)
    othersTotal = models.FloatField(default=0)
    history = HistoricalRecords()
    
    def _str_(self) -> str:
        return str(self.docketNumber) + str(self.truckNo)

    
# -----------------------------------
# Holiday section
# -----------------------------------

class PublicHoliday(models.Model):
    date = models.DateField()
    stateName = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return str(self.description)
    
    
# -----------------------------------
# Past trip errors model
# -----------------------------------

class PastTripError(models.Model):
    clientName = models.CharField(max_length=25 ,default=None ,blank=True,null=True)
    tripDate = models.CharField(max_length=255, default=None, null=True, blank=True) 
    truckNo = models.IntegerField(default=0) 
    docketNumber = models.CharField(max_length=255, default=None, null=True, blank=True)
    lineNumber =  models.CharField(max_length=255, default=None, null=True, blank=True)   
    errorFromPastTrip = models.CharField(max_length=255, default=None, null=True, blank=True)
    exceptionText = models.CharField(max_length=255, default=None, null=True, blank=True)
    fileName = models.CharField(max_length=255, default=None, null=True, blank=True)
    status = models.BooleanField(default=False)
    # 0 : pastTrip error  1: Report Error  2: pastTrip archive
    errorType = models.FloatField(default=0) 
    data = models.CharField(max_length=2048, default=' ')
    history = HistoricalRecords()

    def __str__(self):
        return str(self.docketNumber)
    
    
# -----------------------------------
# Reconciliation model
# -----------------------------------
    
class ReconciliationReport(models.Model):
    docketNumber = models.CharField(max_length=10, default='')
    docketDate = models.DateField(default=None, null= True, blank=True)
    # clientName =  models.CharField(max_length=20,default='')
    driverId = models.PositiveIntegerField(default=0)
    clientId = models.PositiveIntegerField(default=0)
    truckConnectionId = models.PositiveIntegerField(default=0)
    
    # 0:reconciliation, 1:Short Paid, 2: Top up solved, 3: write-of, 4(3):internal,  5(1):External,  7: revenue
    reconciliationType = models.PositiveIntegerField(default=0)
    missingComponent = models.CharField(max_length=255, default=None, null=True, blank=True)
    
    # escalationType = models.CharField(max_length=20,default='')
    # # 0:not escalate, 1:1st step, 2:2nd step, 3:3rd step, 4:escalation complete
    # escalationStep = models.PositiveIntegerField(default=0)
    # escalationAmount = models.PositiveIntegerField(default=0)
    # errorId = models.PositiveIntegerField(default=None)

    fromDriver = models.BooleanField(default=False)
    fromRcti = models.BooleanField(default=False)
    
    # loadKmcost 
    driverLoadAndKmCost = models.FloatField(default=0)
    rctiLoadAndKmCost = models.FloatField(default=0)
    
    # SurchargeCost
    driverSurchargeCost = models.FloatField(default=0)
    rctiSurchargeCost = models.FloatField(default=0)

    # WaitingTimeCost 
    driverWaitingTimeCost = models.FloatField(default=0)
    rctiWaitingTimeCost = models.FloatField(default=0)

    # TransferCost
    driverTransferKmCost = models.FloatField(default=0)
    rctiTransferKmCost = models.FloatField(default=0)
    
    # returnKmCost
    driverReturnKmCost = models.FloatField(default=0)
    rctiReturnKmCost = models.FloatField(default=0)
    
    # otherCost 
    driverOtherCost = models.FloatField(default=0)
    rctiOtherCost = models.FloatField(default=0)    
    
    # standByCost 
    driverStandByCost = models.FloatField(default=0)
    rctiStandByCost = models.FloatField(default=0)
    
    # minimum load
    driverLoadDeficit = models.FloatField(default=0)
    rctiLoadDeficit = models.FloatField(default=0)
    
    # Blow Back
    driverBlowBack = models.FloatField(default=0)
    rctiBlowBack = models.FloatField(default=0)
    
    # Call Out
    driverCallOut = models.FloatField(default=0)
    rctiCallOut = models.FloatField(default=0)
    
    # cancellation 
    driverCancellationCost = models.FloatField(default=0)
    rctiCancellatioCost = models.FloatField(default=0)

    # demurage 
    driverDemurageCost = models.FloatField(default=0)
    rctiDemurageCost = models.FloatField(default=0)

    # Total 
    driverTotalCost = models.FloatField(default=0)
    rctiTotalCost = models.FloatField(default=0)
    history = HistoricalRecords()
        
    def __str__(self):
        return str(self.docketNumber)
    

# -----------------------------------
# Escalation Mail section
# -----------------------------------
class Escalation(models.Model):   
    userId = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    escalationDate = models.DateField(default=None, null=True)
    escalationType = models.CharField(max_length=20 , default='')
    remark = models.CharField(max_length=1024, default='')
    clientName = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    
    # 1:1st step, 2:2nd step, 3:3rd step, 4:4th step, 5:complete
    escalationStep = models.PositiveIntegerField(default=1)
   
    escalationAmount = models.FloatField(default=0)
    errorId = models.PositiveIntegerField(default=None, null=True)
    history = HistoricalRecords()
    
    
    def __str__(self) -> str:
        return str(self.id) + ' ' + str(self.escalationType)
    
class EscalationDocket(models.Model):
    docketNumber = models.CharField(max_length=10, default=None)
    docketDate = models.DateField(default=None, null=True)
    escalationId = models.ForeignKey(Escalation, on_delete=models.CASCADE, default=None)
    amount = models.FloatField(default=0)
    remark = models.CharField(max_length=1024, default='')
    invoiceFile = models.FileField(upload_to='static/Account/manuallyEscalation', null=True, blank=True)
    
    
    truckNo = models.ForeignKey(ClientTruckConnection, on_delete=models.CASCADE, default=None)

    callOut = models.BooleanField(default=False)
    callOutCharge = models.FloatField(default=0, null=True, blank=True)
    
    demurrage = models.BooleanField(default=False)
    demurrageCharge = models.FloatField(default=0, null=True, blank=True)
    
    cancellation = models.BooleanField(default=False)
    cancellationCharge = models.FloatField(default=0, null=True, blank=True)
    
    transferKm = models.BooleanField(default=False)
    transferKmCharge = models.FloatField(default=0, null=True, blank=True)
    
    waitingTime = models.BooleanField(default=False)
    waitingTimeCharge = models.FloatField(default=0, null=True, blank=True)
    
    standBy = models.BooleanField(default=False)
    standByCharge = models.FloatField(default=0, null=True, blank=True)
    
    returnKm = models.BooleanField(default=False)
    returnKmCharge = models.FloatField(default=0, null=True, blank=True)
    
    # ------------------
    surcharge = models.BooleanField(default=False)
    surchargeCharge = models.FloatField(default=0, null=True, blank=True)
    
    loadKm = models.BooleanField(default=False)
    loadKmCharge = models.FloatField(default=0, null=True, blank=True)
    
    blowBack = models.BooleanField(default=False)
    blowBackCharge = models.FloatField(default=0, null=True, blank=True)
    # ------------------
        
    custom = models.BooleanField(default=False)
    customCharge = models.FloatField(default=0, null=True, blank=True)
    history = HistoricalRecords()
    
    
    def save(self, *args, **kwargs):
        # Calculate the total amount based on charges
        total_charge = sum([
            self.callOutCharge,
            self.demurrageCharge,
            self.cancellationCharge,
            self.transferKmCharge,
            self.waitingTimeCharge,
            self.standByCharge,
            self.returnKmCharge,
            self.customCharge,
            self.surchargeCharge,
            self.loadKmCharge,
            self.blowBackCharge,
        ])

        # Update the Total amount field
        self.amount = total_charge

        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return str(self.docketNumber) + ' ' + str(self.docketDate)

    
class EscalationMail(models.Model):
    mailType = [('Send', 'Send'),('Receive', 'Receive'),]
    
    escalationId = models.ForeignKey(Escalation, on_delete=models.CASCADE, default=None)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    mailTo = models.CharField(default=None, max_length=50)
    mailFrom = models.CharField(default=None, max_length=50)
    mailSubject = models.CharField(default=None, max_length=255)
    mailDescription = models.CharField(default=None, max_length=1024)    
    mailAttachment = models.FileField(upload_to='static/img/mailAttachment', null=True, blank=True)    
    mailType = models.CharField(max_length=20, choices=mailType, default='Send')
    mailDate = models.DateField(default=None, null=True)
    mailCount = models.PositiveBigIntegerField(default=1)
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return str(self.escalationId) + ' ' + str(self.mailDate)
    
    
# -----------------------------------
# Rcti Error section
# -----------------------------------
class RctiErrors(models.Model):
    clientName = models.CharField(max_length=25 ,default=None ,blank=True,null=True)
    docketNumber = models.CharField(default=None ,blank=True,null=True ,max_length=255)
    docketDate = models.CharField(default=None, blank=True,null=True, max_length=255)
    truckNo = models.CharField(default=None, blank=True,null=True, max_length=255)
    exceptionText = models.CharField(default=None, blank=True,null=True, max_length=255)
    errorDescription = models.CharField(default=None ,blank=True,null=True ,max_length=255)
    fileName =  models.CharField(default=None ,blank=True,null=True ,max_length=255)
    status = models.BooleanField(default=False)
    data = models.CharField(max_length=2048,default='')
    # 0:Earning, 1 : earning top up manually managed error
    errorType = models.PositiveIntegerField(default=0)
    history = HistoricalRecords()
    
    def __str__(self) -> str:
        return str(self.docketNumber) +' '+ str(self.errorDescription)

# -----------------------------------
# Rcti Expense section
# -----------------------------------
class RctiExpense(models.Model):
    clientName = models.ForeignKey(Client,on_delete=models.CASCADE ,default = None)
    truckNo = models.CharField(max_length=10, default='')
    docketNumber = models.CharField( max_length=10,default='')
    docketDate = models.DateField()
    docketYard = models.CharField(default='', max_length=255)
    description = models.CharField(max_length=255)
    paidKm = models.FloatField(default=0)
    invoiceQuantity = models.FloatField(default=0)
    unit = models.CharField(max_length=100 , default= '')
    unitPrice = models.FloatField(default=0)
    gstPayable = models.FloatField(default=0)
    totalExGST = models.FloatField(default=0)
    total = models.FloatField(default=0)
    history = HistoricalRecords()
    
    def __str__(self):
        return str(self.docketNumber)
    
# model rename  holcimTripReport
class HolcimTrip(models.Model):
    truckNo = models.PositiveBigIntegerField(default=0)
    shiftDate = models.DateField(null=True, default=None)
    numberOfLoads = models.FloatField(default=0)
    history = HistoricalRecords()
    
    def __str__(self):
        return str(self.id)
    
# model rename  holcimDocketReport
class HolcimDocket(models.Model):
    # secondary File 
    truckNo =  models.FloatField(default=0)
    tripId = models.ForeignKey(HolcimTrip, on_delete=models.CASCADE)
    jobNo = models.FloatField(default=0)
    orderNo = models.FloatField(default=0)
    # status = models.CharField(max_length=200)
    ticketed = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    load = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    loadComplete = models.CharField(max_length=200)
    toJob = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    timeToDepart = models.FloatField(default=0)
    onJob = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    timeToSite = models.FloatField(default=0)
    beginUnload = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    waitingTime = models.FloatField(default=0)
    endPour = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    wash = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    toPlant = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    timeOnSite = models.FloatField(default=0)
    atPlant = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    leadDistance = models.FloatField(default=0)
    returnDistance = models.FloatField(default=0)
    totalDistance = models.FloatField(default=0)
    totalTime = models.FloatField(default=0)
    waitTimeBetweenJob = models.FloatField(default=0)
    driverName = models.ForeignKey(Driver, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    slump = models.FloatField(default=0)
    waterAdded = models.FloatField(default=0)
    
    
    # primary File 
    docketDate = models.DateField(null=True, default=None)
    materialCode = models.CharField(max_length= 100 , default=None, null= True, blank=True)
    basePlant = models.ForeignKey(BasePlant, on_delete=models.CASCADE , default=None)
    customerName = models.CharField(max_length= 255 , default=None, null= True, blank=True)
    address = models.CharField(max_length= 255 , default=None, null= True, blank=True)
    loadSize = models.FloatField(default =0)
    timeOnSite = models.FloatField(default=0)
    distanceInKm = models.FloatField(default=0)
    requestedKm = models.FloatField(default=0)
    reasonRequested = models.CharField(max_length= 255 , default=None, null= True, blank=True)
    returnedQty = models.FloatField(default=0)
    dischargeLocation = models.CharField(max_length= 255 , default=None, null= True, blank=True)
    additionalKm = models.CharField(max_length= 255 , default=None, null= True, blank=True)
    status = models.CharField(max_length= 255 , default=None, null= True, blank=True)
    history = HistoricalRecords()
    
    
    def __str__(self):
        return str(self.jobNo)
    
    class Meta:
        unique_together = (('jobNo', 'docketDate','tripId'))