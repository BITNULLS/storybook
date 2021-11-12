--------------------------------------------------------
--  File created - Tuesday-October-05-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Table ACTION
--------------------------------------------------------

CREATE TABLE "ACTION"
(
  "USERNAME" VARCHAR2(20
  BYTE), 
	"TIME_ON_PAGE" NUMBER, 
	"CURRENT_PAGE" NUMBER, 
	"PREV_PAGE" NUMBER
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;
  --------------------------------------------------------
  --  DDL for Table ANSWER
  --------------------------------------------------------

  CREATE TABLE "ANSWER"
  (
    "ANSWER_ID" NUMBER,
    "QUESTION_ID" NUMBER,
    "ANSWER" VARCHAR2(255
    BYTE)
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;
    --------------------------------------------------------
    --  DDL for Table BOOK
    --------------------------------------------------------

    CREATE TABLE "BOOK"
    (
      "BOOK_ID" NUMBER,
      "NAME" VARCHAR2(20
      BYTE), 
	"CREATED_ON" DATE, 
	"URL" VARCHAR2
      (20 BYTE), 
	"DESCRIPTION" VARCHAR2
      (255 BYTE), 
	"STUDY_ID" NUMBER
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;
      --------------------------------------------------------
      --  DDL for Table QUESTION
      --------------------------------------------------------

      CREATE TABLE "QUESTION"
      (
        "QUESTION_ID" NUMBER,
        "SCHOOL_ID" NUMBER,
        "BOOK_ID" NUMBER,
        "QUESTION" VARCHAR2(255
        BYTE)
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;
        --------------------------------------------------------
        --  DDL for Table SCHOOL
        --------------------------------------------------------

        CREATE TABLE "SCHOOL"
        (
          "SCHOOL_ID" NUMBER,
          "NAME" VARCHAR2(20
          BYTE)
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;
          --------------------------------------------------------
          --  DDL for Table STUDY
          --------------------------------------------------------

          CREATE TABLE "STUDY"
          (
            "STUDY_ID" NUMBER,
            "SCHOOL_ID" NUMBER,
            "NAME" VARCHAR2(20
            BYTE)
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;
            --------------------------------------------------------
            --  DDL for Table USER_PROFILE
            --------------------------------------------------------

            CREATE TABLE "USER_PROFILE"
            (
              "EMAIL" VARCHAR2(20
              BYTE), 
	"USERNAME" VARCHAR2
              (20 BYTE), 
	"FIRST_NAME" VARCHAR2
              (20 BYTE), 
	"LAST_NAME" VARCHAR2
              (20 BYTE), 
	"ADMIN" NUMBER, 
	"SCHOOL_ID" NUMBER, 
	"CREATED_ON" DATE, 
	"LAST_LOGIN" DATE
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;
              --------------------------------------------------------
              --  DDL for Table USER_RESPONSE
              --------------------------------------------------------

              CREATE TABLE "USER_RESPONSE"
              (
                "USERNAME" VARCHAR2(20
                BYTE), 
	"QUESTION_ID" NUMBER, 
	"ANSWER_ID" NUMBER, 
	"ANSWERED_ON" DATE
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;
                --------------------------------------------------------
                --  DDL for Table USER_STUDY
                --------------------------------------------------------

                CREATE TABLE "USER_STUDY"
                (
                  "USERNAME" VARCHAR2(20
                  BYTE), 
	"STUDY_ID" NUMBER
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;
REM INSERTING into ACTION
                  SET DEFINE OFF;
                  REM INSERTING into ANSWER
                  SET DEFINE OFF;
                  REM INSERTING into BOOK
                  SET DEFINE OFF;
                  REM INSERTING into CUST
                  SET DEFINE OFF;
                  REM INSERTING into ORDERS
                  SET DEFINE OFF;
                  REM INSERTING into ORDERS_ITEMS
                  SET DEFINE OFF;
                  REM INSERTING into PRODUCT
                  SET DEFINE OFF;
                  REM INSERTING into QUESTION
                  SET DEFINE OFF;
                  REM INSERTING into SCHOOL
                  SET DEFINE OFF;
                  REM INSERTING into STUDENT
                  SET DEFINE OFF;
                  REM INSERTING into STUDY
                  SET DEFINE OFF;
                  REM INSERTING into USER_PROFILE
                  SET DEFINE OFF;
                  REM INSERTING into USER_RESPONSE
                  SET DEFINE OFF;
                  REM INSERTING into USER_STUDY
                  SET DEFINE OFF;
                  --------------------------------------------------------
                  --  Constraints for Table ANSWER
                  --------------------------------------------------------

                  ALTER TABLE "ANSWER" MODIFY
                  ("ANSWER_ID" NOT NULL ENABLE);
                  ALTER TABLE "ANSWER" ADD CONSTRAINT "ANSWER_PK" PRIMARY KEY ("ANSWER_ID")
                  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 
  TABLESPACE "USERS"  ENABLE;
                  ALTER TABLE "ANSWER" MODIFY
                  ("QUESTION_ID" NOT NULL ENABLE);
                  ALTER TABLE "ANSWER" MODIFY
                  ("ANSWER" NOT NULL ENABLE);
                  --------------------------------------------------------
                  --  Constraints for Table BOOK
                  --------------------------------------------------------

                  ALTER TABLE "BOOK" MODIFY
                  ("BOOK_ID" NOT NULL ENABLE);
                  ALTER TABLE "BOOK" MODIFY
                  ("NAME" NOT NULL ENABLE);
                  ALTER TABLE "BOOK" MODIFY
                  ("CREATED_ON" NOT NULL ENABLE);
                  ALTER TABLE "BOOK" MODIFY
                  ("URL" NOT NULL ENABLE);
                  ALTER TABLE "BOOK" MODIFY
                  ("DESCRIPTION" NOT NULL ENABLE);
                  ALTER TABLE "BOOK" MODIFY
                  ("STUDY_ID" NOT NULL ENABLE);
                  ALTER TABLE "BOOK" ADD CONSTRAINT "BOOK_PK" PRIMARY KEY ("BOOK_ID")
                  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  TABLESPACE "USERS"  ENABLE;
                  --------------------------------------------------------
                  --  Constraints for Table QUESTION
                  --------------------------------------------------------

                  ALTER TABLE "QUESTION" MODIFY
                  ("QUESTION_ID" NOT NULL ENABLE);
                  ALTER TABLE "QUESTION" MODIFY
                  ("SCHOOL_ID" NOT NULL ENABLE);
                  ALTER TABLE "QUESTION" MODIFY
                  ("BOOK_ID" NOT NULL ENABLE);
                  ALTER TABLE "QUESTION" MODIFY
                  ("QUESTION" NOT NULL ENABLE);
                  ALTER TABLE "QUESTION" ADD CONSTRAINT "QUESTION_PK" PRIMARY KEY ("QUESTION_ID")
                  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 
  TABLESPACE "USERS"  ENABLE;
                  --------------------------------------------------------
                  --  Constraints for Table SCHOOL
                  --------------------------------------------------------

                  ALTER TABLE "SCHOOL" MODIFY
                  ("SCHOOL_ID" NOT NULL ENABLE);
                  ALTER TABLE "SCHOOL" MODIFY
                  ("NAME" NOT NULL ENABLE);
                  ALTER TABLE "SCHOOL" ADD CONSTRAINT "SCHOOL_PK" PRIMARY KEY ("SCHOOL_ID")
                  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  TABLESPACE "USERS"  ENABLE;
                  --------------------------------------------------------
                  --  Constraints for Table STUDY
                  --------------------------------------------------------

                  ALTER TABLE "STUDY" MODIFY
                  ("STUDY_ID" NOT NULL ENABLE);
                  ALTER TABLE "STUDY" MODIFY
                  ("SCHOOL_ID" NOT NULL ENABLE);
                  ALTER TABLE "STUDY" MODIFY
                  ("NAME" NOT NULL ENABLE);
                  ALTER TABLE "STUDY" ADD CONSTRAINT "STUDY_PK" PRIMARY KEY ("STUDY_ID")
                  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 
  TABLESPACE "USERS"  ENABLE;
                  --------------------------------------------------------
                  --  Constraints for Table USER_PROFILE
                  --------------------------------------------------------

                  ALTER TABLE "USER_PROFILE" MODIFY
                  ("EMAIL" NOT NULL ENABLE);
                  ALTER TABLE "USER_PROFILE" MODIFY
                  ("USERNAME" NOT NULL ENABLE);
                  ALTER TABLE "USER_PROFILE" MODIFY
                  ("FIRST_NAME" NOT NULL ENABLE);
                  ALTER TABLE "USER_PROFILE" MODIFY
                  ("LAST_NAME" NOT NULL ENABLE);
                  ALTER TABLE "USER_PROFILE" MODIFY
                  ("ADMIN" NOT NULL ENABLE);
                  ALTER TABLE "USER_PROFILE" MODIFY
                  ("SCHOOL_ID" NOT NULL ENABLE);
                  ALTER TABLE "USER_PROFILE" MODIFY
                  ("CREATED_ON" NOT NULL ENABLE);
                  ALTER TABLE "USER_PROFILE" MODIFY
                  ("LAST_LOGIN" NOT NULL ENABLE);
                  ALTER TABLE "USER_PROFILE" ADD CONSTRAINT "USER_PROFILE_PK" PRIMARY KEY ("USERNAME")
                  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 
  TABLESPACE "USERS"  ENABLE;
                  --------------------------------------------------------
                  --  Constraints for Table USER_RESPONSE
                  --------------------------------------------------------

                  ALTER TABLE "USER_RESPONSE" MODIFY
                  ("USERNAME" NOT NULL ENABLE);
                  ALTER TABLE "USER_RESPONSE" MODIFY
                  ("QUESTION_ID" NOT NULL ENABLE);
                  ALTER TABLE "USER_RESPONSE" MODIFY
                  ("ANSWER_ID" NOT NULL ENABLE);
                  ALTER TABLE "USER_RESPONSE" MODIFY
                  ("ANSWERED_ON" NOT NULL ENABLE);
                  --------------------------------------------------------
                  --  Constraints for Table USER_STUDY
                  --------------------------------------------------------

                  ALTER TABLE "USER_STUDY" MODIFY
                  ("USERNAME" NOT NULL ENABLE);
                  ALTER TABLE "USER_STUDY" MODIFY
                  ("STUDY_ID" NOT NULL ENABLE);

                  --------------------------------------------------------
                  --  DBMS Scheduler to remove old password reset keys
                  --------------------------------------------------------

                  BEGIN
                        DBMS_SCHEDULER.CREATE_JOB
                                      (
                                job_name => '"KPELSTER"."PASSWORD_RESET_DELETE_OLD_KEYS"',
                                job_type => 'PLSQL_BLOCK',
                                job_action => 'BEGIN DELETE FROM PASSWORD_RESET WHERE REQUEST_DATE + 1 < SYSDATE; END;',
                                number_of_arguments => 0,
                                start_date => TO_TIMESTAMP_TZ
                                      ('2021-11-11 12:47:10.000000000 AMERICA/NEW_YORK','YYYY-MM-DD HH24:MI:SS.FF TZR'),
                                repeat_interval => 'FREQ=DAILY',
                                end_date => TO_TIMESTAMP_TZ
                                      ('2025-11-25 12:51:05.000000000 AMERICA/NEW_YORK','YYYY-MM-DD HH24:MI:SS.FF TZR'),
                                enabled => FALSE,
                                auto_drop => FALSE,
                                comments => 'Deletes rows from PASSWORD_RESET where the request date is at least 24 hours old.');

                        DBMS_SCHEDULER.SET_ATTRIBUTE
                                      ( 
                                name => '"KPELSTER"."PASSWORD_RESET_DELETE_OLD_KEYS"', 
                                attribute => 'store_output', value => TRUE);
                        DBMS_SCHEDULER.SET_ATTRIBUTE
                                      ( 
                                name => '"KPELSTER"."PASSWORD_RESET_DELETE_OLD_KEYS"', 
                                attribute => 'logging_level', value => DBMS_SCHEDULER.LOGGING_OFF);
                          
                        DBMS_SCHEDULER.enable
                                      (
                                name => '"KPELSTER"."PASSWORD_RESET_DELETE_OLD_KEYS"');
                                      END;

--------------------------------------------------------
--  Scheduler job to ping database
--------------------------------------------------------

BEGIN
    DBMS_SCHEDULER.CREATE_JOB (
            job_name => '"KPELSTER"."PING_DATABASE"',
            job_type => 'PLSQL_BLOCK',
            job_action => 'BEGIN

SELECT * FROM USER_PROFILE OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY;

END;',
            number_of_arguments => 0,
            start_date => TO_TIMESTAMP_TZ('2021-11-06 12:58:52.000000000 AMERICA/NEW_YORK','YYYY-MM-DD HH24:MI:SS.FF TZR'),
            repeat_interval => 'FREQ=DAILY; INTERVAL=6',
            end_date => TO_TIMESTAMP_TZ('2025-11-06 12:58:52.000000000 AMERICA/NEW_YORK','YYYY-MM-DD HH24:MI:SS.FF TZR'),
            enabled => FALSE,
            auto_drop => FALSE,
            comments => 'Every 6 days, pings  database by computing a simple select query.');

         
     
 
    DBMS_SCHEDULER.SET_ATTRIBUTE( 
             name => '"KPELSTER"."PING_DATABASE"', 
             attribute => 'store_output', value => TRUE);
    DBMS_SCHEDULER.SET_ATTRIBUTE( 
             name => '"KPELSTER"."PING_DATABASE"', 
             attribute => 'logging_level', value => DBMS_SCHEDULER.LOGGING_OFF);
      
   
  
    
    DBMS_SCHEDULER.enable(
             name => '"KPELSTER"."PING_DATABASE"');
END;

