

	function updatePageAfterImageUpload(data) {
		console.log(data)
	   	$('#id_image').val(data.image.file);
	   	$('#id_thumb').val(data.thumb.file);
	   	$("#user-pic").attr("src", data.image.path);
	   	$("#shared-user-pic").attr("src", data.image.path);
	}
	
	var dataToAccompanyImageUpload = {}
	
	var imageUploadUrl = '{% url 'account:upload_image' %}'


	$(document).ready(function(){

		function updateSharedView() {
	    	$('#shared-first-name').html($('#id_first_name').val());
	    	$('#shared-last-name').html($('#id_last_name').val());
	    	if ( $('#id_share_street').is(':checked') ) {
	    		$('#shared-street').html($('#id_street').val());
	    	} else {
	    	    $('#shared-street').html('');
	    	}
	    	if ($('#id_neighborhood').val() != '') {
	    		$('#shared-neighborhood').html($('#id_neighborhood').val());
	    	}  else  {
	    		$('#shared-neighborhood').html($('#id_city').val());
	    	}
	    	$('#shared-email').html($('#id_email').val());
	    	if ( $('#id_share_email').is(':checked') ) {
	    		$('#shared-email-show').show();
	    	} else {
	    		$('#shared-email-show').hide();
	    	}
	    	if ( !$('#id_share_email').is(':checked') ) {
	    	    $('#nothing-shared-show').show();
	    	} else {
	    	    $('#nothing-shared-show').hide();
	    	}
	    }
	    
	    $('#personal-info-form :input').on("change keyup paste", function() {
	    	updateSharedView();
	    }).trigger("change");
	    
	    $('#personal-info-form :input').on("change keyup paste", function() {
	    	updateSharedView();
	    }).trigger("change");
	    
	    
	});
