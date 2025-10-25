import re

and_keyword = "AND"
or_keyword = "OR"

binary_boolean_operations = [and_keyword, or_keyword]
reserved_keywords = [and_keyword, or_keyword, "(", ")"]

def query_term_in_entry(term, entry_data):
    return term.lower() in entry_data.lower()

def split_query(query):
    result = re.split(r'\s+|([()])', query.strip())
    return [x for x in result if x] # Remove any empty strings


class SearchQuery:
    query_terms: list[str]
    file_type_filter: str

    search_filenames: bool
    search_ai_data: bool

    def __init__(self, query: str, file_type_filter: str, search_filenames: bool, search_ai_data: bool):
        super().__init__()

        self.query_terms = split_query(query)
        self.file_type_filter = file_type_filter
        self.search_filenames = search_filenames
        self.search_ai_data = search_ai_data

    def does_entry_match_query(self, filename: str, ai_data: str, file_extension: str):
        # Handle inclusion of filenames and ai data
        entry_data: str = ""
        if self.search_filenames:
            entry_data = filename
        if self.search_ai_data:
            entry_data += ai_data

        # Handle file filtering
        if self.file_type_filter is not None:
            if file_extension != self.file_type_filter:
                return False

        # Process boolean query
        return self.eval_boolean_query(self.query_terms, entry_data)

    def eval_boolean_query(self, terms: list[str], entry_data: str):
        # Handle base cases
        if len(terms) == 0:
            return True
        if len(terms) == 1:
            if terms[0] in reserved_keywords:
                return False
            return query_term_in_entry(terms[0], entry_data)

        first_term = terms[0]
        first_expression = [first_term]
        second_expression_start = 1

        if first_term == "(":
            open_parentheses = 0
            i = 0
            for term in terms:
                if term == "(":
                    open_parentheses += 1
                if term == ")":
                    open_parentheses -= 1
                if open_parentheses == 0:
                    break
                i += 1

            if open_parentheses != 0:
                raise ValueError("Mismatched parentheses")
            if i == len(terms) - 1: # Expression includes all terms
                return self.eval_boolean_query(terms[1 : -1], entry_data)

            first_expression = terms[1:i]
            second_expression_start = i + 1
        elif first_term in binary_boolean_operations:
            raise ValueError(first_term + " cannot appear as the first word")

        first_expression_result = self.eval_boolean_query(first_expression, entry_data)

        second_term = terms[second_expression_start]
        if second_term in binary_boolean_operations:
            second_expression_start += 1

        second_expression = terms[second_expression_start:]

        # Handle OR case
        if second_term == or_keyword:
            if first_expression_result:
                return True
            second_expression_result = self.eval_boolean_query(second_expression, entry_data)
            return first_expression_result or second_expression_result

        # Default to AND
        if not first_expression_result:
            return False

        second_expression_result = self.eval_boolean_query(second_expression, entry_data)
        return first_expression_result and second_expression_result