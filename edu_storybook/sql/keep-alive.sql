-- the following code is use for the timer job
-- runs once every 6 days
-- this code is only the query, NOT the full timer job

DECLARE 
    user_count number;
BEGIN
    SELECT count(*) into user_count FROM USER_PROFILE;
end;
