"""
TODOS:
1. get account under https://workspace-preview.neo4j.io/
2. replace credential details below
"""

class Credentials():
    NEO4J_URI="TODO"
    NEO4J_USERNAME="TODO"
    NEO4J_PASSWORD="TODO"
    #AURA_INSTANCEID="5129b885"
    #AURA_INSTANCENAME="Instance01"

    def uri():
        return Credentials.NEO4J_URI
    
    def username():
        return Credentials.NEO4J_USERNAME
    
    def password():
        return Credentials.NEO4J_PASSWORD
    
    def getNeo4JDatabaseURI():
        return f'neo4j+s://{Credentials.NEO4J_USERNAME}:{Credentials.NEO4J_PASSWORD}@{Credentials.NEO4J_URI}'