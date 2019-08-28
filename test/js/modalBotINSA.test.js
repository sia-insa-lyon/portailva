jest.dontMock('jquery');
global.window = window;
global.$ = require('jquery');

const script = require('../../static/js/src/modalBotINSA');

describe('Examining the skeleton removal when image is loaded', () => {
    beforeEach(() => {
        const divElement = document.createElement('div');
        divElement.id = 'testDiv';
        divElement.className = 'skeleton';
        document.body.appendChild(divElement);
    });

    afterEach(() => {
        document.body.removeChild(document.getElementById('testDiv'));
    });

    it('can remove animation', () => {
        script.removeSkeleton('testDiv');
        expect(document.getElementById('testDiv').className).toEqual('');
    });
});


describe.skip('Examining the generation of modal', () => {
    beforeAll(() => {
        jest.mock('jquery');
        global.$ = require('jquery');

        const divElement = document.createElement('div');
        divElement.id = 'testDiv';

        const buttonElement = document.createElement('button');
        buttonElement.addEventListener('click', script.getModal('testURL/', 1));

        divElement.appendChild(buttonElement);
        document.body.appendChild(divElement);
    });

    afterAll(() => {
        document.body.removeChild(document.getElementById('testDiv'));
    });

    it('can open modal', () => {
        global.$.ajax.mockImplementation((config) => {
            return $.jqXHR();
        });

        document.querySelector('button').click();

        expect($.ajax).toBeCalledWith({
            method: 'GET',
            url: 'testURL/',
        });
    });

    it('reset modal when closing it', () => {

    });

    it('renders modal detail view correctly', () => {

    });

    it('renders modal opening hours view correctly', () => {

    });

    it('renders modal event view correctly', () => {

    });
});
