(function(window, jQuery, iziToast, WebSocket) {
    window.ChatSocket = function(xroomName, currentUsername) {

        this.roomName = roomName;
        this.currentUsername = currentUsername;
        this.$wrapper = $wrapper;

        this.chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + this.roomName + '/');

        this.$wrapper.on(
            'keyup',
            '#js-chat-message-input',
            this.onKeyUpSendMessage.bind(this)
        );

        this.$wrapper.on(
            'click',
            '#js-chat-message-submit',
            this.onClickSendMessage.bind(this)
        );

        this.chatSocket.onmessage = this.onMessage.bind(this);

        this.chatSocket.onopen = this.onOpen.bind(this);

        this.chatSocket.onclose = this.onClose.bind(this);

        this.chatSocket.onerror = this.onError.bind(this);



        const messageLog = document.querySelector('#js-message-log');
        messageLog.scrollTop = messageLog.scrollHeight;

        const participantLog = document.querySelector('#js-participant-log');

    };

    $.extend(window.ChatSocket.prototype, {
        onKeyUpSendMessage : function (e) {
            if (e.keyCode === 13) {  // enter, return
                this.$wrapper.find('#js-chat-message-submit').click();
            }
        },
        onClickSendMessage : function(e) {
            const messageInput = this.$wrapper.find('#js-chat-message-input');
            const message = messageInput.val();
            if (message.length > 0){
                this.chatSocket.send(JSON.stringify({
                    'message': message
                }));
            }
            messageInput.val('');
        },
        onMessage : function(e) {
            const data = JSON.parse(e.data);
            const type = data['type'];

            const messageLog = this.$wrapper.find('#js-message-log');
            const participantLog = this.$wrapper.find('#js-participant-log');

            messageLog.scrollTop = messageLog.scrollHeight;

            if (type == 'on_message'){
                const message = data['body'];
                const created = data['created'];
                const avatar = data['avatar'];
                const username = data['username'];

                const element = this.$wrapper.find("js-message-empty");
                if(typeof(element) != 'undefined' && element != null){
                    element.remove();
                }

                if (username != currentUsername){
                    messageLog.append('<div class="message">'+
                            '<img class="avatar-md" src="'+ avatar +'" data-toggle="tooltip" data-placement="top" title="" alt="avatar" data-original-title="'+username+'">'+
                            '<div class="text-main">'+
                                '<div class="text-group">'+
                                    '<div class="text">'+
                                        '<p>'+ message +'</p>'+
                                    '</div>'+
                                '</div>'+
                                '<span>'+ created +'</span>'+
                            '</div>'+
                        '</div>');
                }else{
                    messageLog.append('<div class="message me">'+
                        '<div class="text-main">'+
                            '<div class="text-group me">'+
                                '<div class="text me">'+
                                    '<p>'+ message +'</p>'+
                                '</div>'+
                            '</div>'+
                            '<span><i class="ni ni-check-bold"></i> '+ created +'</span>'+
                        '</div>'+
                    '</div>');
                }

                messageLog.scrollTop = messageLog.scrollHeight;
            }

            if (type == 'on_connect'){

                const identifier = data['identifier'];
                const avatar = data['avatar'];
                const full_name = data['full_name'];

                const element = this.$wrapper.find("#js-participant-"+identifier);
                if(typeof(element) != 'undefined' && element != null){
                    element.remove();
                }

                participantLog.append('<a href="javascript:;" id="js-participant-'+ identifier +'" class="list-group-item active mb-2">'+
                      '<div class="media">'+
                        '<img alt="Image" src="'+ avatar +'" class="avatar">'+
                        '<div class="media-body ml-2">'+
                          '<div class="justify-content-between align-items-center">'+
                            '<h6 class="mb-0 text-white">'+ full_name +
                              '<span class="badge badge-success"></span>'+
                            '</h6>'+
                            '<div>'+
                              '<small>{% trans 'Online' %}</small>'+
                            '</div>'+
                          '</div>'+
                        '</div>'+
                      '</div>'+
                    '</a>');
            }

            if (type == 'on_disconnect'){
                const identifier = data['identifier'];
                const avatar = data['avatar'];
                const full_name = data['full_name'];

                const element = this.$wrapper.find("#js-participant-"+identifier);
                if(typeof(element) != 'undefined' && element != null){
                    element.remove();
                }

                participantLog.append('<a href="javascript:;" id="js-participant-'+ identifier +'" class="list-group-item active mb-2">'+
                      '<div class="media">'+
                        '<img alt="Image" src="'+ avatar +'" class="avatar">'+
                        '<div class="media-body ml-2">'+
                          '<div class="justify-content-between align-items-center">'+
                            '<h6 class="mb-0 text-white">'+ full_name +
                              '<span class="badge badge-danger"></span>'+
                            '</h6>'+
                            '<div>'+
                              '<small>{% trans 'Offline' %}</small>'+
                            '</div>'+
                          '</div>'+
                        '</div>'+
                      '</div>'+
                    '</a>');
            }
        },
        onOpen : function open(e) {
            console.log('Post WebSockets connection created');
        },
        onClose: function(e) {
            console.log('Post WebSockets closed unexpectedly');
        },
        onError: function(error) {
            console.log(`Post WebSockets error ${error.message}`);
        }
    });
})(window, jQuery, iziToast, WebSocket);