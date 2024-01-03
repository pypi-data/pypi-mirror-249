import pkg_resources

def version():
    msg = "Using piops version: " + pkg_resources.get_distribution("piops").version
    #print(msg)
    return msg