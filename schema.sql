-- Colleges
CREATE TABLE colleges (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Students
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    college_id INT NOT NULL,
    CONSTRAINT fk_students_college
        FOREIGN KEY (college_id)
        REFERENCES colleges(id)
        ON DELETE CASCADE
);

-- Courses
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL,
    college_id INT NOT NULL,
    CONSTRAINT uq_course_code_college UNIQUE (code, college_id),
    CONSTRAINT fk_courses_college
        FOREIGN KEY (college_id)
        REFERENCES colleges(id)
        ON DELETE CASCADE
);

-- Course Timetables
CREATE TABLE course_timetables (
    id SERIAL PRIMARY KEY,
    course_id INT NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    CONSTRAINT chk_time_range CHECK (start_time < end_time),
    CONSTRAINT fk_timetable_course
        FOREIGN KEY (course_id)
        REFERENCES courses(id)
        ON DELETE CASCADE
);

-- Student Course Enrollments
CREATE TABLE student_courses (
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    CONSTRAINT pk_student_courses PRIMARY KEY (student_id, course_id),
    CONSTRAINT fk_sc_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_sc_course
        FOREIGN KEY (course_id)
        REFERENCES courses(id)
        ON DELETE CASCADE
);

-- Trigger: Prevent timetable clashes for a student
CREATE OR REPLACE FUNCTION prevent_timetable_clash()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM student_courses sc
        JOIN course_timetables ct_existing
            ON ct_existing.course_id = sc.course_id
        JOIN course_timetables ct_new
            ON ct_new.course_id = NEW.course_id
        WHERE sc.student_id = NEW.student_id
          AND ct_existing.day_of_week = ct_new.day_of_week
          AND ct_existing.start_time < ct_new.end_time
          AND ct_new.start_time < ct_existing.end_time
    ) THEN
        RAISE EXCEPTION 'Timetable clash detected for student %', NEW.student_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_timetable_clash
BEFORE INSERT ON student_courses
FOR EACH ROW
EXECUTE FUNCTION prevent_timetable_clash();
