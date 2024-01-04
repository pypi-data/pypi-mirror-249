import argparse
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402


YOUR_REPOSITORY_COMPONENT_ID = 221
YOUR_REPOSITORY_COMPONENT_NAME = "Bu 1972 develop sql2code"
DEVELOPER_EMAIL = "roee.s@circ.zone"
object1 = {
    'component_id': YOUR_REPOSITORY_COMPONENT_ID,
    'component_name': YOUR_REPOSITORY_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

logger = Logger.create_logger(object=object1)


class SQL2Code(GenericCRUD):
    def __init__(self, default_schema_name: str):
        super().__init__(default_schema_name=default_schema_name)

    def read_table(self, table: str, columns: list[str] = None) -> dict:
        data_dict = {}
        i = 0
        logger.start(object={"table": table, "columns": columns})

        if columns is None:
            columns = ['*']
        column_str = ','.join(columns)
        schema_name = self.schema_name
        query = f"SELECT {column_str} FROM {schema_name}.{table}"
        logger.info(f"\nthis is query: {query}")
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        logger.info(f"\nthis is rows: {rows}")

        if columns == ['*']:
            columns = [desc[0] for desc in self.cursor.description()]
            logger.info("\nThis is columns name: "', '.join(column_name for column_name in columns))

        while (i < len(rows)):
            j = 0
            for col in columns:
                # logger.info(f"\n{col} -> {rows[i][j]}")
                if i == 0:
                    data_dict[col] = [rows[i][j]]
                else:
                    data_dict[col].append(rows[i][j])
                j += 1
            i += 1

        # logger.info(f"\nData dictionary: {data_dict}")
        logger.end(object={"return value": data_dict})

        return data_dict

    def create_code(self, language, format) -> str:
        if language == "Python" and format == "String":
            res = "Python code as a string"
        elif language == "TypeScript" and format == "String":
            res = "TypeScript code as a string"
        else:
            res = "Unsupported language or format combination"
        logger.info(f"Generated code: {res}")
        return res


# TODO: Do we really need this main function?
def main():
    parser = argparse.ArgumentParser(description="Generate code based on data in a database of Circles Ai")
    parser.add_argument("--schema", help="Database schema can be relationship_type", required=True)
    parser.add_argument("--table", help="Database table can be relationship_type_ml_table", required=True)
    parser.add_argument("--columns", help="Columns to select make sure they comma-separated")
    parser.add_argument("--language", help="Code created in Python or TypeScript", choices=["Python", "TypeScript"])
    parser.add_argument("--format", help="Code format as a String)")

    args = parser.parse_args()

    Sql2code = SQL2Code()
    logger.info("\n---------- Success to connect MySql Circles Ai Server ---------- \n")
    data = Sql2code.read_table(args.schema, args.table, args.columns.split(',') if args.columns else None)
    generated_code = Sql2code.create_code(args.language, args.format)

    logger.info(f"\nThe requested Table:\n{data}")
    logger.info(f"\nGenerated code:\n{generated_code}")


if __name__ == "__main__":
    main()
