const csrftoken = $("[name=csrfmiddlewaretoken]").val();

$(document).ready(function () {
  $("#status").select2({
    placeholder: "Select status",
    templateResult: formatOption,
  });

  $("#status").on("change", function () {
    var selectedStatus = $(this).val();
    // console.log(selectedStatus);
    getDataFilter(selectedStatus);
  });

  $("#closeBtn").on("click", function () {
    $("#appointmentModel").modal("hide");
  });
  getDataFilter(null);

  $("#cancelJobBtn").on("click", function () {
    $("#cancelModel").modal("show");
  });

  $("#filterBtn").on("click", function () {
    $("#filterModal").modal("show");
  });

  $("#status").on("change", function () {
    // var selectedStatus = $(this).val();
    getDataFilter();
  });

  $("#filterApplyBtn").on("click", function () {
    $("#filterModal").modal("hide");
    getDataFilter();
  });
});



function setDataInTable(tableId, data) {
  var table = $(`#${tableId}`).DataTable();
  table.clear().draw();
  $.each(data, function (index, item) {
    table.row
      .add([
        item.Status,
        item.Title,
        item.Start_Date_Time,
        item.End_Date_Time,
        '<div class="d-flex justify-content-around">' +
          '<a href="/appointment/appointmentForm/view/' +
          item.id +
          '" title="View appointment">' +
          '<i class="fa-regular fa-eye" style="font-size:1.3rem"></i>' +
          "</a>" +
          '<a href="/appointment/appointmentForm/update/' +
          item.id +
          '/?update=1" title="Edit appointment">' +
          '<i class="fa-solid fa-file-pen" style="font-size:1.3rem"></i>' +
          "</a>" +
          "</div>",
      ])
      .draw();
  });
}

function clearFilter(id) {
  $(`#${id} input[type="checkbox"]`).each(function () {
    $(this).attr("checked", false);
  });
}

function getDataFilter() {
  var selectedStatus = $("#status").val();
  var selectedDrivers = [];
  var selectedLocations = [];
  var selectedVehicles = [];
  var selectedContents = [];

  $('#filterDriver input[type="checkbox"]').each(function () {
    if ($(this).prop("checked")) {
      selectedDrivers.push($(this).attr("id"));
    }
  });

  $('#filterLocation input[type="checkbox"]').each(function () {
    if ($(this).prop("checked")) {
      selectedLocations.push($(this).attr("id"));
    }
  });

  $('#filterVehicle input[type="checkbox"]').each(function () {
    if ($(this).prop("checked")) {
      selectedVehicles.push($(this).attr("id"));
    }
  });

  $('#filterContent input[type="checkbox"]').each(function () {
    if ($(this).prop("checked")) {
      selectedContents.push($(this).attr("id"));
    }
  });
  console.log(selectedContents);

  $.ajax({
    url: "/appointment/get/driver-appointment/",
    method: "POST",
    data: {
      selectedStatus: selectedStatus,
      selectedDrivers: selectedDrivers,
      selectedLocations: selectedLocations,
      selectedVehicles: selectedVehicles,
      selectedContents: selectedContents,
    },
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (data) {
      if (data.status) {
        setCalendar(data);
      }
    },
  });
}

function getColorBasedOnStatus(status) {
  if (status === "Unassigned") {
    return "#E74C3Ca8";
  } else if (status === "Assigned") {
    return "#ff8700a8";
  } else if (status === "Dispatched") {
    return "#0084DDa8";
  } else if (status === "InProgress") {
    return "#00B140a8";
  } else if (status === "Incomplete") {
    return "#0e6211a8";
  } else if (status === "Complete") {
    return "#A9A9A9a8";
  } else if (status === "Cancelled") {
    return "#0000008a";
  }
}

function setCalendar(data) {
  var calendarEl = document.getElementById("calendar");
  var calendar = new FullCalendar.Calendar(calendarEl, {
    headerToolbar: {
      left: "today resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth,list",
      center: "title",
      right: "prev,next",
    },
    aspectRatio: 1.6,
    initialView: "resourceTimelineDay",
    slotDuration: "01:00",
    views: {
      resourceTimelineMonth: {
        buttonText: "Month",
        slotDuration: "24:00:00",
        slotMinWidth: "70",
      },
      resourceTimelineWeek: {
        buttonText: "Week",
        duration: { days: 7 },
        slotDuration: "24:00:00",
      },
      resourceTimelineDay: {
        buttonText: "Day",
        slotDuration: "01:00",
      },
    },
    resourceAreaWidth: "20%",
    selectable: true,
    selectHelper: true,
    eventLimit: true,
    select: function (start, end, jsEvent, view) {
      console.log("Selected: " + start + " to " + end);
      // alert("Selected: " + start + " to " + end);
    },
    resources: data.drivers,
    events: data.appointments,
    eventContent: function (arg) {
      var color = getColorBasedOnStatus(arg.event.extendedProps.status);
      var eventTitles = arg.event.title.split(",");
      var titleHtml = "";

      eventTitles.forEach(function (title) {
        titleHtml += '<div class="event-title">' + title + "</div>";
      });
      var html = $("<div>", {
        class: "event-container px-1 py-2",
        style:
          "background-color: " + color + "; border:1px solid " + color + ";",
      }).append(titleHtml);

      return { html: html[0].outerHTML };
    },
    eventClick: function (info) {
      var eventId = info.event._def.publicId;
      showAppointment(eventId);
    },
  });
  calendar.render();
  var newDriver = {
    id: "0", 
    title: "Unassigned"    
  };

  calendar.addResource(newDriver);
  calendar.render();
  $(`.event-title`).each(function () {
    let titleVal = $(this).text();
    $(this).parent(".event-container").attr("title", titleVal);
  });

  $('.fc-datagrid-header.fc-scrollgrid-sync-table .fc-datagrid-cell-main').text('Drivers');
}

