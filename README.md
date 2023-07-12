# crop-recommendation-model
This is the README.MD file for the model api part of project Crop Recommendation System

The request-response schema is as follows:

First send three parameters: State, District and Season in a POST request.

For this the state must be one of the 35 states we have available (here states also include Union Territories.) and district must correspond to the state. For the list of states and districts refer allowed_parameters.xls.
Also the seasons must be one of the following: Summer, Autumn or Winter. 

In response to this request, provided the parameters were in allowed range a response in JSON will be provided.
It will have two properties: "predictions" and "success":true if request passes. Or just "success":false if the request fails.
The "predictions" will be of Object type - it has the crops as key and the yield as value.

For example:
You can send in a POST request at http://host:port/predict and with parameters State=Some, District=Trial & Season=Demo (this actually won't work because all parameters are wrong.).
And you will get a response like this:
{
  "predictions":{
    "Arhar/Tur": 0.72,
    "Arecanut": 1.41,
    "Tobacco": 2.13
  },
  "success": true
}

Here, the yield is in Tonnes/Hectare.



**The structure of this repo**

Here, we have an app.py file which is the application that you will send requests to as discussed above.
Next we have a requirements.txt file.
And a README.MD which you are reading right now!

As for the folders, the Data folder contains the excel file which holds the entire data. 
Then we have the model folder which contains the model.

