"""
storyboard.py

This handles displaying the pages of the book, storing user actions, and
receiving quiz question responses from the user.
"""

import logging
import json
from click import option
import jwt

from flask import Blueprint
from flask import request
from flask import abort

from edu_storybook.templates import Templates
from edu_storybook.core.config import config
from edu_storybook.core.auth import validate_login
from edu_storybook.templates import Templates
from edu_storybook.core.config import config
from edu_storybook.core.sensitive import jwt_key
from edu_storybook.core.config import Config

from edu_storybook.api.index import get_book_info
from edu_storybook.api.storyboard import check_quiz_question

from edu_storybook.navbar import make_navbar

storyboard = Blueprint('storyboard', __name__)

log = logging.getLogger('ssg.storyboard')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

@storyboard.route("/storyboard/<int:book_id_in>/<int:page_number_in>")
def gen_storyboard_page(book_id_in: int, page_number_in: int):
    '''
    Generate the storyboard viewer page.
    '''
    auth = None
    if 'Authorization' in request.cookies:
        auth = request.cookies['Authorization']
        vl = validate_login(
            auth,
            permission=0
        )
        if vl != True:
            log.debug(
                f'A non-admin user tried to access the /storyboard/{book_id_in}/{page_number_in} page.'
            )
            abort(403)
    else:
        log.debug(
            f'An unauthorized, logged out user tried to access the /storyboard/{book_id_in}/{page_number_in} page.'
        )
        abort(403)
        
    if 'Bearer' in auth:
        auth = auth.replace('Bearer ', '', 1)
    
    token = jwt.decode(auth, jwt_key, algorithms=Config.jwt_alg)
    
    book_id = int(book_id_in)
    page_number = int(page_number_in)

    # Get book_info based on book_id from latest api endpoint /api/book/book_id
    book_info = json.loads(get_book_info(book_id))
    name = book_info['BOOK_NAME']
    page_count = book_info['PAGE_COUNT']

    # Display/Hide "Previous" link based on current page number
    if page_number == 1:
        prev_link_visibility = "display: none"
    else:
        prev_link_visibility = "display: block"

    # Display/Hide "Next" link based on current page number
    if page_number == page_count:
        next_link_visibility = "display: none"
    else:
        next_link_visibility = "display: block"
    
    # Returns the list of quiz question(s) for given book and page number for user to answer
    quiz_questions = check_quiz_question(book_id, page_number, token['sub'])
    options_buttons = ""
    
    if(quiz_questions != False):
        
        # Get the first question from the list of unanswered questions
        question = quiz_questions[0]
        
        if(question['question_type'] == 1):
            
            display_question = question['question']
            display_question_id = question['question_id']
                
            # Logic to dynamically add buttons on-the-fly
            for answer_choice in question['answers']:
                button_value = answer_choice['answer_id']
                answer_choice_name = answer_choice['answer']
                options_buttons = options_buttons + "<button name='answer_id' type='submit' value='" + str(button_value) + "' class='btn btn-info'> " + answer_choice_name + " </button> <br> <br>"
            
            display_mc_items = Templates.storyboard_quiz_mc_item.substitute(
                question_id = display_question_id,
                id_of_book = str(book_id),
                page_num_val = str(page_number),
                url = "/storyboard/" + str(book_id) + "/" + str(page_number),
                options = options_buttons
            )
                    
            mc_page = Templates._base.substitute(
                title = 'Multiple Choice Quiz',
                description = 'Check Your Understanding So Far',
                body = Templates.storyboard_quiz_mc.substitute(
                    question = display_question,
                    mc_items = display_mc_items,
                    prevPageURL = "/storyboard/" + str(book_id) + "/" + str(page_number - 1)                
                )
            )
                
            return mc_page
            
        else:
            display_question = question['question']
            display_question_id = question['question_id']
            
            fr_page = Templates._base.substitute(
                title = 'Free Response Quiz',
                description = 'Check Your Understanding So Far',
                body = Templates.storyboard_quiz_fr.substitute(
                    url = "/storyboard/" + str(book_id)+ "/" + str(page_number),
                    id_of_book = str(book_id),
                    page_num_val = str(page_number),    
                    question = display_question,
                    question_id = display_question_id,
                    prevPageURL = "/storyboard/" + str(book_id) + "/" + str(page_number - 1)
                )
            )
            return fr_page

    # Generate Storyboard Viewer page
    storyboard_page = Templates._base.substitute(
        title = 'Storyboard Page',
        description = 'Make an account with our website',
        body = Templates.storyboard_viewer.substitute(
            navbar = make_navbar( auth ),
            book_name = name,
            current_page = "/api/storyboard/page/" + str(book_id) + "/" + str(page_number),
            id = str(book_id),
            prev_page_num = str(page_number - 1),
            next_page_num = str(page_number + 1),
            show_prev_link = prev_link_visibility,
            show_next_link = next_link_visibility
        )
    )
    return storyboard_page

