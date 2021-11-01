select user_profile.email,
        action.action_start,
        action.action_stop,
        action.book_id,
        action_code.action_code,
        action_details.details
        from user_profile
        inner join action on user_profile.user_id = action.user_id
        inner join action_code on action.action_code = action_code.action_code
        inner join action_details on action.detail_id = action_details.detail_id