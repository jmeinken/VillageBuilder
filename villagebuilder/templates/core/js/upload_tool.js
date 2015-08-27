{% comment %}

This code expects some JS variables to already be set:

imageUploadUrl: the destination url to pass image data to

dataToAccompanyImageUpload: a JS object containing any data to pass together with the image upload

updatePageAfterImageUpload(data): a function to run after the image is successfully uploaded

defaultImage 


{% endcomment %}




	$(document).ready(function(){
	
		if (typeof defaultImage !== 'undefined') {
	    	$('#image').attr("src",defaultImage);
	    }
	
		var api  // Jcrop api
	    var $progressBar = $('#progressBar')
	    //options
	    var options = {
	        fileInputs: ['#file'],
	        canvases: {
	            image: {
	                'object': '#medium'
	            },
	            thumb: {
	                'object': '#small'
	            }
			},
	        dragDrops: ['#dragDrop'],
	        afterPick: function () {
	            this.setSelect([0, 0, 400, 300])  // initial selection
	        },
	        beforePick: function (img) {
	            if (img) {//valid file
	                if (img.width < 300 || img.height < 300) {
	                    alert('The image width and height must be over or equal to 300!')
	                    return true  // ignore this img
	                }
	            }
	            else {// invalid file
	                alert('Invalid file!')
	            }
	        },
	        aspectRatio: 1 / 1,
	        minSize: [150, 150],
	        boxWidth: 400,
	        boxHeight: 400
	    }
	    $('#image').Jcrop(options, function () {
	        api = this;
	        this.setSelect([50, 38, 300, 225]);
	        //api.drawInCanvas($('#medium')[0])
	    })
	    
   
	    $('#upload').click(function() {
	        if (!api) {
	            return
	        }
	        if (!api.isSelected()) {
	            alert('No selection!')
	            return
	        }
	        $progressBar.find('div').width(0)
	        //sources
	        var sources = [
	            {
	                key: 'image', // key in options.canvases
	                format: 'image/png' // default = 'image/jpeg'
	            },
	            {
	                key: 'thumb', // key in options.canvases
	                format: 'image/png' // default = 'image/jpeg'
	            },
	        ]
	        //settings
	        var settings = {
	            url: imageUploadUrl,
	            data: dataToAccompanyImageUpload,
	            onprogress: function (evt) { // function for xhr.upload.onprogress
	                if (evt.lengthComputable) {
	                    progress(evt.loaded / evt.total, $progressBar)
	                }
	            },
	            success: updatePageAfterImageUpload,
	            error: function ( jqXHR, textStatus, errorThrown ) {
	                alert(errorThrown + ' ' + textStatus)
	            }
	        }
	        api.upload(sources, settings)
	    });


	    function progress(percent, $element) {
	        var progressBarWidth = percent * $element.width();
	        $element.find('div').animate({ width: progressBarWidth }, 50).html(Math.round(percent * 100) + "%&nbsp;");
	    }

	});
