

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
	    	$('#shared-street').html($('#id_street').val());
	    	if ($('#id_neighborhood').val() != '') {
	    		$('#shared-neighborhood').html($('#id_neighborhood').val());
	    	}  else  {
	    		$('#shared-neighborhood').html($('#id_city').val());
	    	}
	    	$('#shared-email').html($('#id_email').val());
	    	$('#shared-phone').html($('#id_phone_number').val());
	    	$('#shared-phone-type').html( '(' + $('#id_phone_type').val() + ')' );
	    	if ( $('#id_share_email').is(':checked') ) {
	    		$('#shared-email-show').show();
	    	} else {
	    		$('#shared-email-show').hide();
	    	}
	    	if ( $('#id_share_phone').is(':checked') ) {
	    		$('#shared-phone-show').show();
	    	} else {
	    		$('#shared-phone-show').hide();
	    	}
	    }
	    
	    $('#personal-info-form :input').on("change keyup paste", function() {
	    	updateSharedView();
	    }).trigger("change");
	    
	    $('#id_share_phone').change(function() {
	    	if ( $(this).is(':checked') ) {
	    		$('#phone-info').slideDown();
	    	} else {
	    		$('#phone-info').hide();
	    	}
	    }).trigger("change");
	    
	    $('#personal-info-form :input').on("change keyup paste", function() {
	    	updateSharedView();
	    }).trigger("change");
	    
	    $('#id_share_phone').change(function() {
	    	if ( $(this).is(':checked') ) {
	    		$('#phone-info').slideDown();
	    	} else {
	    		$('#phone-info').hide();
	    	}
	    }).trigger("change");
	    
	});