
function addVideoToContainer(video){
    var title = video.text();
    var url = video.attr('href');
    if ( title != "" && url !== undefined ){
        jQuery.ajax({type: 'POST',
                        url: '@@add-video-to-context',
                        async : false,
                        data: {'title':title,
                               'url':url},
                        success: function(results){
                            // XXX: Do we need to do something with the results ?
                                }
                    });
    }
}

if(jQuery) (function($){

    $.extend($.fn, {
        contentTreeAddVideos: function() {
            $(".ui-droppable > li > a").each(function () {
                addVideoToContainer($(this));
                removeVideoFromDroppable($(this));
            });

            $(this).contentTreeCancel();
            window.location.reload();
        }
    });

})(jQuery);
