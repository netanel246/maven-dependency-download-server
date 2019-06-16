# maven-dependency-download
Python code for downloading maven dependencies for offline use  
using flask to create web UI

# Usage:
In route /public_maven_dependency   
in the maven xml pom textArea enter xml pom like this:

    <project>
        <modelVersion>4.0.0</modelVersion>
        <groupId>dummy</groupId>
        <artifactId>dummy</artifactId>
        <version>1.0.0</version>
        
        <dependencies>
            <dependency>
                <groupId>___group id___</groupId>
                <artifactId>___artifact id___</artifactId>
                <version>___version___</version>
            </dependency>
        </dependencies>
    </project>
    
# requirement:
Maven must be installed on the machine  
(and mvn in the PATH environment variable)