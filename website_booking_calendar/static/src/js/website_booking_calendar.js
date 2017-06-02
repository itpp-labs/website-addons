(function (self, $) {

    self.DTF = 'YYYY-MM-DD HH:mm:ss';
    self.MIN_TIME_SLOT = 1; //hours
    self.SLOT_START_DELAY_MINS = 15; //minutes
    self.resources = [];
    self.bookings = [];
    self.session = openerp.website.session || new openerp.Session();
    self.domain = [];
    self.colors = {};

    self.loadSlots = function(start, end, timezone, callback) {
        var d = new Date();
        var offset = d.getTimezoneOffset();
        self.session.rpc("/booking/calendar/slots", {
           // start: start.add(offset, 'minutes').format(self.DTF),
           // end: end.add(offset, 'minutes').format(self.DTF),
           // tz: offset,
           start: start.format(self.DTF),
           end: end.format(self.DTF),
           tz: 0,
           domain: self.domain
        }).then(function (response) {
            callback(response);
        });
    };
    self.loadBookings = function(start, end, timezone, callback) {
        var d = new Date();
        var offset = d.getTimezoneOffset();
        self.session.rpc("/booking/calendar/slots/booked", {
           // start: start.add(offset, 'minutes').format(self.DTF),
           // end: end.add(offset, 'minutes').format(self.DTF),
           // tz: d.getTimezoneOffset(),
           start: start.format(self.DTF),
           end: end.format(self.DTF),
           tz: 0,
           domain: self.domain
        }).then(function (response) {
            callback(response);
        });
    };

    self.warn = function(text) {
        var $bookingWarningDialog = $('#booking_warning_dialog');
        $bookingWarningDialog.find('.modal-body').text(text);
        $bookingWarningDialog.modal('show');
    };

   self.getBookingsInfo = function(toUTC) {
        var res = [];
        _.each(self.bookings, function(b) {
            var start = b.start.clone();
            var end = b.end ? b.end.clone() : start.clone().add(1, 'hours');
            if(toUTC) {
                start.utc();
                end.utc();
            }
            res.push({
                'resource': b.resource_id,
                'start': start.format(self.DTF),
                'end': end.format(self.DTF)
            });
        });
        return res;
    };

    self.viewRender = function(view, element) {
        if (view.name == 'agendaWeek') {
            $(element).find('th.fc-day-header').css({'cursor': 'pointer'})
                .click(function(){
                    var m = moment($(this).text(), view.calendar.option('dayOfMonthFormat'));
                    if (m < view.start) {
                        m.year(view.end.year());
                    }
                    view.calendar.changeView('agendaDay');
                    view.calendar.gotoDate(m);
                });
        }
    };

    self.getParameterByName = function(name, url) {
       if (!url) {
         url = window.location.href;
       }
       name = name.replace(/[\[\]]/g, "\\$&");
       var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
           results = regex.exec(url);
       if (!results) return null;
       if (!results[2]) return '';
       return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    /* initialize the external events
    -----------------------------------------------------------------*/
    self.init = function() {
        self.$calendar = $('#calendar');
        // page is now ready, initialize the calendar...
        self.$calendar.fullCalendar({
            handleWindowResize: true,
            height: 'auto',
            eventResourceField: 'resource_id',
            slotDuration: '01:00:00',
            allDayDefault: false,
            allDaySlot: false,
            displayEventTime: false,
            firstDay: 1,
            defaultView: 'agendaWeek',
            timezone: false,
            weekNumbers: true,
            eventSources: [
                { events: self.loadSlots },
                { events: self.loadBookings }
            ],
            viewRender: self.viewRender,
            eventClick: self.eventClick,
            customButtons: {
                confirm: {
                    text: 'Add to Cart',
                    click: self.confirm
                }
            },
            header: {
                left: 'confirm prev,next today',
                center: 'title',
                right: 'agendaWeek,agendaDay'
            },
            slotEventOverlap: false
        });

        $('#booking-dialog-confirm').click(function(){
            var $form = $('#booking-dialog').find('form');
            var $msg = $('#booking-taken-msg')
            var d = new Date();
            $form.find("[name=timezone]").val(d.getTimezoneOffset());
            var tr_counter = 0;
            var validated_counter = 0;
            var deferreds = [];
            $form.find('tbody tr').each(function() {
               var tr_element = $(this)
               tr_counter = tr_counter + 1;
               deferreds.push(
                  openerp.jsonRpc('/booking/validator', 'call', {'booking': $(this).find('select').attr('name')}).then(function(result) {
                     if(result) {
                        tr_element.css({'color': 'red'});
                        $msg.css({'visibility': 'visible'});
                     } else {
                        validated_counter = validated_counter + 1;
                     }
                  })
               );
            })


            $.when.apply($, deferreds).done(function() {
               if(validated_counter === tr_counter || $form.find("[name='validation_passed']").val()) {
                  $form.submit();
               }
               if(validated_counter) {
                  $form.find("[name='validation_passed']").val(true);
               }
            });
        });

       if (self.getParameterByName('expired')) {
          self.warn('Your shopping cart has expired. All the bookings has been cleared')
       }

    };

    self.confirm = function() {
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
            $('#booking-taken-msg').css({'visibility': 'hidden'});
            $('#booking-dialog').modal('show');
        });
    };

    self.eventClick = function(calEvent, jsEvent, view) {
        $slot = $(this);
        if ($slot.hasClass('booked_slot')) {
            return;
        }
        if (!($("[name=is_logged]").val())) {
            window.location = '/web/login?redirect='+encodeURIComponent(window.location);
            return;
        }
        var booked = false;
        _.each(self.bookings, function (b, k) {
            if (b._id == calEvent._id) {
                booked = true;
                $slot.removeClass('selected');
                if (self.colors[calEvent._id]) {
                    $slot.attr(self.colors[calEvent._id]);
                }
                self.bookings.splice(k, 1);
            }
        });
        if ( !booked ) {
            self.bookings.push(calEvent);
            $slot.addClass('selected');
            self.colors[calEvent._id] = {
                'background-color': $slot.attr('background-color'),
                'border-color': $slot.attr('border-color'),
            };
            $slot.css('background-color', '');
            $slot.css('border-color', '');
        }

    };
}(window.booking_calendar = window.booking_calendar || {}, jQuery));

$(document).ready(function() {
    booking_calendar.init();
});
