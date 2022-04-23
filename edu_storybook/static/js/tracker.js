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

function trackEvent(actionStart, actionStop, actionID, description) {

    var book_id = $('#book_id').val();
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

// ? not working
function open_book() {
    var actionTime = calculateTime();
    console.log("User opened book");
    trackEvent(actionTime, actionTime, 0, 'User opened the book from the book dashboard.');
}

// ? How to see if user closed book
function close_book() {
    var actionTime = calculateTime();
//    trackEvent(actionTime, actionTime, 1, '');
}

function click_page() {
    var actionTime = calculateTime();
    console.log("Click on page");
    trackEvent(actionTime, actionTime, 2, 'User clicked somewhere on the page (not a link, forward or backwards, textbox, etc).');
}

/* wait until all pages have accessible links
function click_link() {
    var actionTime = calculateTime();
      //  trackEvent(actionTime, actionTime, 3, "User clicked a link.");
} */


// Fix exit
function exit_mouse_page() {
    document.addEventListener("mouseleave", () => {
    var actionTime = calculateTime();
   // trackEvent(actionTime, actionTime, 4, 'Mouse of user left the webpage.')
    setTimeout(function() {
        console.log("BYE")
    }, 3000);
}
);
}

// Fix enter
function enter_mouse_page() {
    document.addEventListener("mouseenter", () => {
    var actionTime = calculateTime();
    setTimeout(function() {
     //   console.log("HELLO")
    }, 3000)
}
  //  trackEvent(actionTime, actionTime, 5, '');
)
}

//done
function exit_tab() {
    document.addEventListener("visibilitychange", () => {
        var actionTime = calculateTime();
        if (document.visibilityState != "visible") {
            console.log("Tab is inactive");
//          trackEvent(actionTime, actionTime, 7, '');
        }
    })
}

//done
function enter_tab() {
    document.addEventListener("visibilitychange", () => {
        var actionTime = calculateTime();
        if (document.visibilityState == "visible") {
            console.log("Tab is active");
//          trackEvent(actionTime, actionTime, 7, '');
        }
    })
}

//done
function turn_page_forward() {
    var actionTime = calculateTime();
    console.log("User turned page forward at " + actionTime);
    trackEvent(actionTime, actionTime, 10, 'User turned forward a page.');
}

// done
function turn_page_backward() {    
    var actionTime = calculateTime();
    console.log("User turned page backward at " + actionTime);
    trackEvent(actionTime, actionTime, 11, 'User turned backward a page.');
}



// Work on adding MC and free response first
function answered_question() {
//    trackEvent(dateString, dateString, 8, '');

}
function change_answer_question() {
//    trackEvent(dateString, dateString, 9, '');

}
function enter_text_response() {
//    trackEvent(dateString, dateString, 12, '');

}
function exit_text_response() {
//    trackEvent(dateString, dateString, 13, '');

}

enter_tab();
exit_tab();
enter_mouse_page();
exit_mouse_page();