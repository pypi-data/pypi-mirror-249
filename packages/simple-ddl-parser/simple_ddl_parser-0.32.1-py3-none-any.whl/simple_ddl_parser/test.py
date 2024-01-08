from simple_ddl_parser import DDLParser

ddl = """create table event_types ( id number  constraint event_types_id_pk primary key ) ;
    """
result = DDLParser(ddl).run(group_by_type=True)

import pprint

pprint.pprint(result)