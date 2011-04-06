from __future__ import with_statement
import httplib
import logging


# Setup the logger.
# Add at least one handler to avoid the message "No handlers could be found" on the console.
# The NullHandler is part of the logging module only from Python 2.7 on.

class NullHandler(logging.Handler):
    def emit(self, record):
        pass
        
logger = logging.getLogger("gethipdata")
nullHandler = NullHandler()
logger.addHandler(nullHandler)



def getHipData(hipnr, outputFileName):

    """
    Retrieve Hipparcos epoch photometry from the ESA website.
    The time series together with some header information is 
    written in the specified file.

    Example:
    
    >>> getHipData(23124, "myfile.txt")
    
    @param hipnr: the hipparcos number of the star. 
                  E.g. 1234 or "1234"
    @type hipnr: integer or string
    @param outputFileName: the name of the file that will be created
                           to save the Hipparcos time series
    @type outputFileName: string
    @return: nothing
    
    """

    server = "www.rssd.esa.int"
    webpage = "/hipparcos_scripts/HIPcatalogueSearch.pl?hipepId="

    # Connect to the website, en retrieve the wanted webpage
    
    conn = httplib.HTTPConnection(server)
    conn.request("GET", webpage + str(hipnr))
    response = conn.getresponse()
    if response.reason != "OK":
        logger.critical("Data retrieval for HIP%s not possible. Reason: %s" % (str(hipnr), response.reason))
        return
    else:
        logger.info("Data retrieval for HIP%s: OK" % str(hipnr))
        
    contents = response.read()
    conn.close()
    
    # Parse the webpage, to remove the html codes (line starts with <").
    # Put a "#" in front of the header information, and format nicely.
    # Write to the output file.
    
    with open(outputFileName, 'w') as outputFile:
        for line in contents.split('\n'):
            if line == "": continue
            if not line.startswith("<"):
                if not line[0].isdigit():
                    line = "# " + line
                line = line.replace("|", " ").replace("\r", "")
                outputFile.write(line + "\n")
                