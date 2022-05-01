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
function match(input, compare, register_button) {
    if (document.getElementById(input).value != document.getElementById(compare).value) {
        register_button.setCustomValidity('Passwords do not match.');
    }
    else {
        register_button.setCustomValidity('');
    }
}
