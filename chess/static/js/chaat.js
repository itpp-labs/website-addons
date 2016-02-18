(function() {
	"use strict";
	
	var ajax = require('web.ajax');
	var bus = require('bus.bus');
	
	var data = {};
	1
	var chat = {
		init_chat: function(){
			/*инициализация данных*/


			data.message = $("#message_text").val();
			send_message(data);
		},

		get_message: function(data){
			// Gets the list of messages from the server ??????
			// add messages
			$("#window_chat").append("<p><span class='user'>" + (data['user']) +
			"</span>: " + (data['message']) + "<span class='time_message'>: " + 
			(data['time']) + "</span></p>");
			
			// scroll to bottom
			$("#window_chat").each(function () {
				this.scrollTop = this.scrollHeight;
			});
		},
		
		poll: function() {
			
			/*тут что-то надо делать с модулем bus я так думаю*/
			/*вызываем функцию показать сообщение*/
			get_message(data);
		}
		
		send_message: function(data){
			
			ajax.jsonRpc('/chat/message/', 'call', data).then(function ({
				$('#chat-form #message-text').val('');
			})
			/*вытащить ник пользователя и время отправки сообщения*/
			/*отправить пакет в функцию get_messages*/
			
			
		},
		
		msg_btn: function() {
			$("#message_btn").click(send_message);
			$("#chat_form").submit(function(event) {
				init_chat();
				event.preventDefault(); // отменяем обработку 
			});
			
			poll();
		};
	};
});