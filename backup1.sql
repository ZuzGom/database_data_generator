-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-12-06 08:11:22.069

-- tables
-- Table: CourseAttendance
CREATE TABLE CourseAttendance (
    EventID int  NOT NULL,
    StudentID int  NOT NULL
);

-- Table: CourseEnrollment
CREATE TABLE CourseEnrollment (
    EnrollID int  NOT NULL,
    CourseID int  NOT NULL,
    StudentID int  NOT NULL,
    DateOfEnrollment datetime  NOT NULL,
    Paid money  NOT NULL,
    CONSTRAINT CourseEnrollment_pk PRIMARY KEY  (EnrollID)
);

-- Table: CourseHist
CREATE TABLE CourseHist (
    EventID int  NOT NULL,
    CourseID int  NOT NULL,
    EventDate datetime  NOT NULL,
    ModuleID int  NOT NULL,
    DaySpan int  NOT NULL,
    CONSTRAINT CourseHist_pk PRIMARY KEY  (EventID)
);

-- Table: Courses
CREATE TABLE Courses (
    CourseID int  NOT NULL,
    Title int  NOT NULL,
    Type int  NOT NULL,
    LimitOfParticipants int  NOT NULL,
    NumOfModules int  NOT NULL,
    Price money  NOT NULL,
    CONSTRAINT Courses_pk PRIMARY KEY  (CourseID)
);

-- Table: Lecturer
CREATE TABLE Lecturer (
    LecturerID int  NOT NULL,
    FirstName int  NOT NULL,
    LastName int  NOT NULL,
    DateOfBirth int  NOT NULL,
    Gender int  NOT NULL,
    Title int  NOT NULL,
    CONSTRAINT Lecturer_pk PRIMARY KEY  (LecturerID)
);

-- Table: Locations
CREATE TABLE Locations (
    LocationID int  NOT NULL,
    Buidling nvarchar(max)  NOT NULL,
    Class nvarchar(max)  NOT NULL,
    CONSTRAINT Locations_pk PRIMARY KEY  (LocationID)
);

-- Table: Modules
CREATE TABLE Modules (
    ModuleID int  NOT NULL,
    CourseID int  NOT NULL,
    Link int  NOT NULL,
    LocationID int  NOT NULL,
    LecturerID int  NOT NULL,
    TranslatorID int  NOT NULL,
    CONSTRAINT Modules_pk PRIMARY KEY  (ModuleID)
);

-- Table: RegHist
CREATE TABLE RegHist (
    UserID int  NOT NULL,
    DateOfRegister datetime  NOT NULL,
    CONSTRAINT RegHist_pk PRIMARY KEY  (UserID)
);

-- Table: Student
CREATE TABLE Student (
    StudentID int  NOT NULL,
    FirstName nvarchar(max)  NOT NULL,
    LastName nvarchar(max)  NOT NULL,
    DateOfBirth date  NOT NULL,
    Gender char(1)  NOT NULL,
    Address int  NOT NULL,
    CONSTRAINT StudentID PRIMARY KEY  (StudentID)
);

-- Table: Studies
CREATE TABLE Studies (
    StudyID int  NOT NULL,
    Name nvarchar(max)  NOT NULL,
    CoordinatorID int  NOT NULL,
    Price int  NOT NULL,
    LimitOfParticipants int  NOT NULL,
    CONSTRAINT Studies_pk PRIMARY KEY  (StudyID)
);

-- Table: StudyAttendance
CREATE TABLE StudyAttendance (
    EventID int  NOT NULL,
    StudentId int  NOT NULL
);

-- Table: StudyCourses
CREATE TABLE StudyCourses (
    CourseID int  NOT NULL,
    Title int  NOT NULL,
    Type int  NOT NULL,
    LimitOfParticipants int  NOT NULL,
    NumOfModules int  NOT NULL,
    Price money  NOT NULL,
    CONSTRAINT StudyCourses_pk PRIMARY KEY  (CourseID)
);

-- Table: StudyDetails
CREATE TABLE StudyDetails (
    StudyID int  NOT NULL,
    CourseID int  NOT NULL,
    CoordinatorID int  NOT NULL
);

-- Table: StudyEnrollment
CREATE TABLE StudyEnrollment (
    EnrollID int  NOT NULL,
    CourseID int  NOT NULL,
    StudentID int  NOT NULL,
    DateOfEnrollment datetime  NOT NULL,
    Paid money  NOT NULL,
    CONSTRAINT StudyEnrollment_pk PRIMARY KEY  (EnrollID)
);

-- Table: StudyHist
CREATE TABLE StudyHist (
    EventID int  NOT NULL,
    CourseID int  NOT NULL,
    EventDate datetime  NOT NULL,
    ModuleID int  NOT NULL,
    DaySpan int  NOT NULL,
    CONSTRAINT StudyHist_pk PRIMARY KEY  (EventID)
);

-- Table: StudyModules
CREATE TABLE StudyModules (
    ModuleID int  NOT NULL,
    CourseID int  NOT NULL,
    Link int  NOT NULL,
    LocationID int  NOT NULL,
    LecturerID int  NOT NULL,
    TranslatorID int  NOT NULL,
    CONSTRAINT StudyModules_pk PRIMARY KEY  (ModuleID)
);

-- Table: Translator
CREATE TABLE Translator (
    TranslatorID int  NOT NULL,
    FirstName int  NOT NULL,
    LastName int  NOT NULL,
    CONSTRAINT Translator_pk PRIMARY KEY  (TranslatorID)
);

-- Table: WebinarPurhcase
CREATE TABLE WebinarPurhcase (
    PurchaseID int  NOT NULL,
    WebinarID int  NOT NULL,
    DateOfPurchase datetime  NOT NULL,
    UserID int  NOT NULL,
    Paid money  NOT NULL,
    CONSTRAINT WebinarPurhcase_pk PRIMARY KEY  (PurchaseID)
);

-- Table: Webinars
CREATE TABLE Webinars (
    WebinarID int  NOT NULL,
    Title int  NOT NULL,
    Link int  NOT NULL,
    Price money  NOT NULL,
    Translator int  NOT NULL,
    CONSTRAINT Webinars_pk PRIMARY KEY  (WebinarID)
);

-- End of file.

