// Script - simple change change data in database of users.
// Simple interaction with tables by Javascript
// All is done by AJAX request to server to change

$(function () {
    $('.change').prop('disabled', true);
    $('.delete').prop('disabled', true);

    $('.edit').click(function () {
        $(this)
            .parents('tr')
            .find('td.notedit_id')
            .each(function () {
                var html = $(this).html();
                var input = $(
                    '<input class="editableColumnsStyle" type="text" size="10" readonly/>'
                );
                input.val(html);
                $(this).html(input);
            });

        $(this)
            .parents('tr')
            .find('td.edit_val')
            .each(function () {
                var html = $(this).html();
                var input = $(
                    '<input class="editableColumnsStyle" size="10" type="text"/>'
                );
                input.val(html);
                $(this).html(input);
            });

        $(this)
            .parents('tr')
            .find('td.notedit_val')
            .each(function () {
                var html = $(this).html();
                var input = $(
                    '<input class="editableColumnsStyle" type="text" size="10" readonly/>'
                );
                input.val(html);
                $(this).html(input);
            });

        $('.change').prop('disabled', false);
        $('.delete').prop('disabled', false);
    });

    $('.change').click(function () {
        $('.change').prop('disabled', true);
        $('.delete').prop('disabled', true);

        var change_user = [];

        $(this)
            .parents('tr')
            .find('td.notedit_id')
            .each(function () {
                var val = $(this).children('input').val();
                $(this).html(val);
                change_user.push(val);
            });

        $(this)
            .parents('tr')
            .find('td.edit_val')
            .each(function () {
                var val = $(this).children('input').val();
                $(this).html(val);
                change_user.push(val);
            });

        $(this)
            .parents('tr')
            .find('td.notedit_val')
            .each(function () {
                var val = $(this).children('input').val();
                $(this).html(val);
            });

        $.ajax({
            type: 'POST',
            url: '/change_admin',
            data: JSON.stringify(change_user),
            contentType: 'application/json, charset=utf-8',
            success: function (response) {
                alert(response.allert);
                location.reload();
            },
            error: function (error) {
                console.log(error);
            },
        });
    });

    $('.delete').click(function () {
        $('.delete').prop('disabled', true);
        $('.change').prop('disabled', true);

        var change_user = [];

        $(this)
            .parents('tr')
            .find('td.notedit_id')
            .each(function () {
                var val = $(this).children('input').val();
                $(this).html(val);
                change_user.push(val);
            });

        $(this)
            .parents('tr')
            .find('td.edit_val')
            .each(function () {
                var val = $(this).children('input').val();
                $(this).html(val);
            });

        $(this)
            .parents('tr')
            .find('td.notedit_val')
            .each(function () {
                var val = $(this).children('input').val();
                $(this).html(val);
            });

        $.ajax({
            type: 'POST',
            url: '/change_admin',
            data: JSON.stringify(change_user),
            contentType: 'application/json, charset=utf-8',
            success: function (response) {
                alert(response.allert);
                location.reload();
            },
            error: function (error) {
                console.log(error);
            },
        });
    });
});
