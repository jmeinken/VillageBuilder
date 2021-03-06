$(document).ready(function(){
		
	$('.add-friend').click(function(event) {
		event.preventDefault;
		var friendId = $(this).attr('id').replace("participant-","");
		redirect = window.location.href
		$('#add-friend-form-' + friendId).submit();
	});
	$('.remove-friend').click(function(event) {
		event.preventDefault;
		var friendId = $(this).attr('id').replace("participant-","");
		redirect = window.location.href
		$('#remove-friend-form-' + friendId).submit();
	});
	$('.remove-guest-friend').click(function(event) {
		event.preventDefault;
		var friendId = $(this).attr('id').replace("participant-","");
		redirect = window.location.href
		$('#remove-guest-friend-form-' + friendId).submit();
	});
	
	//load alerts when page opens
    $.get("/alerts/alerts/", function(data, status){
		if (status == 'success') {
    		$('#alert-container').html(data.html)
    		if (data.count != 0) {
    			$('#alert-count').html('<span class="highlight">' + data.count + '</span>')
    		}
    		$('.delete-alert').click(function() {
		        var alertId = $(this).attr('id').replace('delete-alert-', '')
		        postAlerts({action : 'delete_alert', alert_id : alertId})
		    });
		}
    });
    
	//reset alert count when alerts are viewed (maybe use setTimeout here)
    $('#open-alerts').click(function() {
    	if ( $('#alert-count').html() != '' ) {
    	    postAlerts({action : 'reset_count'});
    	}
    });
    
    function postAlerts(postData) {
        $.post("/alerts/alerts/", postData, function(data, status){
			if (status == 'success') {
	    		$('#alert-container').html(data.html)
	    		if (data.count != 0) {
	    			$('#alert-count').html('<span class="highlight">' + data.count + '</span>')
	    		} else {
	    			$('#alert-count').html('')
	    		}
	    		if (data.display) {
	    			$('#alert-container').parent().addClass('open');
	    		}
	    		$('.delete-alert').click(function() {
			        var alertId = $(this).attr('id').replace('delete-alert-', '')
			        postAlerts({action : 'delete_alert', alert_id : alertId})
			    });
			}
	    });
    }
    

    

	

	
}); 
