CREATE TABLE major_qa (
    major_id VARCHAR(10) PRIMARY KEY,
    qa_content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (major_id) REFERENCES majors(major_id)
); 

CREATE TABLE major_intro (
    major_id VARCHAR(10) PRIMARY KEY,
    intro_content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (major_id) REFERENCES majors(major_id)
); 