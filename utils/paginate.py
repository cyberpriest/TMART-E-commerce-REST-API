
def Paginate(page:int = 1, limit:int=10):
    skip = (page-1)*limit
    return skip,limit