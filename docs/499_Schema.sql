--------------------------------------------------------
-- 499_schema
-- Updated Schema for March 9, 2022
--------------------------------------------------------

--------------------------------------------------------
--  SEQUENCES
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Sequence ACTION_DETAIL_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "ACTION_DETAIL_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 48 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL ;
--------------------------------------------------------
--  DDL for Sequence ANSWER_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "ANSWER_SEQ"  MINVALUE 1 MAXVALUE 10000 INCREMENT BY 1 START WITH 201 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL ;
--------------------------------------------------------
--  DDL for Sequence BOOK_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "BOOK_SEQ"  MINVALUE 1 MAXVALUE 10000 INCREMENT BY 1 START WITH 141 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL ;
--------------------------------------------------------
--  DDL for Sequence DETAILS_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "DETAILS_SEQ"  MINVALUE 1 MAXVALUE 10000 INCREMENT BY 1 START WITH 41 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL ;
--------------------------------------------------------
--  DDL for Sequence QUESTION_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "QUESTION_SEQ"  MINVALUE 1 MAXVALUE 10000 INCREMENT BY 1 START WITH 101 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL ;
--------------------------------------------------------
--  DDL for Sequence SCHOOL_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "SCHOOL_SEQ"  MINVALUE 1 MAXVALUE 10000 INCREMENT BY 1 START WITH 21 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL ;
--------------------------------------------------------
--  DDL for Sequence STUDY_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "STUDY_SEQ"  MINVALUE 1 MAXVALUE 10000 INCREMENT BY 1 START WITH 21 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL ;

