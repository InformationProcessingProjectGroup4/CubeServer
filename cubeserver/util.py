def validate_score(score):
    for j in score:
        if type(j) is int:
            if j < 0:
                raise Exception("ValidationException: negative score not allowed")
        else:
            raise Exception("ValidationException: illegal type in score array, integers only")
    return score
        
        

def validate_level(level):
    for j in level:
        if type(j) is int:
            if j not in [0,1,2]:
                raise Exception("ValidationException: integers 0,1,2 only")
        else:
            raise Exception("ValidationException: illegal type in level array, integers 0,1,2 only")
    return level

