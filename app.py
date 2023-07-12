# -*- coding: utf-8 -*-
"""
@author: admin
"""


#%%


import flask
import io
from tensorflow import keras
from tensorflow.keras.utils import CustomObjectScope
import datetime
import ibm_boto3
from ibm_botocore.client import Config

#%%
COS_ENDPOINT = "https://s3.eu-gb.cloud-object-storage.appdomain.cloud" 
COS_API_KEY_ID = "B0XS0BRyaRDsf7I_8gLJ8RY9ae19txED5O9_6qqW50M_" 
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/b2676c63df1847c58445280480041071:3d33f5c5-ab9d-4a99-b3fc-2d2218334cc1::" 

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

bucket = cos.Bucket('crop-yield-data')
bucket.download_file('final_model.h5','model/final_model.h5')
# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = None
crops = ['Arecanut', 'Arhar/Tur', 'Bajra', 'Banana', 'Barley', 'Black pepper', 'Cardamom', 'Cashewnut', 'Castor seed', 'Coconut ', 'Coriander', 'Cotton(lint)', 'Cowpea(Lobia)', 'Dry Ginger', 'Dry chillies', 'Garlic', 'Ginger', 'Gram', 'Groundnut', 'Guar seed', 'Horse-gram', 'Jowar', 'Jute', 'Khesari', 'Linseed', 'Maize', 'Masoor', 'Mesta', 'Moong(Green Gram)', 'Moth', 'Niger seed', 'Oilseeds total', 'Onion', 'Other  Rabi pulses', 'Other Cereals', 'Other Kharif pulses', 'Other Summer Pulses', 'Peas & beans (Pulses)', 'Potato', 'Ragi', 'Rapeseed &Mustard', 'Rice', 'Safflower', 'Sannhamp', 'Sesamum', 'Small millets', 'Soyabean', 'Sugarcane', 'Sunflower', 'Sweet potato', 'Tapioca', 'Tobacco', 'Turmeric', 'Urad', 'Wheat', 'other oilseeds']
location_dict = {'assam-baksa': 1, 'assam-barpeta': 2, 'assam-bongaigaon': 3, 'assam-cachar': 4, 'assam-chirang': 5, 'assam-darrang': 6, 'assam-dhemaji': 7, 'assam-dhubri': 8, 'assam-dibrugarh': 9, 'assam-dima hasao': 10, 'assam-goalpara': 11, 'assam-golaghat': 12, 'assam-hailakandi': 13, 'assam-jorhat': 14, 'assam-kamrup': 15, 'assam-kamrup metro': 16, 'assam-karbi anglong': 17, 'assam-karimganj': 18, 'assam-kokrajhar': 19, 'assam-lakhimpur': 20, 'assam-marigaon': 21, 'assam-nagaon': 22, 'assam-nalbari': 23, 'assam-sivasagar': 24, 'assam-sonitpur': 25, 'assam-tinsukia': 26, 'assam-udalguri': 27, 'bihar-araria': 28, 'bihar-arwal': 29, 'bihar-aurangabad': 30, 'bihar-banka': 31, 'bihar-begusarai': 32, 'bihar-bhagalpur': 33, 'bihar-bhojpur': 34, 'bihar-bokaro': 35, 'bihar-buxar': 36, 'bihar-chatra': 37, 'bihar-darbhanga': 38, 'bihar-deoghar': 39, 'bihar-dhanbad': 40, 'bihar-dumka': 41, 'bihar-east singhbum': 42, 'bihar-garhwa': 43, 'bihar-gaya': 44, 'bihar-giridih': 45, 'bihar-godda': 46, 'bihar-gopalganj': 47, 'bihar-gumla': 48, 'bihar-hazaribagh': 49, 'bihar-jamui': 50, 'bihar-jehanabad': 51, 'bihar-kaimur (bhabua)': 52, 'bihar-katihar': 53, 'bihar-khagaria': 54, 'bihar-kishanganj': 55, 'bihar-koderma': 56, 'bihar-lakhisarai': 57, 'bihar-lohardaga': 58, 'bihar-madhepura': 59, 'bihar-madhubani': 60, 'bihar-munger': 61, 'bihar-muzaffarpur': 62, 'bihar-nalanda': 63, 'bihar-nawada': 64, 'bihar-pakur': 65, 'bihar-palamu': 66, 'bihar-pashchim champaran': 67, 'bihar-patna': 68, 'bihar-purbi champaran': 69, 'bihar-purnia': 70, 'bihar-ranchi': 71, 'bihar-rohtas': 72, 'bihar-saharsa': 73, 'bihar-sahebganj': 74, 'bihar-samastipur': 75, 'bihar-saran': 76, 'bihar-sheikhpura': 77, 'bihar-sheohar': 78, 'bihar-sitamarhi': 79, 'bihar-siwan': 80, 'bihar-supaul': 81, 'bihar-vaishali': 82, 'bihar-west singhbhum': 83, 'chandigarh-chandigarh': 84, 'chhattisgarh-balod': 85, 'chhattisgarh-baloda bazar': 86, 'chhattisgarh-balrampur': 87, 'chhattisgarh-bastar': 88, 'chhattisgarh-bemetara': 89, 'chhattisgarh-bijapur': 90, 'chhattisgarh-bilaspur': 91, 'chhattisgarh-dantewada': 92, 'chhattisgarh-dhamtari': 93, 'chhattisgarh-durg': 94, 'chhattisgarh-gariyaband': 95, 'chhattisgarh-janjgir-champa': 96, 'chhattisgarh-jashpur': 97, 'chhattisgarh-kabirdham': 98, 'chhattisgarh-kanker': 99, 'chhattisgarh-kondagaon': 100, 'chhattisgarh-korba': 101, 'chhattisgarh-korea': 102, 'chhattisgarh-mahasamund': 103, 'chhattisgarh-mungeli': 104, 'chhattisgarh-narayanpur': 105, 'chhattisgarh-raigarh': 106, 'chhattisgarh-raipur': 107, 'chhattisgarh-rajnandgaon': 108, 'chhattisgarh-sukma': 109, 'chhattisgarh-surajpur': 110, 'chhattisgarh-surguja': 111, 'dadra and nagar haveli-dadra and nagar haveli': 112, 'daman and diu-daman': 113, 'daman and diu-diu': 114, 'delhi-delhi': 115, 'goa-north goa': 116, 'goa-south goa': 117, 'haryana-ambala': 118, 'haryana-bhiwani': 119, 'haryana-charki dadri': 120, 'haryana-faridabad': 121, 'haryana-fatehabad': 122, 'haryana-gurgaon': 123, 'haryana-hisar': 124, 'haryana-jhajjar': 125, 'haryana-jind': 126, 'haryana-kaithal': 127, 'haryana-karnal': 128, 'haryana-kurukshetra': 129, 'haryana-mahendragarh': 130, 'haryana-mewat': 131, 'haryana-palwal': 132, 'haryana-panchkula': 133, 'haryana-panipat': 134, 'haryana-rewari': 135, 'haryana-rohtak': 136, 'haryana-sirsa': 137, 'haryana-sonipat': 138, 'haryana-yamunanagar': 139, 'himachal pradesh-bilaspur': 140, 'himachal pradesh-chamba': 141, 'himachal pradesh-kangra': 142, 'himachal pradesh-kullu': 143, 'himachal pradesh-mandi': 144, 'himachal pradesh-shimla': 145, 'himachal pradesh-sirmaur': 146, 'himachal pradesh-solan': 147, 'himachal pradesh-una': 148, 'himachal pradesh-hamirpur': 149, 'himachal pradesh-kinnaur': 150, 'himachal pradesh-lahul and spiti': 151, 'jammu and kashmir -jammu': 152, 'jammu and kashmir -samba': 153, 'jammu and kashmir -bandipora': 154, 'jammu and kashmir -doda': 155, 'jammu and kashmir -kathua': 156, 'jammu and kashmir -kishtwar': 157, 'jammu and kashmir -kupwara': 158, 'jammu and kashmir -rajauri': 159, 'jammu and kashmir -reasi': 160, 'jammu and kashmir -udhampur': 161, 'jammu and kashmir -baramulla': 162, 'jammu and kashmir -ganderbal': 163, 'jammu and kashmir -kargil': 164, 'jammu and kashmir -leh ladakh': 165, 'jammu and kashmir -ramban': 166, 'jammu and kashmir -srinagar': 167, 'jammu and kashmir -badgam': 168, 'jammu and kashmir -anantnag': 169, 'jammu and kashmir -kulgam': 170, 'jammu and kashmir -poonch': 171, 'jammu and kashmir -pulwama': 172, 'jammu and kashmir -shopian': 173, 'jharkhand-bokaro': 174, 'jharkhand-chatra': 175, 'jharkhand-deoghar': 176, 'jharkhand-dhanbad': 177, 'jharkhand-dumka': 178, 'jharkhand-east singhbum': 179, 'jharkhand-garhwa': 180, 'jharkhand-giridih': 181, 'jharkhand-godda': 182, 'jharkhand-gumla': 183, 'jharkhand-hazaribagh': 184, 'jharkhand-jamtara': 185, 'jharkhand-khunti': 186, 'jharkhand-koderma': 187, 'jharkhand-latehar': 188, 'jharkhand-lohardaga': 189, 'jharkhand-pakur': 190, 'jharkhand-palamu': 191, 'jharkhand-ramgarh': 192, 'jharkhand-ranchi': 193, 'jharkhand-sahebganj': 194, 'jharkhand-saraikela kharsawan': 195, 'jharkhand-simdega': 196, 'jharkhand-west singhbhum': 197, 'karnataka-bagalkot': 198, 'karnataka-bangalore rural': 199, 'karnataka-belgaum': 200, 'karnataka-bellary': 201, 'karnataka-bengaluru urban': 202, 'karnataka-bijapur': 203, 'karnataka-chamarajanagar': 204, 'karnataka-chikballapur': 205, 'karnataka-chikmagalur': 206, 'karnataka-chitradurga': 207, 'karnataka-dakshin kannad': 208, 'karnataka-davangere': 209, 'karnataka-dharwad': 210, 'karnataka-gadag': 211, 'karnataka-gulbarga': 212, 'karnataka-hassan': 213, 'karnataka-haveri': 214, 'karnataka-kodagu': 215, 'karnataka-kolar': 216, 'karnataka-mandya': 217, 'karnataka-mysore': 218, 'karnataka-ramanagara': 219, 'karnataka-shimoga': 220, 'karnataka-tumkur': 221, 'karnataka-udupi': 222, 'karnataka-uttar kannad': 223, 'karnataka-bidar': 224, 'karnataka-koppal': 225, 'karnataka-raichur': 226, 'karnataka-yadgir': 227, 'kerala-alappuzha': 228, 'kerala-ernakulam': 229, 'kerala-idukki': 230, 'kerala-kannur': 231, 'kerala-kasaragod': 232, 'kerala-kollam': 233, 'kerala-kottayam': 234, 'kerala-kozhikode': 235, 'kerala-malappuram': 236, 'kerala-palakkad': 237, 'kerala-pathanamthitta': 238, 'kerala-thiruvananthapuram': 239, 'kerala-thrissur': 240, 'kerala-wayanad': 241, 'madhya pradesh-agar malwa': 242, 'madhya pradesh-alirajpur': 243, 'madhya pradesh-anuppur': 244, 'madhya pradesh-ashoknagar': 245, 'madhya pradesh-balaghat': 246, 'madhya pradesh-barwani': 247, 'madhya pradesh-bastar': 248, 'madhya pradesh-betul': 249, 'madhya pradesh-bhind': 250, 'madhya pradesh-bhopal': 251, 'madhya pradesh-bilaspur': 252, 'madhya pradesh-burhanpur': 253, 'madhya pradesh-chhatarpur': 254, 'madhya pradesh-chhindwara': 255, 'madhya pradesh-damoh': 256, 'madhya pradesh-dantewada': 257, 'madhya pradesh-datia': 258, 'madhya pradesh-dewas': 259, 'madhya pradesh-dhamtari': 260, 'madhya pradesh-dhar': 261, 'madhya pradesh-dindori': 262, 'madhya pradesh-durg': 263, 'madhya pradesh-guna': 264, 'madhya pradesh-gwalior': 265, 'madhya pradesh-harda': 266, 'madhya pradesh-hoshangabad': 267, 'madhya pradesh-indore': 268, 'madhya pradesh-jabalpur': 269, 'madhya pradesh-janjgir-champa': 270, 'madhya pradesh-jashpur': 271, 'madhya pradesh-jhabua': 272, 'madhya pradesh-kabirdham': 273, 'madhya pradesh-kanker': 274, 'madhya pradesh-katni': 275, 'madhya pradesh-khandwa': 276, 'madhya pradesh-khargone': 277, 'madhya pradesh-korba': 278, 'madhya pradesh-korea': 279, 'madhya pradesh-mahasamund': 280, 'madhya pradesh-mandla': 281, 'madhya pradesh-mandsaur': 282, 'madhya pradesh-morena': 283, 'madhya pradesh-narsinghpur': 284, 'madhya pradesh-neemuch': 285, 'madhya pradesh-panna': 286, 'madhya pradesh-raipur': 287, 'madhya pradesh-raisen': 288, 'madhya pradesh-rajgarh': 289, 'madhya pradesh-rajnandgaon': 290, 'madhya pradesh-ratlam': 291, 'madhya pradesh-rewa': 292, 'madhya pradesh-sagar': 293, 'madhya pradesh-satna': 294, 'madhya pradesh-sehore': 295, 'madhya pradesh-seoni': 296, 'madhya pradesh-shahdol': 297, 'madhya pradesh-shajapur': 298, 'madhya pradesh-sheopur': 299, 'madhya pradesh-shivpuri': 300, 'madhya pradesh-sidhi': 301, 'madhya pradesh-singrauli': 302, 'madhya pradesh-surguja': 303, 'madhya pradesh-tikamgarh': 304, 'madhya pradesh-ujjain': 305, 'madhya pradesh-umaria': 306, 'madhya pradesh-vidisha': 307, 'maharashtra-ahmednagar': 308, 'maharashtra-akola': 309, 'maharashtra-amravati': 310, 'maharashtra-aurangabad': 311, 'maharashtra-beed': 312, 'maharashtra-bhandara': 313, 'maharashtra-buldhana': 314, 'maharashtra-chandrapur': 315, 'maharashtra-dhule': 316, 'maharashtra-gadchiroli': 317, 'maharashtra-gondia': 318, 'maharashtra-hingoli': 319, 'maharashtra-jalgaon': 320, 'maharashtra-jalna': 321, 'maharashtra-kolhapur': 322, 'maharashtra-latur': 323, 'maharashtra-nagpur': 324, 'maharashtra-nanded': 325, 'maharashtra-nandurbar': 326, 'maharashtra-nashik': 327, 'maharashtra-osmanabad': 328, 'maharashtra-palghar': 329, 'maharashtra-parbhani': 330, 'maharashtra-pune': 331, 'maharashtra-raigad': 332, 'maharashtra-ratnagiri': 333, 'maharashtra-sangli': 334, 'maharashtra-satara': 335, 'maharashtra-sindhudurg': 336, 'maharashtra-solapur': 337, 'maharashtra-thane': 338, 'maharashtra-wardha': 339, 'maharashtra-washim': 340, 'maharashtra-yavatmal': 341, 'maharashtra-mumbai': 342, 'maharashtra-mumbai suburban': 343, 'manipur-bishnupur': 344, 'manipur-chandel': 345, 'manipur-churachandpur': 346, 'manipur-imphal east': 347, 'manipur-imphal west': 348, 'manipur-senapati': 349, 'manipur-tamenglong': 350, 'manipur-thoubal': 351, 'manipur-ukhrul': 352, 'meghalaya-east garo hills': 353, 'meghalaya-east jaintia hills': 354, 'meghalaya-east khasi hills': 355, 'meghalaya-north garo hills': 356, 'meghalaya-ri bhoi': 357, 'meghalaya-south garo hills': 358, 'meghalaya-south west garo hills': 359, 'meghalaya-south west khasi hills': 360, 'meghalaya-west garo hills': 361, 'meghalaya-west jaintia hills': 362, 'meghalaya-west khasi hills': 363, 'mizoram-aizawl': 364, 'mizoram-champhai': 365, 'mizoram-kolasib': 366, 'mizoram-lawngtlai': 367, 'mizoram-lunglei': 368, 'mizoram-mamit': 369, 'mizoram-saiha': 370, 'mizoram-serchhip': 371, 'nagaland-dimapur': 372, 'nagaland-kiphire': 373, 'nagaland-kohima': 374, 'nagaland-longleng': 375, 'nagaland-mokokchung': 376, 'nagaland-mon': 377, 'nagaland-peren': 378, 'nagaland-phek': 379, 'nagaland-tuensang': 380, 'nagaland-wokha': 381, 'nagaland-zunheboto': 382, 'odisha-anugul': 383, 'odisha-balangir': 384, 'odisha-baleshwar': 385, 'odisha-bargarh': 386, 'odisha-bhadrak': 387, 'odisha-boudh': 388, 'odisha-cuttack': 389, 'odisha-deogarh': 390, 'odisha-dhenkanal': 391, 'odisha-gajapati': 392, 'odisha-ganjam': 393, 'odisha-jagatsinghapur': 394, 'odisha-jajapur': 395, 'odisha-jharsuguda': 396, 'odisha-kalahandi': 397, 'odisha-kandhamal': 398, 'odisha-kendrapara': 399, 'odisha-kendujhar': 400, 'odisha-khordha': 401, 'odisha-koraput': 402, 'odisha-malkangiri': 403, 'odisha-mayurbhanj': 404, 'odisha-nabarangpur': 405, 'odisha-nayagarh': 406, 'odisha-nuapada': 407, 'odisha-puri': 408, 'odisha-rayagada': 409, 'odisha-sambalpur': 410, 'odisha-sonepur': 411, 'odisha-sundargarh': 412, 'puducherry-mahe': 413, 'puducherry-karaikal': 414, 'puducherry-pondicherry': 415, 'puducherry-yanam': 416, 'punjab-amritsar': 417, 'punjab-barnala': 418, 'punjab-bathinda': 419, 'punjab-faridkot': 420, 'punjab-fatehgarh sahib': 421, 'punjab-fazilka': 422, 'punjab-firozepur': 423, 'punjab-gurdaspur': 424, 'punjab-hoshiarpur': 425, 'punjab-jalandhar': 426, 'punjab-kapurthala': 427, 'punjab-ludhiana': 428, 'punjab-mansa': 429, 'punjab-moga': 430, 'punjab-muktsar': 431, 'punjab-nawanshahr': 432, 'punjab-patiala': 433, 'punjab-rupnagar': 434, 'punjab-s.a.s nagar': 435, 'punjab-sangrur': 436, 'punjab-tarn taran': 437, 'punjab-pathankot': 438, 'rajasthan-ajmer': 439, 'rajasthan-alwar': 440, 'rajasthan-banswara': 441, 'rajasthan-baran': 442, 'rajasthan-bharatpur': 443, 'rajasthan-bhilwara': 444, 'rajasthan-bikaner': 445, 'rajasthan-bundi': 446, 'rajasthan-chittorgarh': 447, 'rajasthan-dausa': 448, 'rajasthan-dholpur': 449, 'rajasthan-dungarpur': 450, 'rajasthan-ganganagar': 451, 'rajasthan-hanumangarh': 452, 'rajasthan-jaipur': 453, 'rajasthan-jaisalmer': 454, 'rajasthan-jalore': 455, 'rajasthan-jhalawar': 456, 'rajasthan-jhunjhunu': 457, 'rajasthan-jodhpur': 458, 'rajasthan-karauli': 459, 'rajasthan-kota': 460, 'rajasthan-nagaur': 461, 'rajasthan-pali': 462, 'rajasthan-pratapgarh': 463, 'rajasthan-rajsamand': 464, 'rajasthan-sawai madhopur': 465, 'rajasthan-sikar': 466, 'rajasthan-sirohi': 467, 'rajasthan-tonk': 468, 'rajasthan-udaipur': 469, 'rajasthan-barmer': 470, 'rajasthan-churu': 471, 'sikkim-east district': 472, 'sikkim-north district': 473, 'sikkim-south district': 474, 'sikkim-west district': 475, 'tamil nadu-coimbatore': 476, 'tamil nadu-cuddalore': 477, 'tamil nadu-dharmapuri': 478, 'tamil nadu-dindigul': 479, 'tamil nadu-erode': 480, 'tamil nadu-kanniyakumari': 481, 'tamil nadu-karur': 482, 'tamil nadu-krishnagiri': 483, 'tamil nadu-madurai': 484, 'tamil nadu-nagapattinam': 485, 'tamil nadu-namakkal': 486, 'tamil nadu-perambalur': 487, 'tamil nadu-pudukkottai': 488, 'tamil nadu-salem': 489, 'tamil nadu-thanjavur': 490, 'tamil nadu-the nilgiris': 491, 'tamil nadu-theni': 492, 'tamil nadu-thiruvarur': 493, 'tamil nadu-tiruchirappalli': 494, 'tamil nadu-tirunelveli': 495, 'tamil nadu-tiruppur': 496, 'tamil nadu-tiruvannamalai': 497, 'tamil nadu-vellore': 498, 'tamil nadu-villupuram': 499, 'tamil nadu-virudhunagar': 500, 'tamil nadu-ariyalur': 501, 'tamil nadu-kanchipuram': 502, 'tamil nadu-ramanathapuram': 503, 'tamil nadu-sivaganga': 504, 'tamil nadu-thiruvallur': 505, 'tamil nadu-tuticorin': 506, 'telangana -adilabad': 507, 'telangana -bhadradri': 508, 'telangana -jagitial': 509, 'telangana -jangoan': 510, 'telangana -jayashankar': 511, 'telangana -jogulamba': 512, 'telangana -kamareddy': 513, 'telangana -karimnagar': 514, 'telangana -khammam': 515, 'telangana -komaram bheem asifabad': 516, 'telangana -mahabubabad': 517, 'telangana -mahbubnagar': 518, 'telangana -mancherial': 519, 'telangana -medak': 520, 'telangana -medchal': 521, 'telangana -mulugu': 522, 'telangana -nagarkurnool': 523, 'telangana -nalgonda': 524, 'telangana -narayanapet': 525, 'telangana -nirmal': 526, 'telangana -nizamabad': 527, 'telangana -peddapalli': 528, 'telangana -rajanna': 529, 'telangana -rangareddi': 530, 'telangana -sangareddy': 531, 'telangana -siddipet': 532, 'telangana -suryapet': 533, 'telangana -vikarabad': 534, 'telangana -wanaparthy': 535, 'telangana -warangal': 536, 'telangana -warangal urban': 537, 'telangana -yadadri': 538, 'tripura-dhalai': 539, 'tripura-gomati': 540, 'tripura-khowai': 541, 'tripura-north tripura': 542, 'tripura-sepahijala': 543, 'tripura-south tripura': 544, 'tripura-unakoti': 545, 'tripura-west tripura': 546, 'uttar pradesh-agra': 547, 'uttar pradesh-aligarh': 548, 'uttar pradesh-allahabad': 549, 'uttar pradesh-almora': 550, 'uttar pradesh-ambedkar nagar': 551, 'uttar pradesh-amethi': 552, 'uttar pradesh-amroha': 553, 'uttar pradesh-auraiya': 554, 'uttar pradesh-azamgarh': 555, 'uttar pradesh-baghpat': 556, 'uttar pradesh-bahraich': 557, 'uttar pradesh-ballia': 558, 'uttar pradesh-balrampur': 559, 'uttar pradesh-banda': 560, 'uttar pradesh-barabanki': 561, 'uttar pradesh-bareilly': 562, 'uttar pradesh-basti': 563, 'uttar pradesh-bijnor': 564, 'uttar pradesh-budaun': 565, 'uttar pradesh-bulandshahr': 566, 'uttar pradesh-chamoli': 567, 'uttar pradesh-chandauli': 568, 'uttar pradesh-chitrakoot': 569, 'uttar pradesh-dehradun': 570, 'uttar pradesh-deoria': 571, 'uttar pradesh-etah': 572, 'uttar pradesh-etawah': 573, 'uttar pradesh-faizabad': 574, 'uttar pradesh-farrukhabad': 575, 'uttar pradesh-fatehpur': 576, 'uttar pradesh-firozabad': 577, 'uttar pradesh-gautam buddha nagar': 578, 'uttar pradesh-ghaziabad': 579, 'uttar pradesh-ghazipur': 580, 'uttar pradesh-gonda': 581, 'uttar pradesh-gorakhpur': 582, 'uttar pradesh-hamirpur': 583, 'uttar pradesh-hapur': 584, 'uttar pradesh-hardoi': 585, 'uttar pradesh-haridwar': 586, 'uttar pradesh-hathras': 587, 'uttar pradesh-jalaun': 588, 'uttar pradesh-jaunpur': 589, 'uttar pradesh-jhansi': 590, 'uttar pradesh-kannauj': 591, 'uttar pradesh-kanpur dehat': 592, 'uttar pradesh-kanpur nagar': 593, 'uttar pradesh-kasganj': 594, 'uttar pradesh-kaushambi': 595, 'uttar pradesh-kheri': 596, 'uttar pradesh-kushi nagar': 597, 'uttar pradesh-lalitpur': 598, 'uttar pradesh-lucknow': 599, 'uttar pradesh-maharajganj': 600, 'uttar pradesh-mahoba': 601, 'uttar pradesh-mainpuri': 602, 'uttar pradesh-mathura': 603, 'uttar pradesh-mau': 604, 'uttar pradesh-meerut': 605, 'uttar pradesh-mirzapur': 606, 'uttar pradesh-moradabad': 607, 'uttar pradesh-muzaffarnagar': 608, 'uttar pradesh-nainital': 609, 'uttar pradesh-pauri garhwal': 610, 'uttar pradesh-pilibhit': 611, 'uttar pradesh-pithoragarh': 612, 'uttar pradesh-pratapgarh': 613, 'uttar pradesh-rae bareli': 614, 'uttar pradesh-rampur': 615, 'uttar pradesh-saharanpur': 616, 'uttar pradesh-sambhal': 617, 'uttar pradesh-sant kabeer nagar': 618, 'uttar pradesh-sant ravidas nagar': 619, 'uttar pradesh-shahjahanpur': 620, 'uttar pradesh-shamli': 621, 'uttar pradesh-shravasti': 622, 'uttar pradesh-siddharth nagar': 623, 'uttar pradesh-sitapur': 624, 'uttar pradesh-sonbhadra': 625, 'uttar pradesh-sultanpur': 626, 'uttar pradesh-tehri garhwal': 627, 'uttar pradesh-udam singh nagar': 628, 'uttar pradesh-unnao': 629, 'uttar pradesh-uttar kashi': 630, 'uttar pradesh-varanasi': 631, 'uttar pradesh-bageshwar': 632, 'uttar pradesh-champawat': 633, 'uttar pradesh-rudra prayag': 634, 'uttarakhand-almora': 635, 'uttarakhand-bageshwar': 636, 'uttarakhand-chamoli': 637, 'uttarakhand-champawat': 638, 'uttarakhand-dehradun': 639, 'uttarakhand-haridwar': 640, 'uttarakhand-nainital': 641, 'uttarakhand-pauri garhwal': 642, 'uttarakhand-pithoragarh': 643, 'uttarakhand-rudra prayag': 644, 'uttarakhand-tehri garhwal': 645, 'uttarakhand-udam singh nagar': 646, 'uttarakhand-uttar kashi': 647, 'west bengal- paraganas north': 648, 'west bengal- paraganas south': 649, 'west bengal-bankura': 650, 'west bengal-birbhum': 651, 'west bengal-coochbehar': 652, 'west bengal-darjeeling': 653, 'west bengal-dinajpur dakshin': 654, 'west bengal-dinajpur uttar': 655, 'west bengal-hooghly': 656, 'west bengal-howrah': 657, 'west bengal-jalpaiguri': 658, 'west bengal-maldah': 659, 'west bengal-medinipur east': 660, 'west bengal-medinipur west': 661, 'west bengal-murshidabad': 662, 'west bengal-nadia': 663, 'west bengal-purba bardhaman': 664, 'west bengal-purulia': 665, 'west bengal-alipurduar': 666, 'west bengal-jhargram\n': 667, 'west bengal-paschim bardhaman\n': 668, 'west bengal-kalimpong\n': 669, 'gujarat-ahmadabad': 670, 'gujarat-amreli': 671, 'gujarat-anand': 672, 'gujarat-aravalli': 673, 'gujarat-banas kantha': 674, 'gujarat-bharuch': 675, 'gujarat-bhavnagar': 676, 'gujarat-botad': 677, 'gujarat-chhotaudepur': 678, 'gujarat-dang': 679, 'gujarat-devbhumi dwarka': 680, 'gujarat-dohad': 681, 'gujarat-gandhinagar': 682, 'gujarat-gir somnath': 683, 'gujarat-jamnagar': 684, 'gujarat-junagadh': 685, 'gujarat-kachchh': 686, 'gujarat-kheda': 687, 'gujarat-mahesana': 688, 'gujarat-mahisagar': 689, 'gujarat-morbi': 690, 'gujarat-narmada': 691, 'gujarat-navsari': 692, 'gujarat-panch mahals': 693, 'gujarat-patan': 694, 'gujarat-porbandar': 695, 'gujarat-rajkot': 696, 'gujarat-sabar kantha': 697, 'gujarat-surat': 698, 'gujarat-surendranagar': 699, 'gujarat-tapi': 700, 'gujarat-vadodara': 701, 'gujarat-valsad': 702, 'andaman and nicobar islands-nicobars': 703, 'andaman and nicobar islands-north and middle andaman': 704, 'andaman and nicobar islands-south andamans': 705, 'andhra pradesh-anantapur': 706, 'andhra pradesh-east godavari': 707, 'andhra pradesh-krishna': 708, 'andhra pradesh-vizianagaram': 709, 'andhra pradesh-west godavari': 710, 'andhra pradesh-adilabad': 711, 'andhra pradesh-chittoor': 712, 'andhra pradesh-guntur': 713, 'andhra pradesh-kadapa': 714, 'andhra pradesh-karimnagar': 715, 'andhra pradesh-khammam': 716, 'andhra pradesh-kurnool': 717, 'andhra pradesh-mahbubnagar': 718, 'andhra pradesh-medak': 719, 'andhra pradesh-nalgonda': 720, 'andhra pradesh-nizamabad': 721, 'andhra pradesh-prakasam': 722, 'andhra pradesh-rangareddi': 723, 'andhra pradesh-spsr nellore': 724, 'andhra pradesh-srikakulam': 725, 'andhra pradesh-visakhapatanam': 726, 'andhra pradesh-warangal': 727, 'andhra pradesh-hyderabad': 728, 'arunachal pradesh-dibang valley': 729, 'arunachal pradesh-east kameng': 730, 'arunachal pradesh-east siang': 731, 'arunachal pradesh-lohit': 732, 'arunachal pradesh-longding': 733, 'arunachal pradesh-lower dibang valley': 734, 'arunachal pradesh-lower subansiri': 735, 'arunachal pradesh-namsai': 736, 'arunachal pradesh-papum pare': 737, 'arunachal pradesh-siang': 738, 'arunachal pradesh-tirap': 739, 'arunachal pradesh-upper siang': 740, 'arunachal pradesh-upper subansiri': 741, 'arunachal pradesh-west siang': 742, 'arunachal pradesh-anjaw': 743, 'arunachal pradesh-changlang': 744, 'arunachal pradesh-kra daadi': 745, 'arunachal pradesh-kurung kumey': 746, 'arunachal pradesh-tawang': 747, 'arunachal pradesh-west kameng': 748}
path_to_model = "model/final_model.h5"


