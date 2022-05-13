/*
Tracks the user's actions within the ebook pages (/storyboard/122/7)
Use docs/action_labels.csv as a reference to what actions we are tracking.
*/

var book_id_val = null;
var page_num_val = null;
var page_num_next_val = null;
var page_num_back_val = null;

function calculateTime() {
    const currDate = new Date();

    const dateString =
    currDate.getFullYear() + '-' +
    ('0' + (currDate.getMonth()+1)).slice(-2) + '-' +
    ('0' + currDate.getDate()).slice(-2) + " " +
    ('0' + currDate.getHours()).slice(-2) + ":" +
    ('0' + currDate.getMinutes()).slice(-2) + ":" +
    ('0' + currDate.getSeconds()).slice(-2);

    return dateString;
}

var lastAction = calculateTime();

function trackEvent(actionStart, actionStop, actionID, description) {

   $.ajax( {
       type: "POST",
       url: "/api/storyboard/action",
       data: {
           book_id:book_id_val,
           detail_description:description,
           action_key_id:actionID,
           action_start:actionStart,
           action_stop:actionStop
        },
        datatype: String
    });
}

// references story_selection/book.html
function open_book(book_id) {
    book_id_val = book_id;

    var actionTime = calculateTime();

    trackEvent(lastAction, actionTime, 0, 'User opened the book id ' + book_id_val + ' from the book dashboard.');
    lastAction = actionTime;
}

// references navbar/logged_user.html
function close_book() {
    var actionTime = calculateTime();

    trackEvent(lastAction, actionTime, 1, 'User exited the book id ' + book_id_val);
    lastAction = actionTime;
}

// references viewer.html
// !! works for png images for now
function click_page() {
    var actionTime = calculateTime();

    trackEvent(lastAction, actionTime, 2, 'User clicked on the page ' + page_num_val + ' on book id ' + book_id_val + ' (not a link, forward or backwards, textbox, etc).');
    lastAction = actionTime;
}

// ? wait until all pages have accessible links
function click_link() {
    //  var actionTime = calculateTime();
    //  trackEvent(lastAction, actionTime, 3, "User clicked a link.");
}

// references index.html
function exit_mouse_page() {
    document.addEventListener("mouseleave", (event) => {
        var actionTime = calculateTime();

        if (event.clientY <= 0 || event.clientX <= 0 || (event.clientX >= window.innerWidth || event.clientY >= window.innerHeight)) {
            trackEvent(lastAction, actionTime, 4, 'Mouse of user left the webpage on page ' + page_num_val + ' at book id ' + book_id_val);
            lastAction = actionTime;
        }
   });
}

// references index.html
function enter_mouse_page() {
    document.addEventListener("mouseenter", (event) => {
        var actionTime = calculateTime();

        if ((event.clientY > 0 && event.clientY < window.innerHeight) && (event.clientX > 0 && event.clientX < window.innerWidth)) {
            trackEvent(lastAction, actionTime, 5, 'Mouse of user re-entered the webpage on page ' + page_num_val + ' at book id ' + book_id_val)
            lastAction = actionTime;
        }
    });
}

function exit_tab() {
    document.addEventListener("visibilitychange", () => {
        var actionTime = calculateTime();

        if (document.visibilityState != "visible") {
            trackEvent(lastAction, actionTime, 6, 'User switched to another tab on book id ' + book_id_val);
            lastAction = actionTime;
        }
    });
}

function enter_tab() {
    document.addEventListener("visibilitychange", () => {
        var actionTime = calculateTime();

        if (document.visibilityState == "visible") {
            trackEvent(lastAction, actionTime, 7, 'User switched back to our webpage tab on book id ' + book_id_val);
            lastAction = actionTime;
        }
    });
}

// references viewer.html
function turn_page_forward() {
    var actionTime = calculateTime();

    trackEvent(lastAction, actionTime, 10, 'User turned forward to page ' + page_num_next_val + ' on book id ' + book_id_val);
    lastAction = actionTime;
}

// references viewer.html
function turn_page_backward() {
    var actionTime = calculateTime();

    trackEvent(lastAction, actionTime, 11, 'User turned backward to page ' + page_num_back_val + ' on book id ' + book_id_val);
    lastAction = actionTime;
}

// Work on adding MC and free response first
function user_answered_question(book_id) {

    book_id_val = book_id;
    var actionTime = calculateTime();

    trackEvent(lastAction, actionTime, 8, 'User answered a question.');
    lastAction = actionTime;

}

function change_answer_question(book_id) {

    book_id_val = book_id;
    var actionTime = calculateTime();

    trackEvent(lastAction, actionTime, 9, 'User changed answer on a question.');
    lastAction = actionTime;
}

// references quiz_fr.html
function enter_text_response(book_id) {

    book_id_val = book_id;
    var actionTime = calculateTime();

    trackEvent(lastAction, actionTime, 12, 'User entered a textbox.');
    lastAction = actionTime;
}

// references quiz_fr.html
function exit_text_response(book_id) {

    book_id_val = book_id;
    var actionTime = calculateTime();

    trackEvent(lastAction, actionTime, 13, 'User exited a textbox.');
    lastAction = actionTime;
}

window.onload = function afterWebPageLoad() {

    var bookId = document.getElementById("book_id_form");

    if (bookId != null) {
        book_id_val = bookId.book_id_name.value;
        page_num_val = bookId.page_id_name.value;
        page_num_next_val = bookId.page_next_name.value;
        page_num_back_val = bookId.page_back_name.value;

        enter_tab();
        exit_tab();
        enter_mouse_page();
        exit_mouse_page();
    }
}
