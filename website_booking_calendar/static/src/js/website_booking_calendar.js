(function (self, $) {

    self.DTF = 'YYYY-MM-DD HH:mm:ss';
    self.MIN_TIME_SLOT = 1; //hours
    self.SLOT_START_DELAY_MINS = 15 //minutes
    self.resources = [];
    self.bookings = [];

    self.jsonRpc = function(url, data, callback) {
        $.ajax({
            url: url,
            dataType: 'json',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify({
                params: data,
                jsonrpc: '2.0',
                id: Math.floor(Math.random() * 1000 * 1000 * 1000)
            }),
            success: callback
        });
    }

    self.loadEvents = function(start, end, timezone, callback) {
        self.jsonRpc('/booking/calendar/events', {
                start: start.format(self.DTF),
                end: end.format(self.DTF),
                resources: self.resources
        }, function(response) {
            var events = response;
            callback(events['result']);
        });
    };

    self.warn = function(text) {
        var $bookingWarningDialog = $('#booking_warning_dialog');
        $bookingWarningDialog.find('.modal-body').text(text);
        $bookingWarningDialog.modal('show');
    }

    self.eventReceive = function(event) {
        if (event.start < moment().add(-self.SLOT_START_DELAY_MINS, 'minutes')){
            self.warn('Please book on time in ' + self.SLOT_START_DELAY_MINS + ' minutes from now.');
            self.$calendar.fullCalendar('removeEvents', [event._id]);
            return;
        }
        self.bookings.push(event);
    };

    self.eventOverlap = function(stillEvent, movingEvent) {
        return stillEvent.resourceId != movingEvent.resourceId;
    };

    self.eventDrop = function(event, delta, revertFunc, jsEvent, ui, view){
        if (event.start < moment().add(-self.SLOT_START_DELAY_MINS, 'minutes')){
            self.warn('Please book on time in ' + self.SLOT_START_DELAY_MINS + ' minutes from now.');
            revertFunc(event);
        }
    };

    self.getBookingsInfo = function(toUTC) {
        var res = [];
        for(var i=0, len=self.bookings.length; i<len; i++) {
            var start = self.bookings[i].start.clone();
            var end = self.bookings[i].end ? self.bookings[i].end.clone() : start.clone().add(1, 'hours');
            if(toUTC) {
                start.utc();
                end.utc();
            }
            res.push({
                'resource': self.bookings[i].resourceId,
                'start': start.format(self.DTF),
                'end': end.format(self.DTF)
            });
        }
        return res;
    }

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
                borderColor: 'red',
                color: $(this).data('color'),
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
            height: 'auto',
            editable: true,
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
            slotEventOverlap: false,
            events: self.loadEvents,
            eventReceive: self.eventReceive,
            eventOverlap: self.eventOverlap,
            eventDrop: self.eventDrop
            // eventRender: function(event, element) {
            //     element.find(".fc-content").append( "<span class='closeon'>x</span>" );
            //     element.find(".closeon").click(function() {
            //        self.$calendar.fullCalendar('removeEvents', event._id);
            //     });
            // }
        });

        $('#add-to-cart').click(function(){
            var $contentBlock = $('#booking-dialog').find('.modal-body');
            $contentBlock.load('/booking/calendar/confirm/form', {
                events: JSON.stringify(self.getBookingsInfo()),
            }, function(){
                $('.booking-product').change(function(){
                    var price = $(this).find(':selected').data('price');
                    var currency = $(this).find(':selected').data('currency');
                    $(this).closest('tr').find('.booking-price').text(price);
                    $(this).closest('tr').find('.booking-currency').text(currency);
                });
                $('#booking-dialog').modal('show');
            });
        });

        $('#booking-dialog-confirm').click(function(){
            $('#booking-dialog').find('form').submit();
        })

    };
}(window.booking_calendar = window.booking_calendar || {}, jQuery));

$(document).ready(function() {
    booking_calendar.init();
});