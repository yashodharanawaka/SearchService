from pymongo import MongoClient

from DatabaseUpdator import write_num_of_occurrences_of_each_unique_token_in_whole_db_to_token_collection, \
    write_num_of_occurrences_of_each_token_in_a_single_video_to_my_collection, \
    write_probability_of_a_token_being_included_in_particular_video_tutorial_to_token_collection, \
    write_entropy_of_a_token_being_included_in_particular_video_tutorial_to_token_collection

print("*********Python Script call is a success!****************")


def main():
    client = MongoClient('localhost', 27017)
    db = client.MyDB
    collection = db.MyCollection
    token_collection = db.TokenCollection
    results = list(collection.find({}, {"errorPronePercentage": 0, "tokenFrequencies": 0}))

    write_num_of_occurrences_of_each_unique_token_in_whole_db_to_token_collection(results, token_collection)

    write_num_of_occurrences_of_each_token_in_a_single_video_to_my_collection(results, collection)

    write_probability_of_a_token_being_included_in_particular_video_tutorial_to_token_collection(collection,
                                                                                                 token_collection)

    write_entropy_of_a_token_being_included_in_particular_video_tutorial_to_token_collection(token_collection)


if __name__ == "__main__":
    main()