--------------------------------------------------------
--  TABLES
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Table ACTION
--------------------------------------------------------

  CREATE TABLE "ACTION" 
   (	"USER_ID" VARCHAR2(32 BYTE) COLLATE "USING_NLS_COMP", 
	"ACTION_START" DATE, 
	"ACTION_STOP" DATE, 
	"BOOK_ID" NUMBER, 
	"DETAIL_ID" NUMBER
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table ACTION_DETAIL
--------------------------------------------------------

  CREATE TABLE "ACTION_DETAIL" 
   (	"DETAIL_ID" NUMBER, 
	"DETAIL_DESCRIPTION" VARCHAR2(100 BYTE) COLLATE "USING_NLS_COMP", 
	"ACTION_KEY_ID" NUMBER
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table ACTION_KEY
--------------------------------------------------------

  CREATE TABLE "ACTION_KEY" 
   (	"ACTION_KEY_ID" NUMBER, 
	"ACTION_NAME" VARCHAR2(32 BYTE) COLLATE "USING_NLS_COMP"
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table ANSWER
--------------------------------------------------------

  CREATE TABLE "ANSWER" 
   (	"ANSWER_ID" NUMBER, 
	"QUESTION_ID" NUMBER, 
	"ANSWER" VARCHAR2(1000 BYTE) COLLATE "USING_NLS_COMP", 
	"CORRECT" NUMBER
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table BOOK
--------------------------------------------------------

  CREATE TABLE "BOOK" 
   (	"BOOK_ID" NUMBER, 
	"BOOK_NAME" VARCHAR2(20 BYTE) COLLATE "USING_NLS_COMP", 
	"CREATED_ON" DATE, 
	"URL" VARCHAR2(20 BYTE) COLLATE "USING_NLS_COMP", 
	"DESCRIPTION" VARCHAR2(1000 BYTE) COLLATE "USING_NLS_COMP", 
	"PAGE_COUNT" NUMBER, 
	"FOLDER" VARCHAR2(100 BYTE) COLLATE "USING_NLS_COMP"
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table BOOK_STUDY
--------------------------------------------------------

  CREATE TABLE "BOOK_STUDY" 
   (	"BOOK_ID" NUMBER, 
	"STUDY_ID" NUMBER
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table LAST_PAGE
--------------------------------------------------------

  CREATE TABLE "LAST_PAGE" 
   (	"USER_ID" VARCHAR2(36 BYTE) COLLATE "USING_NLS_COMP", 
	"BOOK_ID" NUMBER, 
	"LAST_PAGE" NUMBER
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table PASSWORD_RESET
--------------------------------------------------------

  CREATE TABLE "PASSWORD_RESET" 
   (	"USER_ID" VARCHAR2(36 BYTE) COLLATE "USING_NLS_COMP", 
	"RESET_KEY" VARCHAR2(1024 BYTE) COLLATE "USING_NLS_COMP", 
	"REQUEST_DATE" DATE
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table QUESTION
--------------------------------------------------------

  CREATE TABLE "QUESTION" 
   (	"QUESTION_ID" NUMBER, 
	"SCHOOL_ID" NUMBER, 
	"BOOK_ID" NUMBER, 
	"QUESTION" VARCHAR2(1000 BYTE) COLLATE "USING_NLS_COMP", 
	"PAGE_PREV" NUMBER, 
	"PAGE_NEXT" NUMBER, 
	"QUESTION_TYPE" NUMBER
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table SCHOOL
--------------------------------------------------------

  CREATE TABLE "SCHOOL" 
   (	"SCHOOL_ID" NUMBER, 
	"SCHOOL_NAME" VARCHAR2(40 BYTE) COLLATE "USING_NLS_COMP"
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table STUDY
--------------------------------------------------------

  CREATE TABLE "STUDY" 
   (	"STUDY_ID" NUMBER, 
	"SCHOOL_ID" NUMBER, 
	"STUDY_NAME" VARCHAR2(40 BYTE) COLLATE "USING_NLS_COMP"
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table USER_PROFILE
--------------------------------------------------------

  CREATE TABLE "USER_PROFILE" 
   (	"EMAIL" VARCHAR2(50 BYTE) COLLATE "USING_NLS_COMP", 
	"FIRST_NAME" VARCHAR2(20 BYTE) COLLATE "USING_NLS_COMP", 
	"LAST_NAME" VARCHAR2(20 BYTE) COLLATE "USING_NLS_COMP", 
	"ADMIN" NUMBER, 
	"SCHOOL_ID" NUMBER, 
	"CREATED_ON" DATE, 
	"LAST_LOGIN" DATE, 
	"PASSWORD" VARCHAR2(60 BYTE) COLLATE "USING_NLS_COMP", 
	"USER_ID" VARCHAR2(36 BYTE) COLLATE "USING_NLS_COMP"
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table USER_RESPONSE
--------------------------------------------------------

  CREATE TABLE "USER_RESPONSE" 
   (	"USER_ID" VARCHAR2(32 BYTE) COLLATE "USING_NLS_COMP", 
	"QUESTION_ID" NUMBER, 
	"ANSWER_ID" NUMBER, 
	"ANSWERED_ON" DATE
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table USER_SESSION
--------------------------------------------------------

  CREATE TABLE "USER_SESSION" 
   (	"SESSION_ID" VARCHAR2(36 BYTE) COLLATE "USING_NLS_COMP", 
	"USER_ID" VARCHAR2(36 BYTE) COLLATE "USING_NLS_COMP", 
	"LAST_LOGIN" DATE, 
	"ACTIVE" NUMBER(1,0) DEFAULT 0
   )  DEFAULT COLLATION "USING_NLS_COMP" ;
--------------------------------------------------------
--  DDL for Table USER_STUDY
--------------------------------------------------------

  CREATE TABLE "USER_STUDY" 
   (	"USER_ID" VARCHAR2(32 BYTE) COLLATE "USING_NLS_COMP", 
	"STUDY_ID" NUMBER
   )  DEFAULT COLLATION "USING_NLS_COMP" ;


--------------------------------------------------------
--  INDEXES
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Index ACTION_DETAIL_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "ACTION_DETAIL_PK" ON "ACTION_DETAIL" ("DETAIL_ID") 
  ;
--------------------------------------------------------
--  DDL for Index ACTION_KEY_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "ACTION_KEY_PK" ON "ACTION_KEY" ("ACTION_KEY_ID") 
  ;
--------------------------------------------------------
--  DDL for Index ANSWER_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "ANSWER_PK" ON "ANSWER" ("ANSWER_ID") 
  ;
--------------------------------------------------------
--  DDL for Index BOOK_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "BOOK_PK" ON "BOOK" ("BOOK_ID") 
  ;
--------------------------------------------------------
--  DDL for Index QUESTION_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "QUESTION_PK" ON "QUESTION" ("QUESTION_ID") 
  ;
--------------------------------------------------------
--  DDL for Index SCHOOL_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "SCHOOL_PK" ON "SCHOOL" ("SCHOOL_ID") 
  ;
--------------------------------------------------------
--  DDL for Index STUDY_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "STUDY_PK" ON "STUDY" ("STUDY_ID") 
  ;
--------------------------------------------------------
--  DDL for Index USER_PROFILE_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "USER_PROFILE_PK" ON "USER_PROFILE" ("USER_ID") 
  ;
--------------------------------------------------------
--  DDL for Index USER_SESSION_INDEX1
--------------------------------------------------------

  CREATE UNIQUE INDEX "USER_SESSION_INDEX1" ON "USER_SESSION" ("SESSION_ID") 
  ;
--------------------------------------------------------
--  DDL for Index ACTION_DETAIL_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "ACTION_DETAIL_PK" ON "ACTION_DETAIL" ("DETAIL_ID") 
  ;
--------------------------------------------------------
--  DDL for Index ACTION_KEY_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "ACTION_KEY_PK" ON "ACTION_KEY" ("ACTION_KEY_ID") 
  ;
--------------------------------------------------------
--  DDL for Index ANSWER_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "ANSWER_PK" ON "ANSWER" ("ANSWER_ID") 
  ;
--------------------------------------------------------
--  DDL for Index BOOK_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "BOOK_PK" ON "BOOK" ("BOOK_ID") 
  ;
--------------------------------------------------------
--  DDL for Index QUESTION_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "QUESTION_PK" ON "QUESTION" ("QUESTION_ID") 
  ;
--------------------------------------------------------
--  DDL for Index SCHOOL_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "SCHOOL_PK" ON "SCHOOL" ("SCHOOL_ID") 
  ;
--------------------------------------------------------
--  DDL for Index STUDY_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "STUDY_PK" ON "STUDY" ("STUDY_ID") 
  ;
--------------------------------------------------------
--  DDL for Index USER_PROFILE_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "USER_PROFILE_PK" ON "USER_PROFILE" ("USER_ID") 
  ;
--------------------------------------------------------
--  DDL for Index USER_SESSION_INDEX1
--------------------------------------------------------

  CREATE UNIQUE INDEX "USER_SESSION_INDEX1" ON "USER_SESSION" ("SESSION_ID") 
  ;

--------------------------------------------------------
--  TRIGGERS
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Trigger ANSWER_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "ANSWER_TRG" 
BEFORE INSERT ON ANSWER 
FOR EACH ROW 
BEGIN
    SELECT ANSWER_SEQ.NEXTVAL INTO :new.ANSWER_ID FROM dual;
  NULL;
END;
/
ALTER TRIGGER "ANSWER_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger BOOK_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "BOOK_TRG" 
BEFORE INSERT ON BOOK 
FOR EACH ROW 
BEGIN

    SELECT BOOK_SEQ.NEXTVAL INTO :new.BOOK_ID FROM dual;
    :new.CREATED_ON := sysdate();
    
  NULL;
END;
/
ALTER TRIGGER "BOOK_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger DETAIL_ID_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "DETAIL_ID_TRG" 
BEFORE INSERT ON ACTION_DETAIL
FOR EACH ROW 
BEGIN
    SELECT DETAILS_SEQ.NEXTVAL INTO :new.DETAIL_ID FROM dual;
  NULL;
END;
/
ALTER TRIGGER "DETAIL_ID_TRG" DISABLE;
--------------------------------------------------------
--  DDL for Trigger NEW_USER_SESSION
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "NEW_USER_SESSION" AFTER
    INSERT ON user_profile
    FOR EACH ROW
DECLARE 
    v_random_session_id raw(32);
BEGIN
  -- When a new user is created, it automatically has a new user_session created
  select sys_guid() into v_random_session_id from dual;
  v_random_session_id := RAWTOHEX(v_random_session_id);

    IF inserting THEN
        INSERT INTO user_session (
            session_id,
            user_id,
            last_login,
            active
        ) VALUES (
            v_random_session_id,
            :new.user_id,
            sysdate,
            0
        );

    END IF;
END;
/
ALTER TRIGGER "NEW_USER_SESSION" ENABLE;
--------------------------------------------------------
--  DDL for Trigger PASSWORD_RESET_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "PASSWORD_RESET_TRG" 
BEFORE INSERT ON PASSWORD_RESET 
FOR EACH ROW 
declare
        t_user_id password_reset.user_id%type;
        user_exists EXCEPTION;
        PRAGMA exception_init(user_exists, -20100);
        id_count number;
BEGIN
        select count(*) into id_count from password_reset where user_id = :new.user_id;
        
        if id_count > 0 then
            raise_application_error(-20100, 'User already has entry.');
        end if;
        
        :new.request_date := sysdate;
   
END;
/
ALTER TRIGGER "PASSWORD_RESET_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger QUESTION_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "QUESTION_TRG" 
BEFORE INSERT ON QUESTION 
FOR EACH ROW 
BEGIN
    SELECT QUESTION_SEQ.NEXTVAL INTO :new.QUESTION_ID FROM dual;
  NULL;
END;
/
ALTER TRIGGER "QUESTION_TRG" DISABLE;
--------------------------------------------------------
--  DDL for Trigger SCHOOL_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "SCHOOL_TRG" 
BEFORE INSERT ON SCHOOL
FOR EACH ROW
BEGIN
    SELECT SCHOOL_SEQ.NEXTVAL INTO :new.SCHOOL_ID FROM dual;
  NULL;
END;
/
ALTER TRIGGER "SCHOOL_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger STUDY_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "STUDY_TRG" 
BEFORE INSERT ON STUDY 
FOR EACH ROW 
BEGIN
    SELECT STUDY_SEQ.NEXTVAL INTO :new.STUDY_ID FROM dual;
  NULL;
END;
/
ALTER TRIGGER "STUDY_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger USER_ID_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "USER_ID_TRG" 
BEFORE INSERT ON USER_PROFILE 
FOR EACH ROW 
BEGIN
    select sys_guid() into :new.user_id from dual;
  NULL; 
END;
/
ALTER TRIGGER "USER_ID_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger USER_PROFILE_CREATED_ON
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "USER_PROFILE_CREATED_ON" BEFORE
    INSERT ON user_profile
    FOR EACH ROW
BEGIN
    :new.created_on := sysdate;
    
END;
/
ALTER TRIGGER "USER_PROFILE_CREATED_ON" ENABLE;
--------------------------------------------------------
--  DDL for Trigger DETAIL_ID_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "DETAIL_ID_TRG" 
BEFORE INSERT ON ACTION_DETAIL
FOR EACH ROW 
BEGIN
    SELECT DETAILS_SEQ.NEXTVAL INTO :new.DETAIL_ID FROM dual;
  NULL;
END;
/
ALTER TRIGGER "DETAIL_ID_TRG" DISABLE;
--------------------------------------------------------
--  DDL for Trigger ANSWER_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "ANSWER_TRG" 
BEFORE INSERT ON ANSWER 
FOR EACH ROW 
BEGIN
    SELECT ANSWER_SEQ.NEXTVAL INTO :new.ANSWER_ID FROM dual;
  NULL;
END;
/
ALTER TRIGGER "ANSWER_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger BOOK_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "BOOK_TRG" 
BEFORE INSERT ON BOOK 
FOR EACH ROW 
BEGIN

    SELECT BOOK_SEQ.NEXTVAL INTO :new.BOOK_ID FROM dual;
    :new.CREATED_ON := sysdate();
    
  NULL;
END;
/
ALTER TRIGGER "BOOK_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger PASSWORD_RESET_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "PASSWORD_RESET_TRG" 
BEFORE INSERT ON PASSWORD_RESET 
FOR EACH ROW 
declare
        t_user_id password_reset.user_id%type;
        user_exists EXCEPTION;
        PRAGMA exception_init(user_exists, -20100);
        id_count number;
BEGIN
        select count(*) into id_count from password_reset where user_id = :new.user_id;
        
        if id_count > 0 then
            raise_application_error(-20100, 'User already has entry.');
        end if;
        
        :new.request_date := sysdate;
   
END;
/
ALTER TRIGGER "PASSWORD_RESET_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger QUESTION_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "QUESTION_TRG" 
BEFORE INSERT ON QUESTION 
FOR EACH ROW 
BEGIN
    SELECT QUESTION_SEQ.NEXTVAL INTO :new.QUESTION_ID FROM dual;
  NULL;
END;
/
ALTER TRIGGER "QUESTION_TRG" DISABLE;
--------------------------------------------------------
--  DDL for Trigger SCHOOL_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "SCHOOL_TRG" 
BEFORE INSERT ON SCHOOL
FOR EACH ROW
BEGIN
    SELECT SCHOOL_SEQ.NEXTVAL INTO :new.SCHOOL_ID FROM dual;
  NULL;
END;
/
ALTER TRIGGER "SCHOOL_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger STUDY_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "STUDY_TRG" 
BEFORE INSERT ON STUDY 
FOR EACH ROW 
BEGIN
    SELECT STUDY_SEQ.NEXTVAL INTO :new.STUDY_ID FROM dual;
  NULL;
END;
/
ALTER TRIGGER "STUDY_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger USER_PROFILE_CREATED_ON
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "USER_PROFILE_CREATED_ON" BEFORE
    INSERT ON user_profile
    FOR EACH ROW
BEGIN
    :new.created_on := sysdate;
    
END;
/
ALTER TRIGGER "USER_PROFILE_CREATED_ON" ENABLE;
--------------------------------------------------------
--  DDL for Trigger NEW_USER_SESSION
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "NEW_USER_SESSION" AFTER
    INSERT ON user_profile
    FOR EACH ROW
DECLARE 
    v_random_session_id raw(32);
BEGIN
  -- When a new user is created, it automatically has a new user_session created
  select sys_guid() into v_random_session_id from dual;
  v_random_session_id := RAWTOHEX(v_random_session_id);

    IF inserting THEN
        INSERT INTO user_session (
            session_id,
            user_id,
            last_login,
            active
        ) VALUES (
            v_random_session_id,
            :new.user_id,
            sysdate,
            0
        );

    END IF;
END;
/
ALTER TRIGGER "NEW_USER_SESSION" ENABLE;
--------------------------------------------------------
--  DDL for Trigger USER_ID_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "USER_ID_TRG" 
BEFORE INSERT ON USER_PROFILE 
FOR EACH ROW 
BEGIN
    select sys_guid() into :new.user_id from dual;
  NULL; 
END;
/
ALTER TRIGGER "USER_ID_TRG" ENABLE;


--------------------------------------------------------
--  PROCEDURES
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Procedure CHECK_DETAIL_ID_PROC
--------------------------------------------------------
set define off;

  CREATE OR REPLACE EDITIONABLE PROCEDURE "CHECK_DETAIL_ID_PROC" (
    user_id_in            IN user_profile.user_id%TYPE,
    action_start_in       IN action.action_start%TYPE,
    action_stop_in        IN action.action_stop%TYPE,
    book_id_in            IN book.book_id%TYPE,
    detail_description_in IN action_detail.detail_description%TYPE,
    action_key_id_in      IN action_detail.action_key_id%TYPE
) AS
BEGIN
    BEGIN
        DECLARE
            detail_id_in action_detail.detail_id%TYPE;
        BEGIN
            BEGIN
                SELECT
                    detail_id
                INTO detail_id_in
                FROM
                    action_detail ad
                WHERE
                    detail_description = detail_description_in; -- this is coming from front end
            EXCEPTION
                WHEN no_data_found THEN
                    detail_id_in := NULL;
            END;

            IF detail_id_in IS NOT NULL THEN -- the detail id already exists, run with it
                INSERT INTO action (
                    user_id,
                    action_start,
                    action_stop,
                    book_id,
                    detail_id
                ) VALUES (
                    user_id_in, -- this comes from the token
                    action_start_in, -- this is coming from the front end
                    action_stop_in, -- this is coming from the front end
                    book_id_in, -- this is coming from the front end
                    detail_id_in
                );

            END IF;

            IF detail_id_in IS NULL THEN
                SELECT
                    action_detail_seq.NEXTVAL
                INTO detail_id_in
                FROM
                    dual;

                INSERT INTO action_detail (
                    detail_id,
                    detail_description,
                    action_key_id
                ) VALUES (
                    detail_id_in,
                    detail_description_in, -- also coming from front end
                    action_key_id_in -- '... this is also coming from the front end ...'
                );

                INSERT INTO action (
                    user_id,
                    action_start,
                    action_stop,
                    book_id,
                    detail_id
                ) VALUES (
                    user_id_in, -- this comes from the token
                    action_start_in, -- this is coming from the front end
                    action_stop_in, -- this is coming from the front end
                    book_id_in, -- this is coming from the front end
                    detail_id_in
                );

            END IF;

        END;

    END;
END check_detail_id_proc;

/
--------------------------------------------------------
--  DDL for Procedure DELETE_QUESTION_ANSWER_PROC
--------------------------------------------------------
set define off;

  CREATE OR REPLACE EDITIONABLE PROCEDURE "DELETE_QUESTION_ANSWER_PROC" 
(
  QUESTION_ID_IN IN NUMBER 
) AS 
BEGIN

      DELETE FROM ANSWER WHERE QUESTION_ID = QUESTION_ID_IN;
      DELETE FROM QUESTION WHERE QUESTION_ID = QUESTION_ID_IN;

END DELETE_QUESTION_ANSWER_PROC;

/
--------------------------------------------------------
--  DDL for Procedure EDIT_QUESTION_PROC
--------------------------------------------------------
set define off;

  CREATE OR REPLACE EDITIONABLE PROCEDURE "EDIT_QUESTION_PROC" (
    question_id_in IN NUMBER,
    question_in    IN VARCHAR2,
    answers_in     IN VARCHAR2
) AS
BEGIN
    BEGIN
    
    update question set question = question_in where question_id = question_id_in;
    
        FOR i IN (
            SELECT
                TRIM(regexp_substr(answers_in, '(.*?)( ~`~ |$)', 1, level, NULL,
                                   1)) l
            FROM
                dual
            CONNECT BY
                level <= regexp_count(answers_in, ' ~`~ ') + 1
        ) LOOP
            BEGIN
                DECLARE
                    delimiter_pos NUMBER;
                    answer_id_in varchar2(5);
                    answer_in    answer.answer%TYPE;
                BEGIN
                    SELECT INSTR(i.l, '++', 1, 1) "Instring" into delimiter_pos from DUAL;
                    
                    SELECT substr(i.l, 1, delimiter_pos-1) INTO answer_id_in FROM DUAL;

                    SELECT substr(i.l, delimiter_pos+2) INTO answer_in FROM dual;

                    UPDATE answer SET answer = answer_in WHERE answer_id = to_number(answer_id_in);

                END;

            END;
        END LOOP;

    END;
END edit_question_proc;

/
--------------------------------------------------------
--  DDL for Procedure INSERT_QUESTION_PROC
--------------------------------------------------------
set define off;

  CREATE OR REPLACE EDITIONABLE PROCEDURE "INSERT_QUESTION_PROC" (
    question_in  IN question.question%TYPE,
    school_id_in IN question.school_id%TYPE,
    book_id_in   IN question.book_id%TYPE,
    page_prev_in IN question.page_prev%TYPE,
    page_next_in IN question.page_next%TYPE,
    answers_in   IN VARCHAR2
) AS
BEGIN
    DECLARE
        question_id_in question.question_id%TYPE;
    BEGIN
        SELECT
            question_seq.NEXTVAL
        INTO question_id_in
        FROM
            dual;

        INSERT INTO question (
            question_id,
            school_id,
            book_id,
            question,
            page_prev,
            page_next
        ) VALUES (
            question_id_in,
            school_id_in,
            book_id_in,
            question_in,
            page_prev_in,
            page_next_in
        );

        BEGIN
            FOR i IN (
                SELECT
                    TRIM(regexp_substr(answers_in, '(.*?)( ~`~ |$)', 1, level, NULL,
                                       1)) l
                FROM
                    dual
                CONNECT BY
                    level <= regexp_count(answers_in, ' ~`~ ') + 1
            ) LOOP
                BEGIN
                    INSERT INTO answer (
                        question_id,
                        answer
                    ) VALUES (
                        question_id_in,
                        i.l
                    );

                END;
            END LOOP;
        END;

    END;
END insert_question_proc;

/

--------------------------------------------------------
--  FUNCTIONS
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Function CHECK_DETAIL_ID_FCN
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE FUNCTION "CHECK_DETAIL_ID_FCN" (
    user_id_in            IN VARCHAR2,
    action_start_in       IN DATE,
    action_stop_in        IN DATE,
    book_id_in            IN NUMBER,
    detail_description_in IN VARCHAR2,
    action_key_id_in          IN NUMBER
) RETURN NUMBER AS
    -- 0 if failure, 1 if success
    successful_insert NUMBER := 0;
BEGIN
    DECLARE
        detail_id_in action_detail.detail_id%TYPE;
    BEGIN
        BEGIN
            SELECT
                detail_id
            INTO detail_id_in
            FROM
                action_detail ad
            WHERE
                detail_description = 'onto p1300 from off page'; -- this is coming from front end
        EXCEPTION
            WHEN no_data_found THEN
                detail_id_in := NULL;
        END;

        IF detail_id_in IS NOT NULL THEN -- the detail id already exists, run with it
            INSERT INTO action (
                user_id,
                action_start,
                action_stop,
                book_id,
                detail_id
            ) VALUES (
                user_id_in, -- this comes from the token
                action_start_in,
                action_stop_in,
                book_id_in, -- this is coming from the front end
                detail_id_in
            );

        END IF;

        IF detail_id_in IS NULL THEN
            SELECT
                action_detail_seq.NEXTVAL
            INTO detail_id_in
            FROM
                dual;

            INSERT INTO action_detail (
                detail_id,
                detail_description,
                action_key_id
            ) VALUES (
                detail_id_in,
                detail_description_in, -- also coming from front end
                action_key_id_in -- '... this is also coming from the front end ...'
            );

            INSERT INTO action (
                user_id,
                action_start,
                action_stop,
                book_id,
                detail_id
            ) VALUES (
                user_id_in, -- this comes from the token
                action_start_in,
                action_stop_in,
                book_id_in, -- this is coming from the front end
                detail_id_in
            );

        END IF;

    END;
END check_detail_id_fcn;

/

--------------------------------------------------------
--  CONSTRAINTS
--------------------------------------------------------
--------------------------------------------------------
--  Constraints for Table ACTION
--------------------------------------------------------

  ALTER TABLE "ACTION" MODIFY ("USER_ID" NOT NULL ENABLE);
  ALTER TABLE "ACTION" MODIFY ("ACTION_START" NOT NULL ENABLE);
  ALTER TABLE "ACTION" MODIFY ("ACTION_STOP" NOT NULL ENABLE);
  ALTER TABLE "ACTION" MODIFY ("BOOK_ID" NOT NULL ENABLE);
  ALTER TABLE "ACTION" MODIFY ("DETAIL_ID" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table ACTION_DETAIL
--------------------------------------------------------

  ALTER TABLE "ACTION_DETAIL" MODIFY ("DETAIL_ID" NOT NULL ENABLE);
  ALTER TABLE "ACTION_DETAIL" MODIFY ("DETAIL_DESCRIPTION" NOT NULL ENABLE);
  ALTER TABLE "ACTION_DETAIL" ADD CONSTRAINT "ACTION_DETAIL_PK" PRIMARY KEY ("DETAIL_ID")
  USING INDEX  ENABLE;
  ALTER TABLE "ACTION_DETAIL" MODIFY ("ACTION_KEY_ID" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table ACTION_KEY
--------------------------------------------------------

  ALTER TABLE "ACTION_KEY" MODIFY ("ACTION_NAME" NOT NULL ENABLE);
  ALTER TABLE "ACTION_KEY" ADD CONSTRAINT "ACTION_KEY_PK" PRIMARY KEY ("ACTION_KEY_ID")
  USING INDEX  ENABLE;
  ALTER TABLE "ACTION_KEY" MODIFY ("ACTION_KEY_ID" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table ANSWER
--------------------------------------------------------

  ALTER TABLE "ANSWER" MODIFY ("CORRECT" NOT NULL ENABLE);
  ALTER TABLE "ANSWER" ADD CONSTRAINT "ANSWER_PK" PRIMARY KEY ("ANSWER_ID")
  USING INDEX  ENABLE;
  ALTER TABLE "ANSWER" MODIFY ("QUESTION_ID" NOT NULL ENABLE);
  ALTER TABLE "ANSWER" MODIFY ("ANSWER" NOT NULL ENABLE);
  ALTER TABLE "ANSWER" MODIFY ("ANSWER_ID" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table BOOK
--------------------------------------------------------

  ALTER TABLE "BOOK" MODIFY ("FOLDER" NOT NULL ENABLE);
  ALTER TABLE "BOOK" MODIFY ("PAGE_COUNT" NOT NULL ENABLE);
  ALTER TABLE "BOOK" MODIFY ("BOOK_ID" NOT NULL ENABLE);
  ALTER TABLE "BOOK" MODIFY ("BOOK_NAME" NOT NULL ENABLE);
  ALTER TABLE "BOOK" MODIFY ("CREATED_ON" NOT NULL ENABLE);
  ALTER TABLE "BOOK" MODIFY ("DESCRIPTION" NOT NULL ENABLE);
  ALTER TABLE "BOOK" ADD CONSTRAINT "BOOK_PK" PRIMARY KEY ("BOOK_ID")
  USING INDEX  ENABLE;
--------------------------------------------------------
--  Constraints for Table BOOK_STUDY
--------------------------------------------------------

  ALTER TABLE "BOOK_STUDY" MODIFY ("STUDY_ID" NOT NULL ENABLE);
  ALTER TABLE "BOOK_STUDY" MODIFY ("BOOK_ID" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table LAST_PAGE
--------------------------------------------------------

  ALTER TABLE "LAST_PAGE" MODIFY ("BOOK_ID" NOT NULL ENABLE);
  ALTER TABLE "LAST_PAGE" MODIFY ("LAST_PAGE" NOT NULL ENABLE);
  ALTER TABLE "LAST_PAGE" MODIFY ("USER_ID" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table PASSWORD_RESET
--------------------------------------------------------

  ALTER TABLE "PASSWORD_RESET" MODIFY ("USER_ID" NOT NULL ENABLE);
  ALTER TABLE "PASSWORD_RESET" MODIFY ("REQUEST_DATE" NOT NULL ENABLE);
  ALTER TABLE "PASSWORD_RESET" MODIFY ("RESET_KEY" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table QUESTION
--------------------------------------------------------

  ALTER TABLE "QUESTION" MODIFY ("PAGE_PREV" NOT NULL ENABLE);
  ALTER TABLE "QUESTION" MODIFY ("PAGE_NEXT" NOT NULL ENABLE);
  ALTER TABLE "QUESTION" MODIFY ("QUESTION_TYPE" NOT NULL ENABLE);
  ALTER TABLE "QUESTION" MODIFY ("QUESTION_ID" NOT NULL ENABLE);
  ALTER TABLE "QUESTION" MODIFY ("SCHOOL_ID" NOT NULL ENABLE);
  ALTER TABLE "QUESTION" MODIFY ("BOOK_ID" NOT NULL ENABLE);
  ALTER TABLE "QUESTION" MODIFY ("QUESTION" NOT NULL ENABLE);
  ALTER TABLE "QUESTION" ADD CONSTRAINT "QUESTION_PK" PRIMARY KEY ("QUESTION_ID")
  USING INDEX  ENABLE;
--------------------------------------------------------
--  Constraints for Table SCHOOL
--------------------------------------------------------

  ALTER TABLE "SCHOOL" MODIFY ("SCHOOL_ID" NOT NULL ENABLE);
  ALTER TABLE "SCHOOL" MODIFY ("SCHOOL_NAME" NOT NULL ENABLE);
  ALTER TABLE "SCHOOL" ADD CONSTRAINT "SCHOOL_PK" PRIMARY KEY ("SCHOOL_ID")
  USING INDEX  ENABLE;
--------------------------------------------------------
--  Constraints for Table STUDY
--------------------------------------------------------

  ALTER TABLE "STUDY" MODIFY ("STUDY_ID" NOT NULL ENABLE);
  ALTER TABLE "STUDY" MODIFY ("SCHOOL_ID" NOT NULL ENABLE);
  ALTER TABLE "STUDY" MODIFY ("STUDY_NAME" NOT NULL ENABLE);
  ALTER TABLE "STUDY" ADD CONSTRAINT "STUDY_PK" PRIMARY KEY ("STUDY_ID")
  USING INDEX  ENABLE;
--------------------------------------------------------
--  Constraints for Table USER_PROFILE
--------------------------------------------------------

  ALTER TABLE "USER_PROFILE" MODIFY ("USER_ID" NOT NULL ENABLE);
  ALTER TABLE "USER_PROFILE" ADD CONSTRAINT "USER_PROFILE_PK" PRIMARY KEY ("USER_ID")
  USING INDEX  ENABLE;
  ALTER TABLE "USER_PROFILE" MODIFY ("EMAIL" NOT NULL ENABLE);
  ALTER TABLE "USER_PROFILE" MODIFY ("FIRST_NAME" NOT NULL ENABLE);
  ALTER TABLE "USER_PROFILE" MODIFY ("LAST_NAME" NOT NULL ENABLE);
  ALTER TABLE "USER_PROFILE" MODIFY ("ADMIN" NOT NULL ENABLE);
  ALTER TABLE "USER_PROFILE" MODIFY ("SCHOOL_ID" NOT NULL ENABLE);
  ALTER TABLE "USER_PROFILE" MODIFY ("CREATED_ON" NOT NULL ENABLE);
  ALTER TABLE "USER_PROFILE" MODIFY ("PASSWORD" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table USER_RESPONSE
--------------------------------------------------------

  ALTER TABLE "USER_RESPONSE" MODIFY ("USER_ID" NOT NULL ENABLE);
  ALTER TABLE "USER_RESPONSE" MODIFY ("QUESTION_ID" NOT NULL ENABLE);
  ALTER TABLE "USER_RESPONSE" MODIFY ("ANSWER_ID" NOT NULL ENABLE);
  ALTER TABLE "USER_RESPONSE" MODIFY ("ANSWERED_ON" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table USER_SESSION
--------------------------------------------------------

  ALTER TABLE "USER_SESSION" MODIFY ("USER_ID" NOT NULL ENABLE);
  ALTER TABLE "USER_SESSION" MODIFY ("SESSION_ID" NOT NULL ENABLE);
  ALTER TABLE "USER_SESSION" MODIFY ("LAST_LOGIN" NOT NULL ENABLE);
  ALTER TABLE "USER_SESSION" MODIFY ("ACTIVE" NOT NULL ENABLE);
  ALTER TABLE "USER_SESSION" ADD CONSTRAINT "USER_SESSION_PK" PRIMARY KEY ("SESSION_ID")
  USING INDEX "USER_SESSION_INDEX1"  ENABLE;
--------------------------------------------------------
--  Constraints for Table USER_STUDY
--------------------------------------------------------

  ALTER TABLE "USER_STUDY" MODIFY ("USER_ID" NOT NULL ENABLE);
  ALTER TABLE "USER_STUDY" MODIFY ("STUDY_ID" NOT NULL ENABLE);
