
	$(document).ready(function(){
		
		$('#address-link').click(function() {
			$("[name='redirect-url']").val("account:address");
			$('#main-form').submit();
		});
		$('#personal-info-link').click(function() {
			$("[name='redirect-url']").val("account:personal_info");
			$('#main-form').submit();
		});

	}); 

