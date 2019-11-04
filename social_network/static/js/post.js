(function(window, jQuery, WebSocket) {
    window.PostSocket = function($wrapper) {

        this.$wrapper = $wrapper;
        this.chatSocket = new WebSocket('ws://' + window.location.host + '/ws/post/notifications/');

        this.chatSocket.onmessage = this.onMessage.bind(this);

        this.chatSocket.onopen = this.onOpen.bind(this);

        this.chatSocket.onclose = this.onClose.bind(this);

        this.chatSocket.onerror = this.onError.bind(this);

        this.$wrapper.on(
            'keyup',
            '#js-comment-input',
            this.onKeyUpSendMessage.bind(this)
        );

        this.$wrapper.on(
            'click',
            '#js-comment-submit',
            this.onClickSendMessage.bind(this)
        );

        this.$wrapper.on(
            'click',
            '.js-like-comment',
            this.onClickLikeComment.bind(this)
        );

        this.$wrapper.on(
            'click',
            '.js-like-post',
            this.onClickLikePost.bind(this)
        );
    };

    $.extend(window.PostSocket.prototype, {
        onClickLikePost : function(e) {
            this.chatSocket.send(JSON.stringify({
                'action': 'like_post',
                'post_pk': $(e.currentTarget).data('post')
            }));
        },
        onClickLikeComment : function (e) {
            this.chatSocket.send(JSON.stringify({
                'action': 'like_comment',
                'comment_pk': $(e.currentTarget).data('comment')
            }));
        },
        onKeyUpSendMessage : function (e) {
            if (e.keyCode === 13) {  // enter, return
                $(e.currentTarget).parents('.media').find('#js-comment-submit').click();
            }
        },
        onClickSendMessage : function(e) {
            const messageInput = $(e.currentTarget).parents('.media').find('#js-comment-input');
            const message = messageInput.val();
            if (message.length > 0){
                this.chatSocket.send(JSON.stringify({
                    'action': 'create_comment',
                    'message': message,
                    'post_pk': messageInput.data('post')
                }));
            }
            messageInput.val('');
        },
        onMessage : function(e) {
            const data = JSON.parse(e.data);
            const action = data['action'];
            const post_pk = data['post_pk'];

            $currentWrapper = this.$wrapper.find('#js-post-'+ post_pk +'-content');

            if ($currentWrapper.length == 0){
                return;
            }


            this.commentLog = $currentWrapper.find('#js-comment-log');

            if (action == 'create_comment'){

                const message = data['body'];
                const created = data['created'];
                const avatar = data['avatar'];
                const likes = data['comment_likes'];
                const full_name = data['full_name'];
                const comment_pk = data['comment_pk'];

                this.commentLog.append('<div class="media media-comment" id="js-comment-'+comment_pk+'">'+
                    '<img alt="Image placeholder" class="media-comment-avatar rounded-circle"'+
                         'src="'+ avatar +'">'+
                    '<div class="media-body">'+
                        '<div class="media-comment-text">'+
                            '<h6 class="h5 mt-0">'+ full_name +'</h6>'+
                            '<p class="text-sm lh-160">'+ message +'</p>'+
                            '<div class="icon-actions">'+
                                '<a href="javascript:;" data-comment="'+comment_pk+'" class="like js-like-comment">'+
                                    '<i class="ni ni-like-2 mr-1"></i>'+
                                    '<span id="js-comment-likes-number-'+ comment_pk +'" class="text-muted">'+ likes +'</span>'+
                                '</a>'+
                            '</div>'+
                        '</div>'+
                    '</div>'+
                '</div>');

                $currentWrapper.find('#js-post-comments-number').text(data['post_comments']);
            }

            if (action == 'like_comment'){
                const comment_likes = data['comment_likes'];
                const comment_pk = data['comment_pk'];

                const commentLikesEl = $currentWrapper.find('#js-comment-likes-number-' + comment_pk);
                commentLikesEl.text(comment_likes);
            }

            if (action == 'like_post'){
                const post_likes = data['post_likes'];
                const postLikesEl = $currentWrapper.find('#js-post-likes-number');
                postLikesEl.text(post_likes);
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
})(window, jQuery, WebSocket);