function formatOption(option) {
  if (!option.id) {
    return option.text;
  }
  var $option = $(
    '<span><span class="badge" style="background-color:' +
      $(option.element).data("badge-color") +
      ';width:15px;height:15px;display-inline-block;"> </span> ' +
      option.text +
      "</span>"
  );
  return $option;
}

function cancelJob(appointmentId) {
  $.ajax({
    url: "/appointment/cancelJob/",
    method: "POST",
    data: {
      appointmentId: appointmentId,
    },
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (data) {
      if (data.status) {
        location.reload();
      } else {
        alert("Something went wrong, please try again.");
      }
    },
  });
}

function showAppointment(appointmentId) {
  $.ajax({
    url: "/appointment/get/single/appointment/",
    method: "POST",
    data: {
      appointmentId: appointmentId,
    },
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (data) {
      if (data.status) {
        $("#appTitle").text(data.appointmentObj.title);
        $("#appClient").text(data.appointmentObj.clientName);
        $("#appStartDateTime").text(data.appointmentObj.startTime);
        $("#appEndDateTime").text(data.appointmentObj.endTime);
        $("#appReportOrigin").text(data.appointmentObj.reportingTime);
        $("#appStatus").text(data.appointmentObj.status);
        $("#appOrigin").text(data.appointmentObj.origin_id);
        $("#appStaffNotes").text(data.appointmentObj.staffNotes);
        $("#appDriverNotes").text(data.appointmentObj.driverNotes);
        $("#appShiftType").text(data.appointmentObj.shiftType);
        $("#appCreatedBy").text(data.appointmentObj.createdBy_id);
        $("#appCreatedTime").text(data.appointmentObj.createdTime);
        $("#appPreStart").text(data.appointmentObj.preStartWindow);

        if (data.truckObj) {
          $("#truckNum").text(data.truckObj.adminTruckNumber);
        } else {
          $("#truckNum").text("Not assigned");
        }

        if (data.appointmentObj.status == "Cancelled") {
          $("#cancelJobBtn").addClass("d-none");
          $("#editBtn").addClass("d-none");
        }

        if (data.driverObj) {
          $("#driverName").text(data.driverObj.name);
          $("#driverPhone").text(data.driverObj.phone);
          $("#driverEmail").text(data.driverObj.email);
        } else {
          $("#driverName").text("Not assigned");
          $("#driverPhone").text("Not assigned");
          $("#driverEmail").text("Not assigned");
        }
        if (data.originObj) {
          $("#originBasePlant").text(data.originObj.basePlant);
          $("#originAddress").text(data.originObj.address);
          $("#originPhone").text(data.originObj.phone);
          $("#originPersonOnName").text(data.originObj.personOnName);
          $("#originManagerName").text(data.originObj.managerName);
        }else{
          $("#originBasePlant").text('Not assigned');
          $("#originAddress").text('Not assigned');
          $("#originPhone").text('Not assigned');
          $("#originPersonOnName").text('Not assigned');
          $("#originManagerName").text('Not assigned');
        }

        $('.modalStopSection').empty();
        content = `<h5 class="mb-0">Stop</h5>`
        data.stopObjs.forEach(function(stop){
          content += `<hr>`
          content += `<div class="row">`
          content += `<div class="col-md-4">`
          content += `<p><strong>Stop name:</strong> <span id="originBasePlant" class="text-capitalize">${stop.stopName}</span></p>`
          content += `</div>`
          content += `<div class="col-md-3">`
          content += `<p><strong>Phone:</strong> <span id="originPhone" class="text-capitalize">${stop.stopPhone}</span></p>`
          content += `</div>`
          content += `<div class="col-md-3">`
          content += `<p><strong>Duration :</strong> <span id="originManagerName" class="text-capitalize">${stop.duration}</span></p>`
          content += `</div>`
          content += `<div class="col-md-2">`
          content += `<a href="/appointment/edit/stop/view/${stop.id}/"><i class="fa-regular fa-pen-to-square float-right" style="font-size:1.1em"></i></a>`
          content += `</div>`
          content += `</div>`
          content += `<div class="row">`
          content += `<div class="col-md-4">`
          content += `<p><strong>Stop type:</strong> <span id="originPersonOnName" class="text-capitalize">${stop.stopType}</span></p>`
          content += `</div>`
          content += `<div class="col-md-8 col-sm-8">`
          content += `<p><strong>Address:</strong> <span id="originAddress" class="text-capitalize">${stop.stopAddress}</span></p>`
          content += `</div>`
          content += `</div>`
        })
        if (data.stopObjs.length > 0) {
          $(".modalStopSection").removeClass('d-none').append($(content));
        }

        $("#editBtn").attr(
          "href",
          `/appointment/appointmentForm/update/view/${appointmentId}/1/`
        );

        $('.addStopBtn').attr('href',`/appointment/add/stop/view/${appointmentId}`)

        $("#cancelModel #yes").attr("onClick", `cancelJob(${appointmentId})`);
        $("#appointmentModel").modal("show");
      }
    },
  });
}


// function getDataFilter(selectedStatus) {
//   $.ajax({
//     url: "/appointment/get/driver-appointment/",
//     method: "POST",
//     data: {
//       selectedStatus: selectedStatus,
//     },
//     beforeSend: function (xhr) {
//       xhr.setRequestHeader("X-CSRFToken", csrftoken);
//     },
//     success: function (data) {
//       if (data.status) {
//         setCalendar(data);
//       }
//     },
//   });
// }