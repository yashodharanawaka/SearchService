# Plug-in API
import flask
from nltk import word_tokenize, FreqDist, re
from flask import request, render_template
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.MyDB
collection = db.MyCollection
token_collection = db.TokenCollection

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/search', methods=['GET'])
def retrieve_token_list():
    query_parameter = request.args
    print(query_parameter['context'])  # For debugging
    text = query_parameter.get('context')
    text = re.sub(r'\.|\d+', ' ', text)
    tokenized_text = word_tokenize(text.lower())
    prefixes = ['(', ')', '{', '}', '[', ']', ';', ':', '``', '=', ',', '\'\'', '//', '/']

    for prefix in prefixes:
        tokenized_text = [token for token in tokenized_text if not token.__contains__(prefix)]

    print("tokenized text", tokenized_text)
    freq_list = FreqDist(tokenized_text)
    print("tokenized text", freq_list.keys())
    context_tokens = list(freq_list.keys())
    context_token_indexes = []

    for item in freq_list.items():
        result = list(token_collection.find({'token': item[0]},
                                            {'_id': 0, 'num_of_occurrences': 0,
                                             'logarithm_list_of_probability_to_the_base_total_video_count': 0,
                                             'probability_list': 0,
                                             'product_of_probability_and_log_of_probability': 0,
                                             'entropy': 0}))
        print("result", result)
        if not result:
            continue
        else:
            item_dict = result[0]
            index = [item_dict['1 - entropy'] * item[1]]
            context_token_indexes += index
    print("context tokens", context_token_indexes)
    if not context_token_indexes:
        return render_template("noresult.html")
    if len(context_token_indexes) < 3:
        return render_template("notenoughinfo.html")
    else:
        query_terms = []
        for x in range(3):
            # max_index = max(context_token_indexes)
            # print(max_index)
            max_index_location = context_token_indexes.index((max(context_token_indexes)))
            # print(max_index_location)
            # print("Query Terms: ", context_tokens[max_index_location])
            query_term = context_tokens[max_index_location]
            # query_term.join(query_terms)
            query_terms.append(query_term)
            context_token_indexes.remove(max(context_token_indexes))
        print("Query Terms: ", query_terms)

        query_result = list(
            collection.find({"$and":
                                 [{'tokens': query_terms[0]}, {'tokens': query_terms[1]}, {'tokens': query_terms[2]}]},
                            {'_id': 0,
                             'tokenFrequencies': 0,
                             'tokens': 0}).sort('errorPronePercentage', 1))

        if len(query_result) < 10:
            query_result2 = list(collection.find({'tokens': {'$in': [query_terms[0], query_terms[1], query_terms[2]]}},
                                                 {'_id': 0,
                                                  'tokenFrequencies': 0,
                                                  'tokens': 0}).sort('errorPronePercentage', 1))
        i = 0
        while len(query_result) < 10:
            query_result.append(query_result2[i])
            i += 1

        return render_template("index.html", result=query_result)


app.run()
