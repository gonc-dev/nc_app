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
    $('.department-title').on('click', function(){
        $('.department-list').toggleClass('mobile-active')
    })

    $('.filter-title').on('click', function(){
        $('.filter-form').toggleClass('mobile-active')
    })

    $('.gallery-img').on('click', function(evt){
        $('#main-product-img').attr('src', evt.target.src)
    })

    $('.account-nav').on('click', function(evt){
        console.log('triggered')
        var el = $(evt.target)
        $('.account-nav.active').removeClass('active')
        el.addClass('active')

        $('.account-section.active-account-section').removeClass('active-account-section');
        $(el.data('sectionid')).addClass('active-account-section')
    })

    // $('#main-product-img').on('mousemove', function(evt){
    //     console.log(evt)
    //     if((evt.target.width / 2) > evt.offsetX){
    //         $(evt.target).css('left',  -evt.offsetX + 'px')
    //     }else{
    //         $(evt.target).css('left',  evt.offsetX + 'px')
    //     }
    //     // $(evt.target).css('top',  evt.offsetY + 'px')
    // })
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
            console.log(data)
            $('#sku-options').empty()
            $('#product-image').attr('src', data.image);
            $('#product-name').text(data.name);
            $('#product-quantity').val(1);
            $('#product-id').val(data.id);
            if(data.sku_attribute != ""){
                $('#sku-title').text(data.sku_attribute)
                data.skus.map(function(sku, i){
                    $('#sku-options').append(`<li class='list-group-item'>
                        <input ${i == 0 ? 'checked': '' } type='radio' name='sku' value='${sku.id}'/> 
                            ${sku.name}</li>`)
                })
                
            }
            $('#product-modal').modal();
        }
    })
}



function removeFromCart(item){
    $.ajax({
        method: 'POST',
        url: '/remove-from-cart/',
        data: {
            item: item
        },
        success: function(resp){
            $('#cart-item-' + item).remove();
            $('#tax').text(resp.tax)
            $('#subtotal').text(resp.subtotal)
            $('#total').text(resp.total)
            alert('Item removed from cart successfully')
        }
    })
}

function removeFromWishlist(item){
    $.ajax({
        method: 'POST',
        url: '/remove-from-wishlist/',
        data: {
            item: item
        },
        success: function(resp){
            $('#wishlist-item-' + item).remove();
            alert('Item removed from wishlist successfully')
        }
    })
}

function confirmAddToCart(){
    addToCart($('#product-id').val(), $('input[name="sku"]:checked').val(), $('#product-quantity').val())
}

function pageAddToCart(product_id){
    addToCart(product_id, $('input[name="product_sku"]:checked').val() ,$('#quantity').val())
}

function addToCart(product, sku, quantity){
    console.log(sku)
    $.ajax({
        method: 'POST',
        url: '/add-to-cart/',
        data: {
            product: product,
            sku: sku,
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