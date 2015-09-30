var bookings = new Array();
var isBackend = false;


function init_backend(isBackend, bookings) {
    window.isBackend = isBackend;
    $('#calendar').fullCalendar({
        events: bookings
    });
}

function make_editable(ids) {

}

$(document).ready(function() {

    /* initialize the external events
    -----------------------------------------------------------------*/

    $('#external-events .fc-event').each(function() {

      
      $('#calendar').fullCalendar('addResource', {
        id: $(this).data('resource'),
        title: $.trim($(this).text()),
      });

      // store data so the calendar knows to render an event upon drop
      $(this).data('event', {
        title: $.trim($(this).text()), // use the element's text as the event title
        stick: true, // maintain when user navigates (see docs on the renderEvent method)
        resourceId: $(this).data('resource'),
        borderColor: 'red'
      })


      // make the event draggable using jQuery UI
      $(this).draggable({
        zIndex: 999,
        revert: true,      // will cause the event to go back to its
        revertDuration: 0  //  original position after the drag
      });

    });

    // page is now ready, initialize the calendar...

    $('#calendar').fullCalendar({
        header: {
          left: 'prev,next today',
          center: 'title',
          right: 'month,agendaWeek,agendaDay'
        },
        handleWindowResize: true,
        editable: true,
        eventLimit: true,
        droppable: true, // this allows things to be dropped onto the calendar
        eventResourceField: 'resourceId',
        slotDuration: '01:00:00',
        allDayDefault: false,
        allDaySlot: false,
        defaultTimedEventDuration: '01:00:00',
        displayEventTime: false,
        timezone: 'local',

        events: function(start, end, timezone, callback) {
            $.ajax({
                url: '/booking/calendar/events',
                dataType: 'json',
                contentType: 'application/json',
                method: 'post',
                data: JSON.stringify({params: {
                    // our hypothetical feed requires UNIX timestamps
                    start: start.format("YYYY-MM-DD HH:mm:ss"),
                    end: end.format("YYYY-MM-DD HH:mm:ss"),
                }}),
                success: function(response) {
                    var events = response;
                    callback(events['result']);
                }
            });
        },

        eventReceive: function( event ) {
            if (isBackend) {
                bookings.push(event);
            } else {
                $.ajax({
                    url: '/booking/calendar/events/add',
                    dataType: 'json',
                    contentType: 'application/json',
                    method: 'post',
                    data: JSON.stringify({params: {
                        // our hypothetical feed requires UNIX timestamps
                        resource_id: event.resourceId,
                        start: event.start.format("YYYY-MM-DD HH:mm:ss"),
                        end: event.start.add(1, 'hours').format("YYYY-MM-DD HH:mm:ss"),
                    }}),
                    success: function(response) {
                        event.id = response;
                        $('#calendar').fullCalendar('updateEvent', event);
                    }
                });
            }
        },
        eventDrop: function(event, delta, revertFunc) {

            console.log(event.title + " was dropped on " + event.start.format());

        },

        eventOverlap: function(stillEvent, movingEvent) {
            return stillEvent.resourceId != movingEvent.resourceId;
        },

         eventRender: function(event, element) {
            element.find(".fc-content").append( "<span class='closeon'>x</span>" );
            element.find(".closeon").click(function() {
               $('#calendar').fullCalendar('removeEvents', event._id);
            });
        }

    })

});