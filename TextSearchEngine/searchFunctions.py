




def exactWord(word, caseSensitive = False):
    

def AND(*textMatchers):
    def returnFunction(textJson):
        result = [];
        for matcher in textMatchers:
            matchResult = matcher(textJson)
            if matchResult is None:
                return None
            else
                result += matchResult

    return returnFunction


def OR(*textMatchers):
    def returnFunction(textJson):
        result = [];
        for matcher in textMatchers:
            matchResult = matcher(textJson)
            if matchResult is not None:
                result += matchResult
        if len(result) > 0:
            return result
        else
            return None

    return returnFunction









finder = AND(
    OR(
        exactWord("C", caseSensitive = True),
        exactWord("D"),
        partialWord("C")
        ),
    AND(
        exactWord("Mutation testing"),
        partialWord("")
        )
    )


finder(jsonText)


