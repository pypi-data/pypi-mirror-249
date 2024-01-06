from simple_ddl_parser import DDLParser

ddl = """/* updated 2014-2-1 */
CREATE TABLE users(
	Role  enum ('patient','admin','hcp','uap','er','tester','pha', 'lt'),
	/* Please use the MyISAM backend with no foreign keys.*/
) ; 
"""
result = DDLParser(ddl).run(group_by_type=True)

import pprint

pprint.pprint(result)