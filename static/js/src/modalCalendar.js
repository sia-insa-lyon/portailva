
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
        if (event.type.color) {
            title += ' <span class="badge badge-pill" style="color: #fff; background-color: ' + event.type.color + '">' + event.type.name + '</span>';
        } else {
            title += ' <span class="badge badge-pill badge-secondary">' + event.type.name + '</span>';
        }
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
    const $refRoot= $(divRoot);

    if (event.logo_url) {
        $refRoot.append('<img src="' + event.logo_url + '" alt="Logo" class="float-right col-3" />');
    }

    if (event.description) {
        $refRoot.append('<p>' + event.description.replace(/\r\n/g, '<br/>') + '</p>');
    } else {
        $ref.append('<p><em>Non défini</em></p>');
    }

    $refRoot.append('<div class="row mb-2">');
    $refRoot.find('div.row').append('<div class="col-md-6">');

    $refRoot.find('div.col-md-6').append('<i class="fa fa-fw fa-calendar"></i> ' + formateDate(event.begins_at) + ' - ' + formateDate(event.ends_at));
    $refRoot.find('div.row').append('<div class="col-md-6">');
    $refRoot.find('div.col-md-6:nth-child(2)').append('<i class="fa fa-fw fa-location-arrow"></i> ');

    if (event.location.name && event.location.lat && event.location.long) {
        const {lat, long, name} = event.location;
        $refRoot.find('div.col-md-6:nth-child(2)').append('<a href="http://www.google.com/maps/place/' + lat + ',' + long + '">' + name + '</a>');
    } else {
        $refRoot.find('div.col-md-6:nth-child(2)').append('<em>Non défini</em>');
    }

    if (event.website_url || event.facebook_url) {
        $refRoot.append('<div class="row mb-2">');
        if (event.website_url) {
            $refRoot.find('div.row').last()
                .append('<div class="col-md-6"><i class="fa fa-fw fa-link"></i> <a href="' + event.website_url + '">Page web</a>');
        }
        if (event.facebook_url) {
            $refRoot.find('div.row').last()
                .append('<div class="col-md-6"><i class="fa fa-fw fa-facebook"></i> <a href="' + event.facebook_url + '">Evènement Facebook</a>');
        }
    }

    if (event.prices && event.prices.length>0) {
        $refRoot.append('<hr/><h6><i class="fa fa-fw fa-money"></i> Tarifs de l\'évènement</h6>');
        const listElement = document.createElement('ul');
        listElement.className = 'list-group';
        const $refList = $(listElement);

        event.prices.map((priceElement) => {
            $refList.append('<li class="list-group-item list-group-item-action flex-column">' +
                                '<div class="row justify-content-between align-items-center">' +
                                    '<div class="col-md-6"><strong>' + priceElement.name + '</strong></div>' +
                                    '<div class="col-md-6">'
                                    + (priceElement.price && !priceElement.is_variable ? ('<strong>' + priceElement.price + ' €</strong>') : '')
                                    + (priceElement.is_variable ? 'Prix libre' : '')
                                    + (priceElement.is_va ? ' - (Tarif VA)' : '') +
                                    '</div>' +
                                '</div>' +
                            '</li>');
        });
        $refRoot.append($refList);
        $refRoot.append('<br/>');
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
