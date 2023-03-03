def validate_score(score):
    for i,j in enumerate(score):
        if j < 0:
            raise Exception("ValidationException: negative score not allowed")
        try:
            score[i] = int(j)
        except Exception as e:
            raise (f"ValidationException: {str(e)}, improper score format")
    return score
        
        

def validate_level(level):
    for i, j in enumerate(level):
        if j not in [0, 1, 2]:
            raise Exception("Invalid level")
        try:
            level[i] = int(j)
        except Exception as e:
            raise (f"ValidationException: {str(e)}, level array can only contain 0, 1, 2")
    return level
