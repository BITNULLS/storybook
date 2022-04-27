/*  Create a function, trackEvent(actionStart, actionStop, actionID, description) 
where:
actionStart,
actionStop, 
actionID is a key in the action_labels.csv
description is a short string that states what the user did in a consistent way 
            (e.g. user changed from page 1 to page 2).
 
This function should fire off an $.ajax(...) request to /api/storyboard/action.

In the JavaScript, add event handlers to track user movements and events,
calling on the previously defined trackEvent function.

NOTE: Not all of the features are implemented yet, and are therefore not trackable. 
Since quiz questions do not appear, yet, they do not need to be tracked, now.
Use docs/action_labels.csv as a reference to what actions we are tracking

Tracking actions for the /storyboard/122/7 or the ebook pages only

*/

var book_id_val = null;
var page_num_val = null;

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
     var book_id = $('#book_id').val();
     var book_id = 122;
    
   $.ajax( {
        type: "POST",
        url: "/api/storyboard/action",
        data: {
            book_id:book_id,
            detail_description:description,
            action_key_id:actionID,
            action_start:actionStart,
            action_stop:actionStop
        },
        success: function(result) {
            console.log("Success");
        },
        error: function(result) {
            console.log("Error");
        },
        datatype: String
    }); 
}

function open_book() {
    var actionTime = calculateTime();  
   // alert("User opened book at book_id:" + book_id);

    trackEvent(lastAction, actionTime, 0, 'User opened the book ' + book_id_val + ' from the book dashboard.');
    lastAction = actionTime;
}

function close_book() {
    var actionTime = calculateTime();

    if (book_id_val != null) {
       // alert("User closed book at book_id:" + book_id_val);
        trackEvent(lastAction, actionTime, 1, 'User exited the book ' + book_id_val + ' back to some other page.');
        lastAction = actionTime;
    }
}

// ! fixed for png images for now
function click_page(book_id, page_num) {
    var actionTime = calculateTime();

    alert("Click on page where book_id:" + book_id_val + "and page_num:" + page_num_val);
    trackEvent(lastAction, actionTime, 2, 'User clicked on the page ' + page_num_val + ' on book ' + book_id_val + ' (not a link, forward or backwards, textbox, etc).');
    lastAction = actionTime;
}

// ? wait until all pages have accessible links
function click_link(book_id, page_num) {
    var actionTime = calculateTime();
//  trackEvent(lastAction, actionTime, 3, "User clicked a link.");
} 

function exit_mouse_page(book_id, page_num) {
   /* document.addEventListener("mouseleave", (event) => {
    var actionTime = calculateTime();
    
    if (event.clientY <= 0 || event.clientX <= 0 || (event.clientX >= window.innerWidth || event.clientY >= window.innerHeight)) {
  //    alert('Mouse of user left the webpage on page ' + page_num  + 'at book ' + book_id);
      trackEvent(lastAction, actionTime, 4, 'Mouse of user left the webpage on page ' + page_num + 'at book ' + book_id);
      lastAction = actionTime;
      }
   }); */
}

function enter_mouse_page() {
   /* document.addEventListener("mouseenter", (event) => {
    var actionTime = calculateTime();

    if ((event.clientY > 0 && event.clientY < window.innerHeight) && (event.clientX > 0 && event.clientX < window.innerWidth)) {
      //  alert('Mouse of user re-entered the webpage on page ' + page_num  + 'at book ' + book_id);
        trackEvent(lastAction, actionTime, 5, 'Mouse of user re-entered the webpage on page ' + page_num_val + 'at book ' + book_id_val)
        lastAction = actionTime;
       }
    }); */
}

function exit_tab(book_id) {
    document.addEventListener("visibilitychange", () => {
        var actionTime = calculateTime();
        if (document.visibilityState != "visible") {
       //     alert("Tab is inactive");
            trackEvent(lastAction, actionTime, 6, 'User switched to another tab.');
            lastAction = actionTime;
        }
    });
}

function enter_tab(book_id) {
    document.addEventListener("visibilitychange", () => {
        var actionTime = calculateTime();
        if (document.visibilityState == "visible") {
         //   alert("Tab is active");
            trackEvent(lastAction, actionTime, 7, 'User switched back to our webpage tab on book ' + book_id);
            lastAction = actionTime;
        }
    });
}

function turn_page_forward(book_id, page_num) {
    var actionTime = calculateTime();
    alert("Print the next page");
    trackEvent(lastAction, actionTime, 10, 'User turned forward at page ' + page_num + 'on book ' + book_id);
    lastAction = actionTime;
}

// ?
function turn_page_backward(book_id, page_num) {    
    var actionTime = calculateTime();
 //   alert("User turned page backward at " + actionTime);
    trackEvent(lastAction, actionTime, 11, 'User turned backward at page ' + page_num + 'on book ' + book_id);
    lastAction = actionTime;
}

// Work on adding MC and free response first
function answered_question() {
//    trackEvent(lastAction, dateString, 8, '');
}
function change_answer_question() {
//    trackEvent(lastAction, dateString, 9, '');
}
function enter_text_response() {
//    trackEvent(lastAction, dateString, 12, '');
}
function exit_text_response() {
//    trackEvent(lastAction, dateString, 13, '');
}


window.onload = function afterWebPageLoad() {

    var bookId = document.getElementById("book_id_form");

    if (bookId != null) {
        book_id_val = bookId.book_id_name.value;
        page_num_val = bookId.page_id_name.value;
    }
}
