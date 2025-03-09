/***
*    Copyright (C) 2023-TODAY TechKhedut (<https://www.techkhedut.com>)
*    Part of TechKhedut. See LICENSE file for full copyright and licensing details.
****/
odoo.define('tk_website_rental_management.website_rental', function (require) {
    "use strict";
    const ajax = require('web.ajax');
    $('.geodir-js-favorite_btn, .js_add_wishlist').on('click', function(e){
        const tgClass = $(this).hasClass('liked');
        const access = $(this).data('access');
    	e.preventDefault();
        ajax.jsonRpc("/property/wishlist", 'call', {
            'toggle': tgClass,
            'access': access
        }).then(function (result){
            if(result.count){
                $('.cart-counter').text(result.count);
            }
        });
		$(this).toggleClass('liked');
	});
    $('.clear-wishlist').on('click', function (c) {
        const access = $(this).data('access');
        ajax.jsonRpc("/property/wishlist/clear", 'call', {
            'access': access
        }).then(function (result){
            console.log(result);
            if(result.count){
                $('.cart-counter').text(result.count);
            }
        });
        $(this).parent().parent().fadeOut('slow', function (c) {});
    });
    $('#sort_type').on('change', function() {
        let current_url = window.location.pathname + window.location.search;
        if(current_url.indexOf("?") >=0){
            if(current_url.indexOf("property_type=") >= 0){
                window.location.href = current_url.replace(/\bproperty_type=[0-9a-zA-Z_@.#+-]{1,50}\b/, 'property_type=' + this.value)
            }else{
                window.location.href = current_url+'&property_type='+this.value
            }
        }else{
            window.location.href = current_url+'?property_type='+this.value
        }
    });
    $('#price_type').on('change', function() {
        let current_url = window.location.pathname + window.location.search;
        if(current_url.indexOf("?") >=0){
            if(current_url.indexOf("price_order=") >= 0){
                window.location.href = current_url.replace(/\bprice_order=[0-9a-zA-Z_@.#+-]{1,50}\b/, 'price_order=' + this.value)
            }else{
                window.location.href = current_url+'&price_order='+this.value
            }
        }else{
            window.location.href = current_url+'?price_order='+this.value
        }
    });

    $('#categ').on('change', function() {
        if(this.value === 'apartments' || this.value === 'houses'){
            $('.rooms, .bathrooms').removeClass('d-none')
            $('#rooms').attr('name', 'rooms');
            $('#bathrooms').attr('name', 'bathrooms');
        }else{
            $('.rooms,.bathrooms').addClass('d-none')
            $('#rooms,#bathrooms').removeAttr('name');
        }

        if(this.value === 'apartments' || this.value === 'houses' || this.value === 'commercials'){
            $('.floor').removeClass('d-none')
             $('#floor').attr('name', 'floor');
        }
        else{
            $('.floor').addClass('d-none')
            $('#floor').removeAttr('name');
        }
        if(this.value !== 'All Categories'){
            $('.area-filter').removeClass('d-none');
        }else{
             $('.area-filter').addClass('d-none');
        }
    });

    $('.price-range').on('change', function() {
        let slider = $(".price-range").data("ionRangeSlider");
        $('#price_start').attr('name', 'price-start').val(slider.result.from);
        $('#price_end').attr('name', 'price-end').val(slider.result.to);
    });
    $('.area-range').on('change', function() {
        let slider = $(".area-range").data("ionRangeSlider");
        $('#area_start').attr('name', 'area-start').val(slider.result.from);
        $('#area_end').attr('name', 'area-end').val(slider.result.to);
    });

    $('#check-gym').on('click', function() {
         add_amt_attribute('check-gym', this, 'gym');
    });
    $('#check-wifi').on('click', function() {
        add_amt_attribute('check-wifi', this, 'wifi');
    });
    $('#check-parking').on('click', function() {
        add_amt_attribute('check-parking', this, 'parking');
    });
    $('#check-pool').on('click', function() {
        add_amt_attribute('check-pool', this, 'pool');
    });
    $('#check-security').on('click', function() {
        add_amt_attribute('check-security', this, 'security');
    });
    $('#check-laundry').on('click', function() {
        add_amt_attribute('check-laundry', this, 'laundry');
    });
    $('#check-eq-kitchen').on('click', function() {
        add_amt_attribute('check-eq-kitchen', this, 'kitchen');
    });
    $('#check-air-condition').on('click', function() {
        add_amt_attribute('check-air-condition', this, 'ac');
    });
    $('#check-semi-furnish').on('click', function() {
        add_amt_attribute('check-semi-furnish', this, 'smf');
    });
    $('#check-full-furnish').on('click', function() {
        add_amt_attribute('check-full-furnish', this, 'fuf');
    });
    $('#check-alarm').on('click', function() {
        add_amt_attribute('check-alarm', this, 'alarm');
    });
    $('#check-wc').on('click', function() {
        add_amt_attribute('check-wc', this, 'wc');
    });

    function add_amt_attribute(id, self, name){
        if (self.checked){
            $('#'+id).attr('name', name);
        }else {
            $('#'+id).removeAttr('name');
        }
    }

});