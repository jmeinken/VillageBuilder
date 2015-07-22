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
	
	//load alerts when page opens
    $.get("/alerts/alerts", function(data, status){
		if (status == 'success') {
    		$('#alert-container').html(data.html)
    		if (data.count != 0) {
    			$('#alert-count').html('[' + data.count + ']')
    		}
		}
    });
    
	//reset alert count when alerts are viewed (maybe use setTimeout here)
    $('#open-alerts').click(function() {
    	setTimeout(function() {
    		postAlerts({action : 'reset_count'});
    	}, 10000);
    });
    
    function postAlerts(postData) {
        $.post("/alerts/alerts/", postData, function(data, status){
			if (status == 'success') {
	    		$('#alert-container').html(data.html)
	    		if (data.count != 0) {
	    			$('#alert-count').html('[' + data.count + ']')
	    		} else {
	    			$('#alert-count').html('')
	    		}
	    		$('.delete-alert').click(function() {
			        var alertId = $(this).attr('id').replace('delete-alert-', '')
			        postAlerts({action : 'delete_alert', alert_id : alertId})
			    });
			}
	    });
    }
    

    

	

	
}); 