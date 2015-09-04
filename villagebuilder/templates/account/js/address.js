
	$(document).ready(function(){
		
	
		$('#geocode-results-container').hide();
		
		//initialize page
		var mapOptions = {
           center: { lat: 39.83, lng: -98.58},
           zoom: 4
       	};
	    var mymap = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
	    var geocoder = new google.maps.Geocoder();
	    var geocodeResults = [];
	    
	    //google maps will not diplay in modal unless resize event is triggered
	    $("#full-address-modal").on("shown.bs.modal", function(e) {
	        google.maps.event.trigger(mymap, "resize");
	        mymap.setZoom(mapOptions.zoom);
	        mymap.setCenter(mapOptions.center);
	    });
	    
	    //EVENTS/////////////////////////////////////////////////////////
	    
	    //when a different result is selected, update map
	    $('#geocode-results').on("click", ".geocode-result", function() {
	    	var index = $(this).val();
	    	mymap.setCenter(geocodeResults[index].geometry.location);
    		mymap.setZoom(15);
    		mymarker = new google.maps.Marker({ map: mymap });
    		mymarker.setPosition(geocodeResults[index].geometry.location);
	    })
	    $('#button-lookup-address').click(function() {
	    	var geocoderRequest = {
                address: $('#lookup-address').val()
            }
	    	geocoder.geocode(geocoderRequest, function(results, status) {
	    		if (results.length > 0) {
	    			geocodeResults = results.slice(0,10);
	    			$('#geocode-results').html('');
	    			for (var i=0; i<geocodeResults.length; i++) {
	    				$('#geocode-results').append(
	    					'<input class="geocode-result" type="radio" value="' + i + '" ' +  
	    					(i==0 ? 'checked="checked" ' : '') + 
	    					'name="geocode-results" /> ' +
    						geocodeResults[i].formatted_address + "<br />"
   						);
	    			}	    			
		    		mymap.setCenter(results[0].geometry.location);
		    		mymap.setZoom(15);
		    		mymarker = new google.maps.Marker({ map: mymap });
		    		mymarker.setPosition(results[0].geometry.location);
		    		$('#geocode-results-container').show();
	    		} else {
	    			alert('No results found for that address.');
	    		}
	    	});
	    });
	    
	    $('#button-use-address').click(function() {
	    	prepareAndSubmitAddress();
	    });
	    
	    function prepareAndSubmitAddress() {
	    	var index = $('input[name=geocode-results]:checked').val();
	    	var add = geocodeResults[index];
	    	$('input[name=full_address]').val(add.formatted_address);
	    	$('input[name=street]').val('');
	    	$('input[name=city]').val('');
	    	$('input[name=neighborhood]').val('');
	    	var lat = parseFloat(add.geometry.location.lat()).toFixed(7);
	    	var lng = parseFloat(add.geometry.location.lng()).toFixed(7)
	    	$('input[name=latitude]').val(lat);
	    	$('input[name=longitude]').val(lng);
	    	for (var i=0; i<add.address_components.length; i++) {
		    	if ($.inArray("route", add.address_components[i].types) != -1) {
		    		$('input[name=street]').val(add.address_components[i].short_name);
	            } 
		    	if ($.inArray("neighborhood", add.address_components[i].types) != -1) {
	                $('input[name=neighborhood]').val(add.address_components[i].short_name);
	            }
	            if ($.inArray("locality", add.address_components[i].types) != -1) {
	                $('input[name=city]').val(add.address_components[i].long_name);
	            }
	            if ($.inArray("administrative_area_level_1", add.address_components[i].types) != -1) {
	                $('input[name=state]').val(add.address_components[i].short_name);
	            }
	            if ($.inArray("postal_code", add.address_components[i].types) != -1) {
	                $('input[name=zip_code]').val(add.address_components[i].short_name);
	            }
	    	}
	    	$("#address-form").submit();
	    }
	    
	}); 
    
