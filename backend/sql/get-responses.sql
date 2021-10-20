-- select query to get user response --

select user_profile.username, study.study_name, book.book_name, question.question, answer.answer, user_response.answered_on from user_profile

inner join study on user_profile.study_id = study.study_id

inner join book on study.study_id = book.book_id

inner join user_response on user_profile.user_id = user_response.user_id

inner join answer on user_response.answer_id = answer.answer_id

inner join question on answer.question_id = question.question_id