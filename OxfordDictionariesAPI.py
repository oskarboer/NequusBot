# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import requests
import json

# TODO: replace with your own app_id and app_key
app_id = '-'
app_key = '-'

def get_meaning(word):
    language = 'en'
    word_id = str(word)

    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})


    # print(r)

    # print("code {}\n".format(r.status_code))

    try:
        meaning = r.json()
    except:
        return "No entry available for " + '"' + str(word) +'"'
    # print(type(meaning))
    out = ''
    for i in meaning["results"][0]["lexicalEntries"][0]["entries"][0]["senses"]:
        out += str(i["definitions"][0]).capitalize() + "\n" + "Usage Examples:\n"
        try:
            for j in i["examples"]:
                out +=  "- " + j["text"] + "\n"
        except:
            out += "None\n"
            pass
    return out

if __name__ == '__main__':
    print(get_meaning("cupcalsroskl;dke"))
