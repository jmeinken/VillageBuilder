

	function updatePageAfterImageUpload(data) {
		console.log(data)
		$('#id_image').val(data.image.file);
		$(".current-user-pic").attr("src", data.image.path);
		$("#shared-user-pic").attr("src", data.image.path);
	}
	
	var dataToAccompanyImageUpload = {'member_id': '{{ current.member.id }}'}
	var imageUploadUrl = '{% url 'account:upload_image' %}'


	$(document).ready(function(){
		
		$('#name-edit-btn, #name-close-btn').click(function() {
			$('#name-view').toggle();
			$('#name-edit').toggle();
			return false;
		});
		$('#email-edit-btn, #email-close-btn').click(function() {
			$('#email-view').toggle();
			$('#email-edit').toggle();
			return false;
		});
		$('#password-edit-btn, #password-close-btn').click(function() {
			$('#password-view').toggle();
			$('#password-edit').toggle();
			return false;
		});
		$('#privacy-edit-btn, #privacy-close-btn').click(function() {
			$('#privacy-view').toggle();
			$('#privacy-edit').toggle();
			return false;
		});
		$('#phone-edit-btn, #phone-close-btn').click(function() {
			$('#phone-view').toggle();
			$('#phone-edit').toggle();
			return false;
		});
		$('#display-address-edit-btn, #display-address-close-btn').click(function() {
			$('#display-address-view').toggle();
			$('#display-address-edit').toggle();
			return false;
		});
		$('#account-status-edit-btn, #account-status-close-btn').click(function() {
			$('#account-status-view').toggle();
			$('#account-status-edit').toggle();
			return false;
		}); 
		
	}); 


