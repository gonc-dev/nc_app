var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

function dismissAlert(el){
    $(el).parent().remove();
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function search(element, results){
    if($('#' + element).length > 0){
        $('#' + element).on('change keyup paste', function(){
            var input = $('#' + element).val();
            if(input.length > 2){
                $.ajax({
                    'method': 'GET',
                    'url': '/search',
                    'data': {'text': input},
                    'success': function(data){
                        console.log(data.results)
                        $('#' + results).empty()
                        data.results.map(function(result){
                            $('#' + results).append('<div><a href="'+ result.link +'">'+ result.name +'</a></div>')
                        })
                    }
                })
            }else{
                $('#' + results).empty()
            }
        })
    }
}


$(document).ready(function(){
    search('search', 'search-results')
    search('nav-search', 'nav-search-results')
})


function addToWishlist(product){
    $.ajax({
        method: 'POST',
        url: '/add-to-wishlist/',
        data: {
            product: product
        },
        success: function(res){
            console.log(res)
        }
    })
}


function increment(idx){
    var current = $('#' + idx).val();
    $('#' + idx).val(parseInt(current) + 1)
}

function decrement(idx){
    var current = $('#' + idx).val();
    if(current == 1){
        return;
    }
    $('#' + idx).val(parseInt(current) - 1)
}

function openAddToCart(product){
    //raise overlay
    $.ajax({
        method: 'GET',
        url: '/api/product/' + product + '/',
        success: function(data){
            $('#product-image').attr('src', data.image);
            $('#product-name').text(data.name);
            $('#product-quantity').val(1);
            $('#product-id').val(data.id);
            $('#product-modal').modal();
        }
    })
}

function confirmAddToCart(){
    addToCart($('#product-id').val(), $('#product-quantity').val())
}

function pageAddToCart(product_id){
    addToCart(product_id, $('#quantity').val())
}

function addToCart(product, quantity){

    $.ajax({
        method: 'POST',
        url: '/add-to-cart/',
        data: {
            product: product,
            quantity: quantity
            
        },
        success: function(res){
            $('#product-modal').modal('hide');

        }
    })
}

function revealNavSearch(){
    $('#nav-search').toggleClass('active');
    $('#nav-search').focus();
    if(!$('#nav-search').hasClass('active')){
        $('#nav-search').blur();
        $('#nav-search').val('');
        $('#nav-search-results').empty();
    }

}