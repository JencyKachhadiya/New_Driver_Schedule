"""
URL configuration for Driver_Schedule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from . import views

app_name = 'Account'

urlpatterns = [
    path('', views.index, name='index'),
    
    # Driver trip path start
    path('Form1/', views.getForm1, name='getForm1'),
    path('Form2/', views.getForm2, name='getForm2'),
    path('existing/Form2/<int:id>/', views.getForm2, name='existingForm2'),
    
    path('createFormSession/',views.createFormSession, name='createFormSession'),
    path('formsSave/', views.formsSave, name='formsSave'),
    
    path('jobs/assigned/', views.assignedJobShow, name='assignedJobShow'),
    path('jobs/assigned/accept/<int:id>/', views.assignedJobAccept, name='assignedJobAccept'),
    path('jobs/view/<int:id>/', views.singleJobView, name='singleJobView'),

    # path('jobs/open/', views.openJobShow, name='openJobShow'),
    path('jobs/finish/<int:id>/', views.finishJob, name='finishJob'),

    path('holcim/data/get/<int:id>/', views.getHolcimDataView, name='getHolcimTripDataView'),
    path('holcim/data/save/<int:id>/', views.getHolcimDataSave, name='getHolcimTripDataSave'),
    
    path('docket/upload/<int:id>/', views.uploadDocketView, name='uploadDocketView'),
    path('docket/save/<int:id>/', views.uploadDocketSave, name='uploadDocketSave'),
    
    
    path('timeOfStart/view/', views.timeOfStart, name='timeOfStart'),
    path('timeOfStart/save/', views.timeOfStartSave, name='timeOfStartSave'),
    
    
    path('driver/show-profile/', views.driverProfileView, name='driverProfileView'),


    path('mapForm/view/', views.mapFormView, name='mapFormView'),
    path('mapForm/view/<str:startDate>', views.mapFormView, name='mapFormViewWithDate'),
    path('mapForm/save/', views.mapDataSave, name='mapDataSave'),
    path('recurring/trip/<int:recurring>/', views.mapDataSave, name='recurringTrip'),
    
    path('clientAndTruck/save/<int:id>/', views.clientAndTruckDataSave, name='clientAndTruckDataSave'),
    path('check/trip/', views.checkTrip, name='checkTrip'),

    path('checkQuestion/requirement/', views.checkQuestionRequired, name='checkQuestionRequired'),
    path('DriverPreStart/save/<int:tripId>/', views.DriverPreStartSave, name='DriverPreStartSave'),
    path('DriverPreStart/save/<int:tripId>/<int:endShift>/', views.DriverPreStartSave, name='DriverPreStartSaveWithEndShift'),

    path('Driver/break/add/view/<int:shiftId>/', views.addDriverBreak, name='addDriverBreak'),
    path('Driver/break/add/view/<int:shiftId>/<int:breakId>/', views.addDriverBreak, name='editDriverBreak'),
    path('Driver/break/add/save/<int:shiftId>/', views.saveDriverBreak, name='saveDriverBreak'),
    path('Driver/break/add/save/<int:shiftId>/<int:breakId>/', views.saveDriverBreak, name='editSaveDriverBreak'),

    path('Driver/reimbursement/view/<int:shiftId>/', views.addReimbursementView, name='addReimbursementView'),
    path('Driver/reimbursement/save/<int:shiftId>/', views.addReimbursementSave, name='addReimbursementSave'),

    path('endShift/<int:shiftId>/', views.endShift, name='endShift'),

    path('collect/dockets/<int:shiftId>/<int:tripId>/<int:endShift>/', views.collectDockets, name='collectDockets'),
    path('collect/dockets/save/<int:shiftId>/<int:tripId>/<int:endShift>/', views.collectedDocketSave, name='collectedDocketSave'),
    
    path('driver/pre-start/view/<int:shiftId>/<int:tripId>/', views.showPreStartForm, name='showPreStartForm'),
    path('driver/shift/view/<int:shiftId>/', views.driverShiftView, name='driverShiftView'),
    path('driver/select/client-docket/view/<int:shiftId>/', views.showClientAndTruckNumGet, name='showClientAndTruckNumGet'),

    # Leave section
    path('driver/leave-request/show/', views.driverLeaveRequestShow, name='driverLeaveRequestShow'),
    path('driver/leave-request/save/', views.driverLeaveRequestSave, name='driverLeaveRequestSave'),

    path('driver/past-leaves/view/', views.pastLeaveRequestShow, name='pastLeaveRequestShow'),
    path('driver/cancel-request/<int:id>/', views.cancelLeaveRequest, name='cancelLeaveRequest'),

    
    # Driver trip path end
    
    path('getTrucks/', views.getTrucks, name='getTrucks'), 
    
    path('Rcti/', views.rcti, name='rcti'), 
    # path('Rcti/Error/Solve/<int:id>', views.rctiErrorSolve, name='rctiErrorSolve'), 
    # Add RCTI manually
    path('rctiForm/', views.rctiForm, name='rctiFormAdd'), 
    path('rctiForm/<int:errorId>/<int:clientId>/<str:date>', views.rctiForm, name='rctiFormViewWithErrorId'), 
    path('rctiForm/save/', views.rctiFormSave, name='rctiFormSave'), 
    path('rctiForm/save/<int:errorId>', views.rctiFormSave, name='rctiErrorFormSave'), 
    path('rctiForm/<int:id>/', views.rctiForm, name='rctiForm'), 
    path('RctiSave/', views.rctiSave, name='rctiSave'), 
    path('uploded/rcti/', views.uplodedRCTI, name='UplodedRCTI'), 
    path('rcti/error/get/', views.getRctiError, name='getRctiError'), 
    path('rcti/Error/Form/<int:errorId>/', views.rctiErrorForm, name='rctiErrorForm'), 
    path('rcti/Error/Solve/View/<int:solveId>/', views.rctiErrorSolveView, name='rctiErrorSolveView'), 
    path('rcti/manually/managed/error/<int:errorId>/', views.rctiManuallyManagedError, name='rctiManuallyManagedError'), 
    path('rcti/manually/managed/error/docket/table/', views.rctiManuallyManagedErrorDocketTable, name='rctiManuallyManagedErrorDocketTable'), 
    path('rcti/manually/managed/error/docket/view/', views.rctiManuallyManagedErrorDocketView, name='rctiManuallyManagedErrorDocketView'), 
    path('rcti/manually/managed/error/docket/save/', views.rctiManuallyManagedErrorDocketSave, name='rctiManuallyManagedErrorDocketSave'), 
    path('rcti/error/resolve/', views.newRctiWithErrorResolve, name='newRctiWithErrorResolve'), 
    
    path('rcti/archive/', views.archiveRCTI, name='archiveRCTI'),
    path('rcti/archive/reset/', views.archiveResetRCTI, name='archiveResetRCTI'),
    
    
    # Expanse entry manually
    path('expense/', views.expanseForm, name='expanseForm'), 
    path('expense/save/', views.expanseSave, name='expanseFormSave'), 
    path('expense/<int:id>', views.expanseForm, name='expanseView'),  
    path('expense/filter/view', views.expensesFilterView, name='expensesFilterView'),  
    path('expense/table/view/', views.expensesTableView, name='expensesTableView'),  
    
    
    
    path('DriverEntry/', views.driverEntry, name='driverentry'), 
    path('DriverEntrySave/', views.driverEntrySave, name='driverEntrySave'),           
    path('DriverDocketEntry/<int:tripId>/', views.driverDocketEntry, name='driverDocketEntry'),
    
    path('driverDocket/waitingTime/count/', views.countDocketWaitingTime, name='countDocketWaitingTime'),
    path('driverDocket/standByTime/count/', views.countDocketStandByTime, name='countDocketStandByTime'),

    
    path('DriverDocketEntrySave/<int:tripId>/', views.driverDocketEntrySave, name='driverDocketEntrySave'), 
    # for error solve      
    path('DriverDocketEntrySave/<int:tripId>/<int:errorId>', views.driverDocketEntrySave, name='driverDocketErrorEntrySave'),      
    
    # Account Tables 
    # Base plant routes
    path('BasePlantTable/', views.basePlantTable, name='basePlantTable'),
    path('BasePlant/add/', views.basePlantForm, name='basePlantAdd'),
    path('BasePlant/add/save/', views.basePlantSave, name='basePlantAddSave'),   
    path('BasePlant/edit/<int:id>/', views.basePlantForm, name='basePlantEdit'),      
    path('BasePlant/edit/save/<int:id>/', views.basePlantSave, name='basePlantEditSave'),   

    # Location
    # path('location/save/', views.locationSave, name='locationSave'), 
    # path('location/edit/<int:id>/', views.locationEditForm, name='locationEdit'),   
    # path('location/edit/save/<int:id>', views.locationSave, name='locationEditSave'),   

    path('RctiTable/', views.rctiTable, name='rctiTable'),
    # path('DriverTripsTable/', views.driverTripsTable, name='driverTripsTable'),

    # Rate Card 
    path('RateCardTable', views.rateCardTable, name='rateCardTable'),
    path('RateCardTable/<int:clientId>/', views.rateCardTable, name='rateCardTableClient'),
    path('RateCardTable/<int:clientId>/<int:clientOfcId>/', views.rateCardTable, name='rateCardTableClientOfc'),
    
    path('RateCardForm/<int:clientId>/<int:clientOfcId>/', views.rateCardForm, name='rateCardForm'),
    # path('RateCardForm/<int:clientId>', views.rateCardForm, name='rateCardWithClient'),
    path('RateCardSave/<int:clientOfcId>/', views.rateCardSave, name='rateCardSave'),
    path('RateCard/view/<int:id>/', views.rateCardForm, name='rateCardView'),
    path('RateCard/revision/<int:id>/', views.rateCardSave, name='rateCardRevision'),
    path('RateCard/revision/<int:id>/<int:edit>/', views.rateCardSave, name='rateCardRevision'),
    path('getOld/rateCards/', views.getOldRateCards, name='getOldRateCards'),
    
    
    # DriverTrip Csv
    path('DriverShiftCsv/', views.driverShiftCsv, name='driverShiftCsv'),
    path('RctiCsvForm/', views.rctiCsvForm, name='rctiCsvForm'),
    path('DriverSampleCsv/', views.driverSampleCsv, name='driverSampleCsv'),
    
    # Edit
    path('driverTrip/edit/<int:id>/', views.DriverTripEditForm, name='DriverTripEdit'), 
    path('charge-job/edit/<int:id>/<int:typeOfShift>/', views.DriverTripEditForm, name='chargeJobEdit'), 
    path('ongoing/shift/end/<int:tripId>/', views.ongoingShiftEnd, name='ongoingShiftEnd'), 
    path('driverShift/archive/<int:shiftId>/', views.DriverShiftArchive, name='DriverShiftArchive'), 
    path('driverShift/restore/<int:shiftId>/', views.RestoreDriverShift, name='RestoreDriverShift'),
    path('driverTrip/update/<int:shiftId>/', views.driverEntryUpdate, name='driverEntryUpdate'), 
    path('driverTrip/docket/update/', views.driverDocketUpdate, name='driverDocketUpdate'), 
    path('driverTrip/entry/<int:shiftId>/', views.tripEntry, name='tripEntry'), 
    path('get/driver/break/', views.getDriverBreak, name='getDriverBreak'), 
    path('check/trip/deficit', views.checkTripDeficit, name='checkTripDeficit'), 
    path('get/last/trip/', views.getLastTrip, name='getLastTrip'), 
    
    path('ocr/read/', views.ocrRead, name='ocrRead'), 
    
    # Filters
    path('verifiedFilter/', views.verifiedFilter, name='verifiedFilter'),  
    path('clientFilter/', views.clientFilter, name='clientFilter'),  
    path('dateRangeFilter/', views.dateRangeFilter, name='dateRangeFilter'),


    # Reconciliation

    # path('reconciliation/report/filter/<int:dataType>/', views.reconciliationReportFilter, name='reconciliationReportFilter'),
    path('reconciliation/form/<int:dataType>/', views.reconciliationForm, name='reconciliationForm'),
    path('reconciliation/analysis/<int:dataType>/', views.reconciliationAnalysis, name='reconciliationAnalysis'),
    path('reconciliation/analysis/<int:dataType>/<int:download>/', views.reconciliationAnalysis, name='reconciliationAnalysisDownload'),

    path('reconciliation/docket/view/<int:reconciliationId>/', views.reconciliationDocketView, name='reconciliationDocketView'),
    path('reconciliation/setMark/', views.reconciliationSetMark, name='reconciliationSetMark'),
    
    path('reconciliation/escalate/checkClient/', views.escalationClientCheck, name='escalationClientCheck'),

    path('reconciliation/escalation/form1/<str:reconciliationId>/<str:clientName>/', views.showReconciliationEscalation1, name='showReconciliationEscalation1'),
    path('reconciliation/get/difference/', views.getCostDifference, name='getCostDifference'),

    path('reconciliation/escalation/create/<str:reconciliationIdStr>/<str:clientName>/', views.createReconciliationEscalation, name='createReconciliationEscalation'),

    path('reconciliation/escalation/add/mail/<int:id>/', views.reconciliationEscalationMailAdd, name='reconciliationEscalationMailAdd'),
    
    path('reconciliation/escalation/form2/<int:escalationId>/', views.showReconciliationEscalation2, name='showReconciliationEscalation2'),
    path('reconciliation/escalation/form3/<int:id>/', views.reconciliationEscalationForm3, name='reconciliationEscalationForm3'),
    path('reconciliation/escalation/complete/<int:id>/', views.reconciliationEscalationComplete, name='reconciliationEscalationComplete'),
   
    path('reconciliation-filter/', views.reconciliationFilters, name='reconciliationFilters'),

    # Custom report
    path('Custom-report/view/', views.customReportView, name='customReportView'),

    # Public holiday
    path('publicHoliday/', views.publicHoliday, name='publicHoliday'),
    path('publicHoliday/add/', views.publicHolidayForm, name='publicHolidayAdd'),
    path('publicHoliday/add/save/', views.publicHolidaySave, name='publicHolidaySave'),

    path('publicHoliday/edit/<int:id>/', views.publicHolidayForm, name='publicHolidayEdit'),
    path('publicHoliday/edit/save/<int:id>/', views.publicHolidaySave, name='publicHolidayEditSave'),
    
    # Past trip
    path('pastTrip/form/',views.PastTripForm, name='pastTripForm'),
    path('pastTrip/form/save/',views.pastTripSave, name='pastTripSave'),
    path('pastTrip/errorSolve/<int:id>/',views.pastTripErrorSolve, name='pastTripErrorSolve'),
    path('pastTrip/error/resolve/<int:tripId>/<int:errorId>/', views.driverDocketEntry, name='pastTripErrorResolve'),
    path('pastTrip/error/get/', views.getSinglePastTripError, name='getSinglePastTripError'),
    path('pastTrip/solve/error/get/', views.getSinglePastTripSolveError, name='getSinglePastTripSolveError'),
    
    path('uploded/pastTrip/', views.uplodedPastTrip, name='uplodedPastTrip'),
    path('archive/pastTrip/', views.archivePastTrip, name='archivePastTrip'),
    path('archive/reset/pastTrip/', views.archiveReset, name='archiveReset'),
    
    
     
    # Base plant routes
    path('SurchargeTable/', views.surchargeTable, name='surchargeTable'),
    path('Surcharge/add/', views.surchargeForm, name='surchargeAdd'),
    path('Surcharge/add/save/', views.surchargeSave, name='surchargeAddSave'),   
    path('Surcharge/edit/<int:id>/', views.surchargeForm, name='surchargeEdit'),      
    path('Surcharge/edit/save/<int:id>/', views.surchargeSave, name='surchargeEditSave'),
    
    # Trip 
    path('Driver/Shift/Form/<int:id>', views.DriverShiftForm, name='DriverShiftForm'),
    path('Driver/Shift/Details/<int:id>', views.ShiftDetails, name='ShiftDetails'),
    path('running-trucks/', views.runningTrucks, name='runningTrucks'),
    
    # Holcim 
    path('Holcim/Docket/View/<int:id>', views.HolcimDocketView, name='HolcimDocketView'),
    # path('rctiHolcimForm/<int:holcimDocketId>/', views.rctiForm, name='rctiHolcimForm'), 
    path('rctiHolcimFormSave/', views.rctiHolcimFormSave, name='rctiHolcimFormSave'), 
    
    
    
    # Top Up 
    path('TopUp/Form/<int:id>', views.topUpForm, name='topUpForm'), 
    path('TopUp/View/<int:id>/<int:topUpDocket>', views.topUpForm, name='topUpView'), 
    # Ajax 
    path('TopUp/Solve', views.topUpSolve, name='topUpSolve'),
    
    
    # Report Holcim
    path('Report/', views.report, name='report'),
    path('Report/Save', views.reportSave, name='reportSave'),
    
    

    # EscalationForm 
    path('Manually-Escalation/Form/', views.EscalationForm, name='EscalationForm'),
    path('Escalation/Table/', views.EscalationTable, name='EscalationTable'),
    path('Escalation/Form/View/<int:id>/', views.EscalationForm, name='EscalationFormView'),
    path('Manually/Escalation/Forma/Save/', views.manuallyEscalationForm1Save, name='manuallyEscalationForm1Save'),
    path('Escalation/View/<int:escalationId>/', views.ViewBulkEscalationData, name='ViewBulkEscalationData'),

    # Find job filters
    path('job/selectedStatus/', views.jobSelectedStatus, name='jobSelectedStatus'),
    
    # History URLs
    
    path('history/cost-parameter/<int:id>/', views.costParameterHistory, name='costParameterHistory'), 
    path('history/threshHoldDay/<int:id>/', views.threshHoldDayHistoryHistory, name='threshHoldDayHistoryHistory'), 
    path('history/threshHoldNight/<int:id>/', views.threshHoldNightHistoryHistory, name='threshHoldNightHistoryHistory'), 
    path('history/grace/<int:id>/', views.graceHistory, name='graceHistory'), 

    path('history/base-plant/<int:id>/', views.basePlantHistory, name='basePlantHistory'), 

    path('history/trip/<int:tripId>/', views.tripHistory, name='tripHistory'), 
    path('history/docket/<int:docketId>/', views.docketHistory, name='docketHistory'), 
    path('history/break/<int:breakId>/', views.breakHistory, name='breakHistory'), 

    path('history/rcti/<int:rctiId>/', views.rctiHistory, name='rctiHistory'), 
    path('history/escalation/<int:escalationId>/', views.escalationHistory, name='escalationHistory'), 
    
    
    # ***********************************************
    # API urls
    # ***********************************************
    
    # path('api/shift-start/', views.apiMapDataSave, name='apiMapDataSave'),
    # path('api/getClients/', views.getClients, name='getClients'),
    # path('api/getTrucks/', views.getTrucks, name='getTrucks'),

    # path('api/apiClientAndTruckData/save/', views.apiClientAndTruckDataSave, name='apiClientAndTruckDataSave'),
    # path('api/getPreStartQuestions/', views.getPreStartQuestions, name='getPreStartQuestions'),
    
]
