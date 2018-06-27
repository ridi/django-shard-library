class QueryFileHandler:
    @staticmethod
    def load_queries(file_name: str):
        file = open(file_name, 'r')
        query = file.read()
        file.close()

        query_list = [s and s.strip() for s in query.split(';')]
        return list(filter(None, query_list))
