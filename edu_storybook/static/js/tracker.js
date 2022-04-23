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

function trackEvent(actionStart, actionStop, actionID, description) {

    // error with open_book() so hardcoded book_id
    // var book_id = $('#book_id').val();
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
//  console.log("User opened book");
    trackEvent(lastAction, actionTime, 0, 'User opened the book from the book dashboard.');
    lastAction = actionTime;
}

function close_book() {
    var actionTime = calculateTime();
//    console.log("User closed book");
    trackEvent(lastAction, actionTime, 1, 'User exited the book back to some other page.');
    lastAction = actionTime;
}

// ! fixed for png images for now
function click_page() {
    var actionTime = calculateTime();
 //   console.log("Click on page");
    trackEvent(lastAction, actionTime, 2, 'User clicked somewhere on the page (not a link, forward or backwards, textbox, etc).');
    lastAction = actionTime;
}

// ? wait until all pages have accessible links
function click_link() {
    var actionTime = calculateTime();
//  trackEvent(lastAction, actionTime, 3, "User clicked a link.");
} 

function exit_mouse_page() {
    document.addEventListener("mouseleave", (event) => {
    var actionTime = calculateTime();
    
    if (event.clientY <= 0 || event.clientX <= 0 || (event.clientX >= window.innerWidth || event.clientY >= window.innerHeight)) {
   //   console.log("I'm out");
      trackEvent(lastAction, actionTime, 4, 'Mouse of user left the webpage.')
      lastAction = actionTime;
      }
   });
}

function enter_mouse_page() {
    document.addEventListener("mouseenter", (event) => {
    var actionTime = calculateTime();

    if ((event.clientY > 0 && event.clientY < window.innerHeight) && (event.clientX > 0 && event.clientX < window.innerWidth)) {
     //   console.log("I'm in");
        trackEvent(lastAction, actionTime, 5, 'Mouse of user re-entered the webpage.')
        lastAction = actionTime;
       }
    });
}

function exit_tab() {
    document.addEventListener("visibilitychange", () => {
        var actionTime = calculateTime();
        if (document.visibilityState != "visible") {
      //      console.log("Tab is inactive");
            trackEvent(lastAction, actionTime, 6, 'User switched to another tab.');
            lastAction = actionTime;
        }
    });
}

function enter_tab() {
    document.addEventListener("visibilitychange", () => {
        var actionTime = calculateTime();
        if (document.visibilityState == "visible") {
   //         console.log("Tab is active");
            trackEvent(lastAction, actionTime, 7, 'User switched back to our webpage tab.');
            lastAction = actionTime;
        }
    });
}

function turn_page_forward() {
    var actionTime = calculateTime();
    trackEvent(lastAction, actionTime, 10, 'User turned forward a page.');
    lastAction = actionTime;
}

function turn_page_backward() {    
    var actionTime = calculateTime();
  //  console.log("User turned page backward at " + actionTime);
    trackEvent(lastAction, actionTime, 11, 'User turned backward a page.');
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

//enter_tab();
//exit_tab();
//enter_mouse_page();
//exit_mouse_page();
