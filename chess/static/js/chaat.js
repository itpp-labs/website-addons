(function() {
	"use strict";
	
	var ajax = require('web.ajax');
	var bus = require('bus.bus');
	var data = {};
	1
	var chat = {
		init_chat: function(){
			
			data.message = $("#message_text").val(); /*get message*/
			/*вытащить ник пользователя и время отправки сообщения*/
			send_message(data);
		},

		get_message: function(data){
			
			// Gets the list of messages from the server ??????
			
			/*display messages*/
			$("#window_chat").append("<p><span class='user'>" + (data['user']) +
			"</span>: " + (data['message']) + "<span class='time_message'>: " + 
			(data['time']) + "</span></p>");
			
			// scroll to bottom
			$("#window_chat").each(function () {
				this.scrollTop = this.scrollHeight;
			});
		},
		
		poll: function() {
			
			var self = this;

            this.bus = bus.bus;
            this.bus.on("notification", this, this.on_notification);
            this.bus.start_polling();
			/*получаем сообщение из сервера в случае
			если сообщение было получено успешно вызываем функцию get_message
			и передаем полученное сообщение*/
			get_message(data);
			/*если сообщение не было получено, т.е. запрос не получил ответа*
			делаем повторный запрос через некоторое время*/
		}
		
		on_notification: function(notification){
			
            var self = this;
            var channel = notification[0];
            var message = notification[1];
		},
		
		
		send_message: function(data){
			
			ajax.jsonRpc('/chess/chat/message/', 'call', data).then(function(result){
				$('#chat-form #message-text').val("");
			}).fail(function(){
				$("#window_chat").append("<p><span class='error'>Not connection with server</span></p>");
			});
		},
		
		msg_btn: function() {
			$("#message_btn").click(send_message);
			$("#chat_form").submit(function(event) {
				init_chat();
				event.preventDefault();
			});
			
			poll();
		};
	};
});