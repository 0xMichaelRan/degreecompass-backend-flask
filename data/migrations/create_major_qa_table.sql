DROP TABLE IF EXISTS major_qa;
CREATE TABLE major_qa (
    id SERIAL PRIMARY KEY,
    major_id VARCHAR(10) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (major_id) REFERENCES majors(major_id)
); 

CREATE INDEX idx_major_qa_major_id ON major_qa(major_id);

CREATE TABLE major_intro (
    major_id VARCHAR(10) PRIMARY KEY,
    intro_content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (major_id) REFERENCES majors(major_id)
); 