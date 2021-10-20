-- select query to get user actions --

select user_profile.username,action.current_page, action.prev_page, action.link, action.occurred_on from user_profile

inner join action on user_profile.user_id = action.user_id;

