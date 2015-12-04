
	
	function attachEvents() {
		$('.btn-complete-request').off();
		$('.btn-complete-request').click(function(event) {
			var requestId = this.id.replace("btn-complete-request-", "");
			var data = {
				'redirect' : '{{request.build_absolute_uri}}',
				'request_id' : requestId,
			}
			$.post("{% url 'requests:complete_request' %}", data, function(data, status) {
                if (status == 'success') {
                	$('#request-' + data.request_id).replaceWith( data.html );
                	attachEvents();
                }
			});
			event.preventDefault();
		});
		$('.btn-uncomplete-request').off();
		$('.btn-uncomplete-request').click(function(event) {
			var requestId = this.id.replace("btn-uncomplete-request-", "");
			var data = {
				'redirect' : '{{request.build_absolute_uri}}',
				'request_id' : requestId,
			}
			$.post("{% url 'requests:uncomplete_request' %}", data, function(data, status) {
                if (status == 'success') {
                	$('#request-' + data.request_id).replaceWith( data.html );
                	attachEvents();
                }
			});
			event.preventDefault();
		});
		$('.btn-edit-request').off();		//remove all existing event handlers
		$('.btn-edit-request').click(function(event) {
			var requestId = this.id.replace("btn-edit-request-", "");
			if ( $(this).html().trim() == 'Edit' ) {
				$('#view-request-' + requestId).hide();
				$('#edit-request-' + requestId).show();
				$(this).html('Cancel Edit');
			} else {
				$('#edit-request-' + requestId).hide();
				$('#view-request-' + requestId).show();
				$(this).html('Edit');
			}
			event.preventDefault();
		});
		$('.btn-show-edit-request-comment').off();
		$('.btn-show-edit-request-comment').click(function(event) {
			var commentId = this.id.replace("btn-show-edit-request-comment-", "");
			if ( $(this).html().trim() == 'Edit' ) {
				$('#view-request-comment-' + commentId).hide();
				$('#edit-request-comment-' + commentId).show();
				$(this).html('Cancel Edit');
			} else {
				$('#edit-request-comment-' + commentId).hide();
				$('#view-request-comment-' + commentId).show();
				$(this).html('Edit');
			}
			event.preventDefault();
		});
		$('.show-comments').off();
		$('.show-comments').click(function(event) {
			var requestId = this.id.replace("show-comments-for-request-", "");
			if ( $(this).html().indexOf('up') == -1 ) {
				$('#comments-for-request-' + requestId).slideDown();
				$(this).html($(this).html().replace( 'down', 'up'));
			} else {
				$('#comments-for-request-' + requestId).slideUp();
				$(this).html($(this).html().replace( 'up', 'down'));
			}
			event.preventDefault();
		});
		$('.btn-delete-request').off();
		$('.btn-delete-request').click(function(event) {
			var requestId = this.id.replace("btn-delete-request-", "");
			var data = {
				'redirect' : '{{request.build_absolute_uri}}',
				'request_id' : requestId,
			}
			$.post("{% url 'requests:delete_request' %}", data, function(data, status) {
                if (status == 'success') {
                	$('#request-' + data).html('<div class="alert alert-dismissible alert-danger">'
                			  + '<button type="button" class="close" data-dismiss="alert">X</button>'
                			  + 'Request Deleted</div>');
                }
			});
			event.preventDefault();
		});
		$('.btn-delete-request-comment').off();
		$('.btn-delete-request-comment').click(function(event) {
			var commentId = this.id.replace("btn-delete-request-comment-", "");
			var data = {
				'redirect' : '{{request.build_absolute_uri}}',
				'comment_id' : commentId,
			}
			$.post("{% url 'requests:delete_request_comment' %}", data, function(data, status) {
                if (status == 'success') {
                	$('#comment-' + data).html('<div class="alert alert-dismissible alert-danger">'
                			  + '<button type="button" class="close" data-dismiss="alert">X</button>'
                			  + 'Comment Deleted</div>');
                }
			});
			event.preventDefault();
		});
		$('.btn-edit-request-comment').off();
		$('.btn-edit-request-comment').click(function(event) {
			var commentId = this.id.replace("btn-edit-request-comment-", "");
			var data = {
				'comment_id' : commentId,
				'body' : $('#edit-request-comment-body-' + commentId).val()
			}
			if ( data.body.trim() == '' ) {
				return;
			}
			$.post("{% url 'requests:edit_request_comment' %}", data, function(data, status) {
                if (status == 'success') {
                	$('#comment-' + data.comment_id).replaceWith(data.html);
                	attachEvents();
                }
			});
			event.preventDefault();
		});
		$('.btn-add-request-comment').off();
		$('.btn-add-request-comment').click(function(event) {
			var requestId = this.id.replace("btn-add-request-comment-", "");
			var data = {
				'request_id' : requestId,
				'body' : $('#add-request-comment-body-' + requestId).val()
			}
			if ( data.body.trim() == '' ) {
				return;
			}
			$.post("{% url 'requests:post_request_comment' %}", data, function(data, status) {
                if (status == 'success') {
                	$('#new-comments-' + data.request_id).append(data.html);
                	$('#add-request-comment-body-' + data.request_id).val('')
                	attachEvents();
                }
			});
			event.preventDefault();
		});
		$('.edit-request-form').off();
		$('.edit-request-form').submit(function() {
			if ( $(this).find("textarea[name=body]").val().trim() == '' ) {
				return false;
			} 
			return true;
		})

	}
	
	
	attachEvents();
	





