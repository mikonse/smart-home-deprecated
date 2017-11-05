/**
 * Created by mikonse on 05.11.2017.
 */

const speisekammerAPIUrl = '/api/speisekammer/';

function productIO(product, io) {
    $.ajax({
        type: 'POST',
        url: speisekammerAPIUrl + 'products/' + product + '/item-io/',
        data: {
            item_io: io,
        },
        success: function () {
            location.reload();
        }
    });
}

function productStockIO(product, io) {
    $.ajax({
        type: 'POST',
        url: speisekammerAPIUrl + 'products/' + product + '/stock-io/',
        data: {
            stock_io: io,
        },
        success: function () {
            location.reload();
        }
    });
}

function dynamicProductIO(product) {
    const inputValue = $('#io-input-' + product).val();
    if (inputValue != null && inputValue != "") {
        productIO(product, inputValue);
    }
}

function dynamicProductStockIO(product) {
    const inputValue = $('#io-stock-input-' + product).val();
    if (inputValue != null && inputValue != "") {
        productIO(product, inputValue);
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