#%%


@app.route("/predict", methods=["GET"])
def predict():
    
    data = {"success": False}
    
    if flask.request.method == "GET":
      try:
        params = flask.request.args
        if (params != None):
            params = prepare_data(params)
            #model should predict here and we will send the prediction 
            predictions = {}
            print("params", params)
            i = 1
            for crop in crops:
                new_params = [[i]+params]
                results = model.predict(new_params)
                if results:
                    predictions[crop] = float(results[0,0])
                else:
                    new_params = [[i] + [1, 1, 1] + params[-1:]]
                    results = model.predict(new_params)
                    if results:
                        print(crop, results)
                        predictions[crop] = float(results[0,0])
                    else:
                        predictions[crop] = 0.0
                #print(crop, predictions[crop])
                i+=1
            data["predictions"] = predictions
            data["success"] = True
      except Exception as e:
            print(e)

    # return the data dictionary as a JSON response
    return flask.jsonify(data)




#%%
import sys
sys.path.insert(1, 'model/')
from CustomLayer import MyLayer
def load_model():
    global model
    with CustomObjectScope({'MyLayer': MyLayer}):
        model = keras.models.load_model(path_to_model) #we'll load our saved keras model here once it's built




#%%

def prepare_data(params):
    #we prepare our data here
    location = (params.get('State')+'-'+params.get('District')).lower()
    season = params.get('Season')
    year = datetime.datetime.now().year
    row = []
    if season == "Summer":
        row.extend([1, 0, 0])
    elif season == "Winter":
        row.extend([0, 1, 0])
    elif season == "Autumn":
        row.extend([0, 0, 1])
    else:
        return None
    global location_dict
    if location in location_dict.keys():
        row.append(location_dict[location])
    else:
        return None
    return row
#%%


print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
load_model()



#%%

