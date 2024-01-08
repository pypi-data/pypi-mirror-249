from simple_ddl_parser import DDLParser

ddl = """CREATE TABLE MY_TABLE (
        DATETIME datetime,
        REGIONID varchar
    )  ;
    ALTER TABLE MY_TABLE MODIFY REGIONID integer;
    """
result = DDLParser(ddl).run(group_by_type=True)

import pprint

pprint.pprint(result)