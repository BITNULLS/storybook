select
    user_profile.email,
    user_profile.first_name,
    user_profile.last_name,
    user_profile.created_on,
    user_profile.last_login,
    school.school_name,
    study.study_name

from user_profile
    inner join school on user_profile.school_id = school.school_id
    inner join study on user_profile.study_id = study.study_id