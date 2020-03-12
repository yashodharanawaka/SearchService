def write_token_frequencies_of_each_video_to_my_collection(results, collection):
    tokens = []

    for result in results:
        terms = result['tokens']
        tokens = tokens + result['tokens']
        # works
        for term in terms:
            # print(term + " =>", terms.count(term))
            number_of_occurrences_in_video = terms.count(term)
            collection.update_one({"_id": result['_id']}, {
                "$addToSet": {"tokenFrequencies": {"token": term, "frequency": number_of_occurrences_in_video}}})

    # works
    for token in tokens:
        print(token + " =>", tokens.count(token))
        # NumberOfOccurrencesInDB = tokens.count(token)
