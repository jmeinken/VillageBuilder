$(document).ready(function(){
		

	
	//load messages when page opens
    $.get("/pm/message_list", function(data, status){
		if (status == 'success') {
    		$('#message-container').html(data.html)
    		if (data.count != 0) {
    			$('#message-count').html('<span class="highlight">' + data.count + '</span>')
    		}
		}
    });
    

    

    

	

	
}); 
