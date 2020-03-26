const SKELETON_TYPE = {
    TEXT: 'text',
    TEXT_WITH_BADGE: 'textBadged',
    TEXT_WITH_THUMB: 'textThumbed',
    SHORT_TEXT: 'shortText'
};

let lastModalAssociationId = 0;

// eslint-disable-next-line no-unused-vars
function removeSkeleton(divId) {
    $('#'+divId).removeClass('skeleton');
}

/** Function to generate HTML for modal in initial state
 *
 * @param  {SKELETON_TYPE} skeletonType      Type of skeleton to generate
 * @param  {Number}        numberOfElement   Number of skeleton text element
 * @param  {String}        titleContent      (Optional) Content of h5 element
 * @return {String}                          HTML skeleton div element
 */
function getHTMLInitialSection(skeletonType, numberOfElement, titleContent=null) {
    let HTMLCode = '';

    const generateCode = (code) => {
        for (let i=0; i<numberOfElement; i++) {
            HTMLCode = HTMLCode.concat(code);
        }
    };

    if (titleContent) {
        HTMLCode = HTMLCode.concat('<h5>', titleContent, '</h5>');
    }

    switch (skeletonType) {
    case SKELETON_TYPE.SHORT_TEXT:
        generateCode('<div class="skeleton skeletonShortText"></div>');
        break;
    case SKELETON_TYPE.TEXT:
        generateCode('<div class="skeleton skeletonShortText"></div>');
        break;
    case SKELETON_TYPE.TEXT_WITH_THUMB:
        HTMLCode = HTMLCode.concat('<div class="float-right skeleton col-3 skeletonThumb"></div>');
        generateCode('<div class="skeleton skeletonText"></div>');
        break;
    case SKELETON_TYPE.TEXT_WITH_BADGE:
        generateCode('<div class="skeleton skeletonTitle"></div>');
        HTMLCode = HTMLCode.concat('<div class="skeleton skeletonBadge"></div>');
        break;
    default:
    }

    return HTMLCode;
}

function getHTMLTitleSection(name, acronym, category) {
    const $ref = $('#modal-association-title');
    $ref.empty().append(name + ' ');
    if (acronym) {
        $ref.append('<small class="text-muted">(' + acronym + ')</small>');
    }
    $ref.append(' <span class="badge badge-pill badge-secondary">' + category.name + '</span>');
}

function getHTMLDescriptionSection(description, logo) {
    const $ref = $('#modal-association-description');
    $ref.empty().append('<h5>Description</h5>');
    if (logo) {
        $ref.append('<img src="' + logo + '" alt="Logo" class="float-right col-3">');
    }

    if (description) {
        $ref.append('<p>' + description.replace(/\r\n/g, '<br/>') + '</p>');
    } else {
        $ref.append('<p><em>Non défini</em></p>');
    }
}

function getHTMLPlaceSection(name, lat, long) {
    const $ref = $('#modal-association-place');
    $ref.empty().append('<h5>Lieu</h5>');

    const contentElement = document.createElement('p');
    const $refContent = $(contentElement);

    $refContent.append('<i class="fa fa-fw fa-location-arrow"></i> ');
    if (name && lat && long) {
        $refContent.append('<a href="http://www.openstreetmap.org/?mlat=' + lat + '&mlon=' + long + '&zoom=18">' + name + '</a>');
    } else {
        $refContent.append('<em>Non défini</em>');
    }

    $ref.append($refContent);
}

function getHTMLWebsiteSection(link) {
    const $ref = $('#modal-association-website');
    $ref.empty().append('<h5>Site web</h5>');

    const contentElement = document.createElement('p');
    const $refContent = $(contentElement);

    $refContent.append('<i class="fa fa-fw fa-external-link"></i> ');
    if (link) {
        $refContent.append('<a href="' + link +'" style="word-wrap: break-word;">' + link + '</a>');
    } else {
        $refContent.append('<em>Non défini</em>');
    }

    $ref.append($refContent);
}

