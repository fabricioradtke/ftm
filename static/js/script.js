//JS

$(function() {

    // Popstate event
    window.addEventListener('popstate', function() {
        loadPage(location.href, false, false);
    });
/*
    // Menu
    $(document).on('click', 'a[data-load="menu"]', function(e) {
        e.preventDefault();

        var item = $(this).parent('li');
        var href = $(this).attr('href');

        loadPage(href, true, false, function() {
            item.addClass('active');
        });
    });

    // Links
    $(document).on('click', 'a[data-load="inner"]', function(e) {
        e.preventDefault();

        var href = $(this).attr('href');

        loadPage(href, true, false);
    });
*/
    // Search
    $(document).on('submit', '#search form', function(e) {
        e.preventDefault();

        var input = $(this).find('input');
        var value = input.val();
        var href  = '/search/' + value + '/'; // $(this).attr('action')

        if (value)
            loadPage(href, true, false, function() {
                input.val( value );
            });
    });

    // Submit on change
    $(document).on('change', '.submit-change', function() {
        $(this).submit();
    });
});

// Load page
function loadPage(href, add_history, append, callback) {

    var $loading = $('#loading');

    $.ajax(href, {
        beforeSend: function() {
            $loading.show();
        },
        success: function(html) {
            console.log('Sucesso');
            $loading.hide();

            var $html = $(html);

            if (append) {
               $('#search-list').append( $html.find('#search-list>*') );
            }
            else {
                $('#main').scrollTop(0);
                $('#search input').val('');
                $('#menu li').removeClass('active');

                $('#main').replaceWith( $html.filter('#main') );
            }

            $('.script').replaceWith( $html.filter('.script') );

            var title = $html.filter('title').text();
            document.title = title;

            if (window.history && window.history.pushState && add_history)
                window.history.pushState({is_mine:true}, title, href);

            if (callback) callback();
        },
        error: function(jqXHR, text_status) {
            console.log('Erro', jqXHR, text_status);
            $loading.hide();
            UIkit.notify('Ocorreu um erro (' + jqXHR.statusText + ').', {status:'danger'});
        }
    });
}

// Pagination
function pagination(page, total_pages) {

    var working = false;

    $('#main').on('scroll', function() {

        if ( $(this).scrollTop() + $(this).height() >= $('#content').height() && page < total_pages && !working ) {

            working  = true;
            var next = page + 1;

            setTimeout(function() {

                loadPage('?p=' + next, false, true, function() {
                    page++;
                    working = false;
                });

            }, 500);
        }
    });
}
