/**
 * Created by mikonse on 05.11.2017.
 */

const speisekammerAPIUrl = '/api/speisekammer/';
const speisekammerUrl = '/speisekammer/';

// using jQuery
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function productIO(product, io, callbackField) {
    $.ajax({
        type: 'POST',
        url: speisekammerAPIUrl + 'products/' + product + '/item-io/',
        data: {
            item_io: io,
        },
        success: function (data) {
            $(callbackField).text(data.item_count);
        }
    });
}

function productStockIO(product, io, callbackField) {
    $.ajax({
        type: 'POST',
        url: speisekammerAPIUrl + 'products/' + product + '/stock-io/',
        data: {
            stock_io: io,
        },
        success: function (data) {
            $(callbackField).text(data.stock_count);
        }
    });
}

function dynamicProductIO(product, callbackField) {
    const input = $('#io-input-' + product);
    const inputValue = input.val();
    input.val("");
    if (inputValue != null && inputValue != "") {
        productIO(product, inputValue, callbackField);
    }
}

function dynamicProductStockIO(product, callbackField) {
    const input = $('#io-stock-input-' + product);
    const inputValue = input.val();
    input.val("");
    if (inputValue != null && inputValue != "") {
        productIO(product, inputValue, callbackField);
    }
}

function productToShoppingList(product) {
    const inputValue = $('#list-input-' + product).val();
    if (inputValue != null && inputValue != "") {
        $.ajax({
            type: 'POST',
            url: speisekammerAPIUrl + 'products/' + product + '/to-active-list/',
            data: {
                amount: inputValue,
            },
            success: function (data) {
                location.reload();
            }
        })
    }
}

function completeShoppingList(id) {
    $.ajax({
        type: 'POST',
        url: speisekammerAPIUrl + 'shopping-lists/' + id + '/complete/',
        success: function () {
            location.reload()
        }
    });
}

function completeShoppingListItem(id, checkmark) {
    $.ajax({
        type: 'POST',
        url: speisekammerAPIUrl + 'shopping-list-items/' + id + '/complete/',
        success: function (data) {
            if (data.done) {
                $(checkmark).removeClass('fa-times-circle').removeClass('text-danger').addClass('fa-check').addClass('text-success');
            } else {
                $(checkmark).removeClass('fa-check').removeClass('text-success').addClass('fa-times-circle').addClass('text-danger');
            }
        }
    });
}

function deleteShoppingList(id) {
    $.ajax({
        type: 'DELETE',
        url: speisekammerAPIUrl + 'shopping-lists/' + id + '/',
        success: function () {
            window.location.href = speisekammerUrl + "shopping-lists/";
        }
    });
}