function getHTMLNetworkSection(facebook, twitter, instagram) {
    const $ref = $('#modal-association-network');
    $ref.empty().append('<h5>Réseaux sociaux</h5>');

    const contentElement = document.createElement('p');
    const $refContent = $(contentElement);

    $refContent.append('<i class="fa fa-fw fa-facebook-f"></i> ');
    if (facebook) {
        $refContent.append('<a href="' + facebook + '">Facebook</a><br/>');
    } else {
        $refContent.append('<em>Non défini</em><br/>');
    }
    $refContent.append('<i class="fa fa-fw fa-twitter"></i> ');
    if (twitter) {
        $refContent.append('<a href="' + twitter + '">Twitter</a><br/>');
    } else {
        $refContent.append('<em>Non défini</em><br/>');
    }
    $refContent.append('<i class="fa fa-fw fa-instagram"></i> ');
    if (instagram) {
        $refContent.append('<a href="' + instagram + '">Instagram</a>');
    } else {
        $refContent.append('<em>Non défini</em>');
    }

    $ref.append($refContent);
}

function getHTMLContactSection(mail, phone, phoneSource) {
    const $ref = $('#modal-association-contact');
    $ref.empty().append('<h5>Contact</h5>');

    const contentElement = document.createElement('p');
    const $refContent = $(contentElement);

    $refContent.append('<i class="fa fa-fw fa-envelope-o"></i> ');
    if (mail) {
        $refContent.append('<a href="mailto:' + mail +'">' + mail +'</a><br>');
    } else {
        $refContent.append('<em>Non défini</em><br>');
    }

    $refContent.append('<i class="fa fa-fw fa-phone"></i> ');
    if (phone) {
        $refContent.append('<a href="tel:' + phone +'">' + phone +'</a>');
        if (phoneSource) {            
            $refContent.append(' (' + phoneSource + ')');
        }
    } else {
        $refContent.append('<em>Non défini</em>');
    }

    $ref.append($refContent);
}

