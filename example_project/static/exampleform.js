addEvent('domready', function () {
    var button = $('attach-media-button');
    MEDIAMAN.addAutoTag('id_name', 'id_tags');
    button.addEvent('click', function () {
        button.removeEvents('click');
        button.set('disabled', true);
        var selector = new MEDIAMAN.MediaSelector(
            'media-selector-container', // container for selector
            'edit-something-form', // form for object
            {
                model: 'exampleapp.something', // model of object
                tagField: 'id_name' // field, value of which should be used to
                               // search initially and prepopulate media items
            }
        );
    });
});
