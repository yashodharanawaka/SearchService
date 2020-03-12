import math
from collections import Counter

import numpy


def write_num_of_occurrences_of_each_unique_token_in_whole_db_to_token_collection(results, token_collection):
    tokens = []
    for result in results:
        tokens = tokens + result['tokens']

    unique_tokens = Counter(tokens).keys()

    for unique_token in unique_tokens:
        # print(unique_token)
        num_of_occurrences = tokens.count(unique_token)
        token_collection.update({'token': unique_token},
                                {'token': unique_token, "num_of_occurrences": num_of_occurrences}, upsert=True)


def write_num_of_occurrences_of_each_token_in_a_single_video_to_my_collection(results, collection):
    for result in results:
        terms = result['tokens']
        # works
        for term in terms:
            # print(term + " =>", terms.count(term))
            number_of_occurrences_in_video = terms.count(term)
            collection.update_one({"_id": result['_id']}, {
                "$addToSet": {"tokenFrequencies": {"token": term, "frequency": number_of_occurrences_in_video}}})
    # return number_of_occurrences_in_video


def write_probability_of_a_token_being_included_in_particular_video_tutorial_to_token_collection(collection,
                                                                                                 token_collection):
    # print(-(5 + 8)+9)
    token_list = list(token_collection.find({}, {'_id': 0}))
    # print(token_list)

    for token in token_list:
        # print("Token is:", token['token'])
        total_occurrences = token['num_of_occurrences']
        frequency_list = list(collection.find({'tokenFrequencies.token': token['token']},
                                              {'_id': 0, 'errorPronePercentage': 0,
                                               'tokenFrequencies.token': 0,
                                               'tokenFrequencies': {'$elemMatch': {'token': token['token']}}}))
        # print('frequency_list', frequency_list)
        for item in frequency_list:
            if item.get('tokenFrequencies') is not None:
                single_item = list(item.get('tokenFrequencies'))
                # print("single item: ", single_item)
                single_item = single_item[0]
                # print(single_item)
                occurrences_in_single_video = single_item['frequency']
                print('occurrences_in_single_video:', occurrences_in_single_video)
                print('total_occurrences:', total_occurrences)
                probability_of_occurrence_of_token_in_this_video = occurrences_in_single_video / total_occurrences
                # print('Probability of occurrence of token: ' + token['token'] + '=>',
                #       probability_of_occurrence_of_token_in_this_video)
                m = collection.count_documents({})
                # print(m)
                logarithm_of_probability_to_the_base_total_video_count = math.log(
                    probability_of_occurrence_of_token_in_this_video, m)
                # print(logarithm_of_probability_to_the_base_total_video_count)
                product_of_probability_and_log_of_probability = \
                    probability_of_occurrence_of_token_in_this_video * \
                    logarithm_of_probability_to_the_base_total_video_count
                # print(product_of_probability_and_log_of_probability)
                token_collection.update({'token': token['token']},
                                        {"$push":
                                             {'probability_list': probability_of_occurrence_of_token_in_this_video,
                                              'logarithm_list_of_probability_to_the_base_total_video_count':
                                                  logarithm_of_probability_to_the_base_total_video_count,
                                              'product_of_probability_and_log_of_probability':
                                                  product_of_probability_and_log_of_probability}})
                # print('probability: ', probability_of_occurrence_of_token_in_this_video)
                # print("\n")
            else:
                continue
            print("\n")


def write_entropy_of_a_token_being_included_in_particular_video_tutorial_to_token_collection(token_collection):
    product_array_list = list(token_collection.find({}, {'token': 0, 'num_of_occurrences': 0,
                                                         'logarithm_list_of_probability_to_the_base_total_video_count':
                                                             0,
                                                         'probability_list': 0}))
    print(product_array_list)
    for item in product_array_list:
        if item.get('product_of_probability_and_log_of_probability') is not None:
            # print("inside loop", item)
            product_array = item['product_of_probability_and_log_of_probability']
            # print("product_array: ", product_array)
            # for item_product_array in product_array:
            #     print(item_product_array)
            summation = -(numpy.sum(product_array, dtype=numpy.float64))
            print('ID:', item['_id'])
            print('Summation:', summation)
            token_collection.update({'_id': item['_id']},
                                    {"$set": {'entropy': summation, '1 - entropy': 1 - summation}})
        else:
            summation = 0
            print('Else - Summation:', summation)
            token_collection.update({'_id': item['_id']},
                                    {"$set": {'entropy': summation, '1 - entropy': 1 - summation}})
            continue
