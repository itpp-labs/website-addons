
	function init_chat(){
		/*инициализация данных*/
		send_message();
	}

	
	// send message
	function send_message() {
		
		/*нужно вытащить значение сообщения с текстового поля #message_text*/
		/*вытащить ник пользователя и время отправки сообщения*/
		/*сформировать пакет с сообщением формата JSON*/
		/*отправить пакет в функцию get_messages*/
		/*после завершения отправки сообщения очистить
		текстовое поле от сообщения*/
		$('#chat-form #message-text').val('');

	}
	
	
	/* Gets the list of messages from the server and 
	appends the messages to the chatbox*/
		
	function get_message(data) {
		// Gets the list of messages from the server ??????
		// add messages
		$("#window_chat").append("<p><span class='user'>" + (data['user']) +
		"</span>: " + (data['message']) + "</p>");
		
		// scroll to bottom
		$("#window_chat").each(function () {
			this.scrollTop = this.scrollHeight;
		});
		
		// wait for next
		setTimeout("get_messages()", 2000);

	}
	
	function msg_btn() {
		$("#message_btn").click(send_message);
		$("#chat_form").submit(function(event) {
			setTimeout(function() {
				init_chat();
				event.preventDefault(); // отменяем обработку соб
			}, 
			100);
		});
		
	}