function getHTMLHoursSection(hours) {
    const formatTime = (time) => {
        return time.substring(0, time.length-3);
    };

    const formatDay = (day) => {
        const conversionTable = ['Inconnu', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'];
        return conversionTable[day];
    };

    const $ref = $('#hours');
    $ref.empty().append('<h5>Horaires de permanences</h5>');
    if (hours && hours.length>0) {
        const listElement = document.createElement('ul');
        listElement.className = 'list-group';
        const $refList = $(listElement);

        hours.map((openingHours) => {
            $refList.append('<li class="list-group-item">' + formatDay(openingHours.day) +
                            ' de ' + formatTime(openingHours.begins_at) + ' à ' + formatTime(openingHours.ends_at) + '</li>');
        });

        $ref.append($refList);
    } else {
        $ref.append('<em>Aucun horaire défini</em>');
    }
}

function getHTMLEventsSection(eventList, eventToDisplay = null) {
    const $ref = $('#events');
    $ref.empty();
    if (eventList && eventList.length>0) {
        eventList.map((event, index) => {
            const divRoot = document.createElement('div');
            divRoot.className = 'item';

            const eventLink = 'event-' + event.id;
            $(divRoot).append('<a data-toggle="collapse" data-parent="#events" ' +
                'href="#' + eventLink + '" aria-expanded="true" aria-controls="event">' +
                event.name + ' (' + event.type + ')' + '</a>');

            const divChild = document.createElement('div');
            divChild.id = eventLink;
            if (eventToDisplay) {
                if (event.id === eventToDisplay) {
                    divChild.className = 'collapse show';
                } else {
                    divChild.className = 'collapse';
                }
            } else {
                if (index === 0) {
                    divChild.className = 'collapse show';
                } else {
                    divChild.className = 'collapse';
                }
            }

            divChild.setAttribute('role', 'tabpanel');

            const $refDivChild = $(divChild);

            if (event.logo_url) {
                $refDivChild.append('<img src="' + event.logo_url + '" alt="Logo" class="float-right col-3" />');
            }
            $refDivChild.append('<p>' + event.description.replace(/\r\n/g, '<br/>') + '</p>');
            $refDivChild.append('<div class="row mb-2">');
            $refDivChild.find('div.row').append('<div class="col-md-6">');
            $refDivChild.find('div.col-md-6').append('<i class="fa fa-fw fa-calendar"></i> ' + event.begins_at + ' - ' + event.ends_at);
            $refDivChild.find('div.row').append('<div class="col-md-6">');
            $refDivChild.find('div.col-md-6:nth-child(2)').append('<i class="fa fa-fw fa-location-arrow"></i> ');

            if (event.place.name && event.place.lat && event.place.long) {
                const {lat, long, name} = event.place;
                $refDivChild.find('div.col-md-6:nth-child(2)').append('<a href="http://www.google.com/maps/place/' + lat + ',' + long + '">' + name + '</a>');
            } else {
                $refDivChild.find('div.col-md-6:nth-child(2)').append('<em>Non défini</em>');
            }

            if (event.website_url || event.facebook_url) {
                $refDivChild.append('<div class="row mb-2">');
                if (event.website_url) {
                    $refDivChild.find('div.row').last()
                        .append('<div class="col-md-6"><i class="fa fa-fw fa-link"></i> <a href="' + event.website_url + '">Page web</a>');
                }
                if (event.facebook_url) {
                    $refDivChild.find('div.row').last()
                        .append('<div class="col-md-6"><i class="fa fa-fw fa-facebook"></i> <a href="' + event.facebook_url + '">Evènement Facebook</a>');
                }
            }

            if (event.prices && event.prices.length>0) {
                $refDivChild.append('<hr/><h6><i class="fa fa-fw fa-money"></i> Tarifs de l\'évènement</h6>');
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
                $refDivChild.append($refList);
                $refDivChild.append('<br/>');
            }

            $(divRoot).append(divChild);
            $ref.append(divRoot);
        });
    } else {
        $ref.append('<em>Aucun évènement à venir.</em>');
    }
}

function resetModal() {
    $('#modal-association-title').html(getHTMLInitialSection(SKELETON_TYPE.TEXT_WITH_BADGE, 1));
    $('#modal-association-description').html(getHTMLInitialSection(SKELETON_TYPE.TEXT_WITH_THUMB, 4, 'Description'));
    $('#modal-association-place').html(getHTMLInitialSection(SKELETON_TYPE.SHORT_TEXT, 1, 'Lieu'));
    $('#modal-association-website').html(getHTMLInitialSection(SKELETON_TYPE.SHORT_TEXT, 1, 'Site web'));
    $('#modal-association-network').html(getHTMLInitialSection(SKELETON_TYPE.SHORT_TEXT, 3, 'Réseaux sociaux'));
    $('#modal-association-contact').html(getHTMLInitialSection(SKELETON_TYPE.SHORT_TEXT, 2, 'Contact'));
    $('#hours').html(getHTMLInitialSection(SKELETON_TYPE.SHORT_TEXT, 2, 'Horaires de permanences'));
    $('#events').html(getHTMLInitialSection(SKELETON_TYPE.TEXT, 3));
}

/** Function to generate modal for a specific association and open it !
 *
 * @param  {string} baseURL  URL of the endpoint to use
 * @param  {Number} assoId   ID of the association to display
 * @param  {Number} eventId  (Optional) ID of the event to show directly to user
 */
// eslint-disable-next-line no-unused-vars
function getModal(baseURL, assoId, eventId = null) {
    $.ajax({
        url: baseURL + assoId + '/',
        method: 'GET',
        beforeSend: () => {
            resetModal();
        },
        complete: () => {
            const links = $('#assoDetails div.btn-group a');
            for (let i=0; i<links.length; i++) {
                const url = links[i].href;
                const idPos = url.lastIndexOf(lastModalAssociationId);
                links[i].setAttribute('href', url.substring(0, idPos) + url.substring(idPos, url.length).replace(lastModalAssociationId, assoId));
            }
            lastModalAssociationId=assoId;
            $('#assoDetails').modal('show');

            if ( eventId ) {
                $('.nav-tabs a[href="#events"]').tab('show');
            } else {
                $('.nav-tabs a[href="#info"]').tab('show');
            }
        }
    }).done( (data) => {
        $('#modal-association-title').html(getHTMLTitleSection(data.name, data.acronym, data.category));
        $('#modal-association-description').html(getHTMLDescriptionSection(data.description, data.logo_url));
        $('#modal-association-website').html(getHTMLWebsiteSection(data.website_url));
        $('#modal-association-network').html(getHTMLNetworkSection(data.facebook_url, data.twitter_url, data.instagram_url));
        $('#modal-association-place').html(getHTMLPlaceSection(data.location.name, data.location.lat, data.location.long));
        $('#modal-association-contact').html(getHTMLContactSection(data.contact_address, data.public_phone.phone, data.public_phone.source));

        $('#hours').html(getHTMLHoursSection(data.opening_hours));
        $('#events').html(getHTMLEventsSection(data.related_events, eventId));
    }).fail( (err) => {
        $('div.modal').prepend(
            '<div class="alert alert-danger" role="alert">\n' +
            ' Une erreur est survenue, voici le détail : '+ (err.responseJSON) ? err.responseJSON.detail : 'erreur inattendue' +
                '</div>');
    });
}

// Export for test methods
if (typeof module === 'object' && module.exports) {
    module.exports = {getModal, resetModal, removeSkeleton};
}
