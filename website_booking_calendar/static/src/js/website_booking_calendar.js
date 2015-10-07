(function (self, $) {

    self.resources = [];

    self.loadEvents = function(start, end, timezone, callback) {
        $.ajax({
            url: '/booking/calendar/events',
            dataType: 'json',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify({params: {
                // our hypothetical feed requires UNIX timestamps
                start: start.format("YYYY-MM-DD HH:mm:ss"),
                end: end.format("YYYY-MM-DD HH:mm:ss"),
                resources: self.resources
            }}),
            success: function(response) {
                var events = response;
                callback(events['result']);
            }
        });
    };

    self.addEvent = function(event) {
        $.ajax({
            url: '/booking/calendar/events/add',
            dataType: 'json',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify({params: {
                // our hypothetical feed requires UNIX timestamps
                resource_id: event.resourceId,
                start: event.start.format("YYYY-MM-DD HH:mm:ss"),
                end: event.start.add(1, 'hours').format("YYYY-MM-DD HH:mm:ss"),
            }}),
            success: function(response) {
                event.id = response;
                self.$calendar.fullCalendar('updateEvent', event);
            }
        });
    };

    self.eventReceive = function(event) {
        self.addEvent(event);
    };

    /* initialize the external events
    -----------------------------------------------------------------*/
    self.init = function() {
        self.$calendar = $('#calendar');
        $('#external-events .fc-event').each(function() {
            self.resources.push($(this).data('resource'));
            // store data so the calendar knows to render an event upon drop
            $(this).data('event', {
                title: $.trim($(this).text()), // use the element's text as the event title
                stick: true, // maintain when user navigates (see docs on the renderEvent method)
                resourceId: $(this).data('resource'),
                borderColor: 'red'
            });
            // make the event draggable using jQuery UI
            $(this).draggable({
                zIndex: 999,
                revert: true,      // will cause the event to go back to its
                revertDuration: 0  //  original position after the drag
            });
        });

        // page is now ready, initialize the calendar...
        self.$calendar.fullCalendar({
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
            firstDay: 1,
            defaultView: 'agendaWeek',
            timezone: 'local',
            events: self.loadEvents,
            eventReceive: self.eventReceive,
            eventDrop: function(event, delta, revertFunc) {

                console.log(event.title + " was dropped on " + event.start.format());

            },
            eventOverlap: function(stillEvent, movingEvent) {
                return stillEvent.resourceId != movingEvent.resourceId;
            },

            eventRender: function(event, element) {
                element.find(".fc-content").append( "<span class='closeon'>x</span>" );
                element.find(".closeon").click(function() {
                   self.$calendar.fullCalendar('removeEvents', event._id);
                });
            }
        });
    };
}(window.booking_calendar = window.booking_calendar || {}, jQuery));

$(document).ready(function() {
    booking_calendar.init();
});