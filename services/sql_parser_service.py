class SQLParserService:
    @staticmethod
    def parse_qa_values(sql_statement):
        """Parse values from a QA SQL INSERT statement."""
        if not sql_statement.strip():
            return None
            
        try:
            # Extract values part from SQL statement
            values_part = (
                sql_statement.split("VALUES")[1]
                .strip()
                .strip(";")
                .strip("(")
                .strip(")")
            )
            
            # Split and clean values
            major_id, question, answer = [
                v.strip().strip("'") for v in values_part.split(",", 2)
            ]
            
            return {
                'major_id': major_id,
                'question': question,
                'answer': answer
            }
            
        except (IndexError, ValueError) as e:
            print(f"Error parsing SQL statement: {sql_statement}")
            print(f"Error: {str(e)}")
            return None 