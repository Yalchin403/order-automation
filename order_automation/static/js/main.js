(function($) {

	"use strict";


  // Form
	var contactForm = function() {
		if ($('#contactForm').length > 0 ) {
			$( "#contactForm" ).validate( {
				rules: {
					name: "required",
					surname: "required",
					phone: "required",
					subject: "required",
					email: {
						required: true,
						email: true
					},
					link: "required"
				},
				messages: {
					name: "Please enter your name",
					subject: "Please enter your subject",
					email: "Please enter a valid email address",
					surname: "Please enter your surname",
					link: "Please enter the link",
					phone: "Please enter your phone number"
				},
				/* submit via ajax */

				submitHandler: function(form) {
					var $submit = $('.submitting'),
						waitText = 'Submitting...';

					$.ajax({

				      type: "POST",
				      url: "/order/",
				      data: $(form).serialize(),

				      beforeSend: function() {
				      	$submit.css('display', 'block').text(waitText);
				      },

				      success: function(msg, textStatus, xhr) {
		               if (xhr.status == 200) {
		               	$('#form-message-warning').hide();
				            setTimeout(function(){
		               		$('#contactForm').fadeIn();
		               	}, 1000);
				            setTimeout(function(){
				               $('#form-message-success').fadeIn();
		               	}, 1400);

		               	setTimeout(function(){
				               $('#form-message-success').fadeOut();
		               	}, 8000);

		               	setTimeout(function(){
				               $submit.css('display', 'none').text(waitText);
		               	}, 1400);

		               	setTimeout(function(){
		               		$( '#contactForm' ).each(function(){
											    this.reset();
											});
		               	}, 1400);

			            } else {
			               $('#form-message-warning').html(msg);
				            $('#form-message-warning').fadeIn();
				            $submit.css('display', 'none');
			            }
				      },
				      error: function(msg) {
				      	$('#form-message-warning').html(msg.responseText);
				         $('#form-message-warning').fadeIn();
				         $submit.css('display', 'none');
				      }
			      });    		
		  		} // end submitHandler

			});
		}
	};
	contactForm();

})(jQuery);
