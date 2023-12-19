import re

def parse_major_data(file_path):
    # Initialize variables to store current category and subject
    current_category = None
    current_subject = None
    
    # SQL statements storage
    category_inserts = []
    subject_inserts = []
    major_inserts = []
    
    # Regular expressions for matching different levels
    category_pattern = r'^(\d{2})学科门类：(.+)$'
    subject_pattern = r'^(\d{4})\s+(.+)类$'
    major_pattern = r'^(\d{6}[TK]*)\s+(.+)(?:\（\d{4}\）|\（.+\）)?$'
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
                
            # Try to match category
            category_match = re.match(category_pattern, line)
            if category_match:
                category_id, category_name = category_match.groups()
                current_category = category_id
                category_inserts.append(
                    f"INSERT INTO categories (category_id, category_name) VALUES ('{category_id}', '{category_name}');"
                )
                continue
                
            # Try to match subject
            subject_match = re.match(subject_pattern, line)
            if subject_match:
                subject_id, subject_name = subject_match.groups()
                current_subject = subject_id
                subject_inserts.append(
                    f"INSERT INTO subjects (subject_id, category_id, subject_name) "
                    f"VALUES ('{subject_id}', '{current_category}', '{subject_name}');"
                )
                continue
                
            # Try to match major
            major_match = re.match(major_pattern, line)
            if major_match:
                major_id, major_name = major_match.groups()
                # Remove any notes in parentheses from major name
                major_name = re.sub(r'\（.*?\）', '', major_name).strip()
                major_inserts.append(
                    f"INSERT INTO majors (major_id, subject_id, major_name) "
                    f"VALUES ('{major_id}', '{current_subject}', '{major_name}');"
                )
    
    # Return all SQL statements
    return {
        'categories': category_inserts,
        'subjects': subject_inserts,
        'majors': major_inserts
    }

def write_sql_file(sql_statements, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write CREATE TABLE statements
        f.write("""
CREATE TABLE categories (
    category_id VARCHAR(2) PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

CREATE TABLE subjects (
    subject_id VARCHAR(4) PRIMARY KEY,
    category_id VARCHAR(2),
    subject_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE majors (
    major_id VARCHAR(10) PRIMARY KEY,
    subject_id VARCHAR(4),
    major_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);
\n""")
        
        # Write INSERT statements
        for category_sql in sql_statements['categories']:
            f.write(category_sql + '\n')
        f.write('\n')
        
        for subject_sql in sql_statements['subjects']:
            f.write(subject_sql + '\n')
        f.write('\n')
        
        for major_sql in sql_statements['majors']:
            f.write(major_sql + '\n')

# Usage
sql_statements = parse_major_data('./data/major_data.txt')
write_sql_file(sql_statements, './data/output_major_data.sql')
