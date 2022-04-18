/**
 * main.js
 * Main JavaScript file for the edu_storybook project.
 */

/**
 * Verify if two input text fields match.
 * @param   input   Input 1.
 * @param   compare Input 2.
 * @returns nothing.
 */
function match(input, compare) {
    if (input.value != document.getElementById(compare).value) 
        input.setCustomValidity('Passwords do not match.'); 
}
