# API KEY: 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
openai_apikey = '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'
import json
import requests

url = "https://api.openai.com/v1/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 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",
}

#numberOfRooms= str(input('number of bathrooms:'))+'rooms'
numberOfFloors= None
#numberOfBedrooms= str(input('number of bedrooms:'))+'bedrooms'
#numberOfSquareFeetOnPlot= str(input('number of sq feet on plot:'))+'square feet plot'
numberOfBuiltSquareFeet= None
#houseCondition= str(input('house condition:'))+'condition'
readinessToSell= None
listingAddress= None
listingPrice= None
listingPropertyHighlights= None
listingRentLicenseAvailable= None
listingIdealUse= None
listingOpenHouseDates= None
listingAgentContactEmail= None
listingKeyWordsList= None
listingToneOfVoice= None

#characteristics = numberOfBedrooms+numberOfRooms+numberOfSquareFeetOnPlot+houseCondition
characteristics = '2 bed, 2 bathroom, 200 square feet plot'
prompt = 'generate a selling real estate listing based on the following characteristics:'+characteristics+ 'urgency to sell, perfect condition'
data = {
    "model": "text-davinci-003",
    "prompt": prompt,
    "temperature": 1,
    "max_tokens": 50,
}

response = requests.post(url, headers=headers, data=json.dumps(data))
processedResponse = response.json()
listing = processedResponse['choices'][0]['text']
print(listing)
