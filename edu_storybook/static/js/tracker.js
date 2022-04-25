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

function trackEvent(book_id, actionStart, actionStop, actionID, description) {

    // error with open_book() so hardcoded book_id
    // var book_id = $('#book_id').val();
   // var book_id = 122;
    
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

function open_book(book_id) {
    var actionTime = calculateTime();  
 // const book_id = document.getElementById("book_id").value;
 // console.log("Book_id=" + book_id);
  
    console.log("User opened book at book_id:" + book_id);
    trackEvent(book_id, lastAction, actionTime, 0, 'User opened the book from the book dashboard.');
    lastAction = actionTime;
}

function close_book(book_id) {
    var actionTime = calculateTime();
   // console.log("User closed book at book_id:" + book_id);
    
    document.getElementById("edustorybook-user-link")
    document.getElementById("story-selection-link")
    document.getElementById("logout-button")

    trackEvent(book_id, lastAction, actionTime, 1, 'User exited the book back to some other page.');
    lastAction = actionTime;
}

// ! fixed for png images for now
function click_page(book_id, page_num) {
    var actionTime = calculateTime();
    console.log("Click on page where book_id:" + book_id + "and page_num:" + page_num);
    trackEvent(book_id, lastAction, actionTime, 2, 'User clicked somewhere on the page (not a link, forward or backwards, textbox, etc).');
    lastAction = actionTime;
}

// ? wait until all pages have accessible links
function click_link(book_id, page_num) {
    var actionTime = calculateTime();
//  trackEvent(lastAction, actionTime, 3, "User clicked a link.");
} 

function exit_mouse_page(book_id, page_num) {
    document.addEventListener("mouseleave", (event) => {
    var actionTime = calculateTime();
    
    if (event.clientY <= 0 || event.clientX <= 0 || (event.clientX >= window.innerWidth || event.clientY >= window.innerHeight)) {
   //   console.log("I'm out");
      trackEvent(book_id, lastAction, actionTime, 4, 'Mouse of user left the webpage.')
      lastAction = actionTime;
      }
   });
}

function enter_mouse_page(book_id, page_num) {
    document.addEventListener("mouseenter", (event) => {
    var actionTime = calculateTime();

    if ((event.clientY > 0 && event.clientY < window.innerHeight) && (event.clientX > 0 && event.clientX < window.innerWidth)) {
     //   console.log("I'm in");
        trackEvent(book_id, lastAction, actionTime, 5, 'Mouse of user re-entered the webpage.')
        lastAction = actionTime;
       }
    });
}

function exit_tab(book_id) {
    document.addEventListener("visibilitychange", () => {
        var actionTime = calculateTime();
        if (document.visibilityState != "visible") {
            console.log("Tab is inactive");
            trackEvent(book_id, lastAction, actionTime, 6, 'User switched to another tab.');
            lastAction = actionTime;
        }
    });
}

function enter_tab(book_id) {
    document.addEventListener("visibilitychange", () => {
        var actionTime = calculateTime();
        if (document.visibilityState == "visible") {
            console.log("Tab is active");
            trackEvent(book_id, lastAction, actionTime, 7, 'User switched back to our webpage tab.');
            lastAction = actionTime;
        }
    });
}

function turn_page_forward(book_id, page_num) {
    var actionTime = calculateTime();
//    console.log("Print the next page");
    trackEvent(book_id, lastAction, actionTime, 10, 'User turned forward a page.');
    lastAction = actionTime;
}

function turn_page_backward(book_id, page_num) {    
    var actionTime = calculateTime();
 //   console.log("User turned page backward at " + actionTime);
    trackEvent(book_id, lastAction, actionTime, 11, 'User turned backward a page.');
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

//enter_mouse_page();
//exit_mouse_page();
