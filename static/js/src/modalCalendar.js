
/** Function to generate HTML for modal in initial state
 * @param  {Number}        numberOfElement   Number of skeleton text element
 * @return {String}                          HTML skeleton div element
 */
function getHTMLInitialSection(numberOfElement) {
    let HTMLCode = '';
    const generateCode = (code) => {
        for (let i=0; i<numberOfElement; i++) {
            HTMLCode = HTMLCode.concat(code);
        }
    };

    generateCode('<div class="skeleton skeletonShortText"></div>');
    return HTMLCode;
}

/**
 *  Function to display UTC date string into human language
 * @param  {String}        date             UTC Date string
 * @return {String}                         Date in format DD/MM/YYYY HH:mm
 */
function formateDate(date) {
    const d = new Date(date);
    return d.toLocaleDateString('fr-FR') + ' ' + d.toLocaleTimeString('fr-FR').substring(0, 5);
}

/** Function to display event inside the modal
 * @param  {Object}        event            Object returned by the PVA API
 */
function getHTMLEventsSection(event) {
    let title = event.name;
    if (event.type) {
        title += ' <span class="badge badge-pill badge-secondary">' + event.type.name + '</span>';
    }
    title += ' <small class="text-muted">(';
    if (event.association.acronym) {
        title += event.association.acronym;
    } else {
        title += event.association.name;
    }
    $('#modal-event-title').html('<h4>' + title + ')</small></h4>');

    const $ref = $('#modal-event-content');
    $ref.empty();

    const divRoot = document.createElement('div');
    const refRoot= $(divRoot);

    if (event.logo_url) {
        refRoot.append('<img src="' + event.logo_url + '" alt="Logo" class="float-right col-3" />');
    }

    if (event.description) {
        refRoot.append('<p>' + event.description.replace(/\r\n/g, '<br/>') + '</p>');
    } else {
        $ref.append('<p><em>Non défini</em></p>');
    }

    refRoot.append('<div class="row mb-2">');
    refRoot.find('div.row').append('<div class="col-md-6">');

    refRoot.find('div.col-md-6').append('<i class="fa fa-fw fa-calendar"></i> ' + formateDate(event.begins_at) + ' - ' + formateDate(event.ends_at));
    refRoot.find('div.row').append('<div class="col-md-6">');
    refRoot.find('div.col-md-6:nth-child(2)').append('<i class="fa fa-fw fa-location-arrow"></i> ');

    if (event.location.name && event.location.lat && event.location.long) {
        const {lat, long, name} = event.location;
        refRoot.find('div.col-md-6:nth-child(2)').append('<a href="http://www.google.com/maps/place/' + lat + ',' + long + '">' + name + '</a>');
    } else {
        refRoot.find('div.col-md-6:nth-child(2)').append('<em>Non défini</em>');
    }
    refRoot.append('<div class="row mb-2"><div class="col-12">');
    refRoot.find('div.col-12').append('<i class="fa fa-fw fa-link"></i> ');

    if (event.website_url) {
        refRoot.find('div.col-12').append('<a href="' + event.website_url + '">Page web</a>');
    } else {
        refRoot.find('div.col-12').append('<em>Non défini</em>');
    }
    $ref.append(divRoot);
}

/** Function to generate modal for a specific event and open it !
 *
 * @param  {string} baseURL  URL of the endpoint to use
 * @param  {Number} eventId  ID of the event to show directly to user
 */
// eslint-disable-next-line no-unused-vars
function getEventModal(baseURL, eventId) {
    $.ajax({
        url: baseURL + eventId + '/',
        method: 'GET',
        beforeSend: () => {
            $('#modal-event-title').html(getHTMLInitialSection(1));
            $('#modal-event-content').html(getHTMLInitialSection(3));
        },
        complete: () => {
            $('#modal-event').modal('show');
        }
    }).done( (data) => {
        $('#modal-event-content').html(getHTMLEventsSection(data));
    }).fail( (err) => {
        $('#modal-event-content').prepend(
            '<div class="alert alert-danger" role="alert">\n' +
            ' Une erreur est survenue, voici le détail : '+ (err.responseJSON && err.responseJSON.detail) ? err.responseJSON.detail : 'erreur inattendue' +
                '</div>');
    });
}

// Export for test methods
if (typeof module === 'object' && module.exports) {
    module.exports = {getEventModal};
}
