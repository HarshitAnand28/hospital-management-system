from django.shortcuts import render, redirect
from datetime import datetime
from django import http
from patients import models
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
user_model = get_user_model()
import json

# Create your views here.

def public_site(request):
    return render(request, 'public_site/index.html')

@login_required(login_url = "/Patients/login/")
def dashboard(request):
    response = render(request, 'index.html')
    return response

STATE_DISTRICT_DATA = {
    "Andhra Pradesh": [
        "Alluri Sitharama Raju",
        "Anakapalli",
        "Ananthapuramu",
        "Annamayya",
        "Bapatla",
        "Chittoor",
        "Dr. B. R. Ambedkar Konaseema",
        "East Godavari",
        "Eluru",
        "Guntur",
        "Kakinada",
        "Krishna",
        "Kurnool",
        "Nandyal",
        "NTR",
        "Palnadu",
        "Parvathipuram Manyam",
        "Prakasam",
        "Sri Potti Sriramulu Nellore",
        "Sri Sathya Sai",
        "Srikakulam",
        "Tirupati",
        "Visakhapatnam",
        "Vizianagaram",
        "West Godavari",
        "YSR Kadapa",
    ],
    "Arunachal Pradesh": [
        "Anjaw",
        "Bichom",
        "Changlang",
        "Dibang Valley",
        "East Kameng",
        "East Siang",
        "Kamle",
        "Keyi Panyor",
        "Kra Daadi",
        "Kurung Kumey",
        "Leparada",
        "Lohit",
        "Longding",
        "Lower Dibang Valley",
        "Lower Siang",
        "Lower Subansiri",
        "Namsai",
        "Pakke Kessang",
        "Papum Pare",
        "Shi Yomi",
        "Siang",
        "Tawang",
        "Tirap",
        "Upper Siang",
        "Upper Subansiri",
        "West Kameng",
        "West Siang",
        "Itanagar Capital Region",
    ],
    "Assam": [
        "Bajali",
        "Baksa",
        "Barpeta",
        "Biswanath",
        "Bongaigaon",
        "Cachar",
        "Charaideo",
        "Chirang",
        "Darrang",
        "Dhemaji",
        "Dhubri",
        "Dibrugarh",
        "Dima Hasao",
        "Goalpara",
        "Golaghat",
        "Hailakandi",
        "Hojai",
        "Jorhat",
        "Kamrup",
        "Kamrup Metropolitan",
        "Karbi Anglong",
        "Kokrajhar",
        "Lakhimpur",
        "Majuli",
        "Morigaon",
        "Nagaon",
        "Nalbari",
        "Sivasagar",
        "Sonitpur",
        "South Salmara-Mankachar",
        "Tamulpur",
        "Tinsukia",
        "Udalguri",
        "West Karbi Anglong",
        "Sribhumi",
    ],
    "Bihar": [
        "Araria",
        "Arwal",
        "Aurangabad",
        "Banka",
        "Begusarai",
        "Bhagalpur",
        "Bhojpur",
        "Buxar",
        "Darbhanga",
        "East Champaran",
        "Gaya",
        "Gopalganj",
        "Jamui",
        "Jehanabad",
        "Kaimur",
        "Katihar",
        "Khagaria",
        "Kishanganj",
        "Lakhisarai",
        "Madhepura",
        "Madhubani",
        "Munger",
        "Muzaffarpur",
        "Nalanda",
        "Nawada",
        "Patna",
        "Purnia",
        "Rohtas",
        "Saharsa",
        "Samastipur",
        "Saran",
        "Sheikhpura",
        "Sheohar",
        "Sitamarhi",
        "Siwan",
        "Supaul",
        "Vaishali",
        "West Champaran",
    ],
    "Chhattisgarh": [
        "Balod",
        "Baloda Bazar",
        "Balrampur",
        "Bastar",
        "Bemetara",
        "Bijapur",
        "Bilaspur",
        "Dantewada",
        "Dhamtari",
        "Durg",
        "Gariaband",
        "Gaurela-Pendra-Marwahi",
        "Janjgir-Champa",
        "Jashpur",
        "Kabirdham",
        "Khairagarh-Chhuikhadan-Gandai",
        "Kondagaon",
        "Korba",
        "Korea",
        "Mahasamund",
        "Manendragarh-Chirmiri-Bharatpur",
        "Mohla-Manpur-Ambagarh Chowki",
        "Mungeli",
        "Narayanpur",
        "Raigarh",
        "Raipur",
        "Rajnandgaon",
        "Sakti",
        "Sarangarh-Bilaigarh",
        "Sukma",
        "Surajpur",
        "Surguja",
    ],
    "Goa": [
        "North Goa",
        "South Goa",
    ],
    "Gujarat": [
        "Ahmedabad",
        "Amreli",
        "Anand",
        "Aravalli",
        "Banaskantha",
        "Bharuch",
        "Bhavnagar",
        "Botad",
        "Chhota Udepur",
        "Dahod",
        "Dang",
        "Devbhoomi Dwarka",
        "Gandhinagar",
        "Gir Somnath",
        "Jamnagar",
        "Junagadh",
        "Kheda",
        "Kutch",
        "Mahisagar",
        "Mehsana",
        "Morbi",
        "Narmada",
        "Navsari",
        "Panchmahal",
        "Patan",
        "Porbandar",
        "Rajkot",
        "Sabarkantha",
        "Surat",
        "Surendranagar",
        "Tapi",
        "Vadodara",
        "Valsad",
    ],
    "Haryana": [
        "Ambala",
        "Bhiwani",
        "Charkhi Dadri",
        "Faridabad",
        "Fatehabad",
        "Gurugram",
        "Hisar",
        "Jhajjar",
        "Jind",
        "Kaithal",
        "Karnal",
        "Kurukshetra",
        "Mahendragarh",
        "Nuh",
        "Palwal",
        "Panchkula",
        "Panipat",
        "Rewari",
        "Rohtak",
        "Sirsa",
        "Sonipat",
        "Yamunanagar",
    ],
    "Himachal Pradesh": [
        "Bilaspur",
        "Chamba",
        "Hamirpur",
        "Kangra",
        "Kinnaur",
        "Kullu",
        "Lahaul and Spiti",
        "Mandi",
        "Shimla",
        "Sirmaur",
        "Solan",
        "Una",
    ],
    "Jharkhand": [
        "Bokaro",
        "Chatra",
        "Deoghar",
        "Dhanbad",
        "Dumka",
        "East Singhbhum",
        "Garhwa",
        "Giridih",
        "Godda",
        "Gumla",
        "Hazaribagh",
        "Jamtara",
        "Khunti",
        "Koderma",
        "Latehar",
        "Lohardaga",
        "Pakur",
        "Palamu",
        "Ramgarh",
        "Ranchi",
        "Sahibganj",
        "Seraikela-Kharsawan",
        "Simdega",
        "West Singhbhum",
    ],
    "Karnataka": [
        "Bagalkote",
        "Ballari",
        "Belagavi",
        "Bengaluru Rural",
        "Bengaluru Urban",
        "Bidar",
        "Chamarajanagar",
        "Chikkaballapur",
        "Chikkamagaluru",
        "Chitradurga",
        "Dakshina Kannada",
        "Davanagere",
        "Dharwad",
        "Gadag",
        "Hassan",
        "Haveri",
        "Kalaburagi",
        "Kodagu",
        "Kolar",
        "Koppal",
        "Mandya",
        "Mysuru",
        "Raichur",
        "Ramanagara",
        "Shivamogga",
        "Tumakuru",
        "Udupi",
        "Uttara Kannada",
        "Vijayapura",
        "Vijayanagara",
        "Yadgir",
    ],
    "Kerala": [
        "Alappuzha",
        "Ernakulam",
        "Idukki",
        "Kannur",
        "Kasaragod",
        "Kollam",
        "Kottayam",
        "Kozhikode",
        "Malappuram",
        "Palakkad",
        "Pathanamthitta",
        "Thiruvananthapuram",
        "Thrissur",
        "Wayanad",
    ],
    "Madhya Pradesh": [
        "Agar Malwa",
        "Alirajpur",
        "Anuppur",
        "Ashoknagar",
        "Balaghat",
        "Barwani",
        "Betul",
        "Bhind",
        "Bhopal",
        "Burhanpur",
        "Chhatarpur",
        "Chhindwara",
        "Damoh",
        "Datia",
        "Dewas",
        "Dhar",
        "Dindori",
        "Guna",
        "Gwalior",
        "Harda",
        "Indore",
        "Jabalpur",
        "Jhabua",
        "Katni",
        "Khandwa",
        "Khargone",
        "Maihar",
        "Mandla",
        "Mandsaur",
        "Morena",
        "Narmadapuram",
        "Narsinghpur",
        "Neemuch",
        "Niwari",
        "Pandhurna",
        "Panna",
        "Raisen",
        "Rajgarh",
        "Ratlam",
        "Rewa",
        "Sagar",
        "Satna",
        "Sehore",
        "Seoni",
        "Shahdol",
        "Shajapur",
        "Sheopur",
        "Shivpuri",
        "Sidhi",
        "Singrauli",
        "Tikamgarh",
        "Ujjain",
        "Umaria",
        "Vidisha",
        "Mauganj",
    ],
    "Maharashtra": [
        "Ahmednagar",
        "Akola",
        "Amravati",
        "Beed",
        "Bhandara",
        "Buldhana",
        "Chandrapur",
        "Chhatrapati Sambhajinagar",
        "Dharashiv",
        "Dhule",
        "Gadchiroli",
        "Gondia",
        "Hingoli",
        "Jalgaon",
        "Jalna",
        "Kolhapur",
        "Latur",
        "Mumbai City",
        "Mumbai Suburban",
        "Nagpur",
        "Nanded",
        "Nandurbar",
        "Nashik",
        "Palghar",
        "Parbhani",
        "Pune",
        "Raigad",
        "Ratnagiri",
        "Sangli",
        "Satara",
        "Sindhudurg",
        "Solapur",
        "Thane",
        "Wardha",
        "Washim",
        "Yavatmal",
    ],
    "Manipur": [
        "Bishnupur",
        "Chandel",
        "Churachandpur",
        "Imphal East",
        "Imphal West",
        "Jiribam",
        "Kakching",
        "Kamjong",
        "Kangpokpi",
        "Noney",
        "Pherzawl",
        "Senapati",
        "Tamenglong",
        "Tengnoupal",
        "Thoubal",
        "Ukhrul",
    ],
    "Meghalaya": [
        "East Garo Hills",
        "East Jaintia Hills",
        "East Khasi Hills",
        "Eastern West Khasi Hills",
        "North Garo Hills",
        "Ri Bhoi",
        "South Garo Hills",
        "South West Garo Hills",
        "South West Khasi Hills",
        "West Garo Hills",
        "West Jaintia Hills",
        "West Khasi Hills",
    ],
    "Mizoram": [
        "Aizawl",
        "Champhai",
        "Hnahthial",
        "Khawzawl",
        "Kolasib",
        "Lawngtlai",
        "Lunglei",
        "Mamit",
        "Saiha",
        "Saitual",
        "Serchhip",
    ],
    "Nagaland": [
        "Chümoukedima",
        "Dimapur",
        "Kiphire",
        "Kohima",
        "Longleng",
        "Meluri",
        "Mokokchung",
        "Mon",
        "Niuland",
        "Noklak",
        "Peren",
        "Phek",
        "Shamator",
        "Tseminyü",
        "Tuensang",
        "Wokha",
        "Zunheboto",
    ],
    "Odisha": [
        "Angul",
        "Balangir",
        "Balasore",
        "Bargarh",
        "Bhadrak",
        "Boudh",
        "Cuttack",
        "Deogarh",
        "Dhenkanal",
        "Gajapati",
        "Ganjam",
        "Jagatsinghpur",
        "Jajpur",
        "Jharsuguda",
        "Kalahandi",
        "Kandhamal",
        "Kendrapara",
        "Kendujhar",
        "Khordha",
        "Koraput",
        "Malkangiri",
        "Mayurbhanj",
        "Nabarangpur",
        "Nayagarh",
        "Nuapada",
        "Puri",
        "Rayagada",
        "Sambalpur",
        "Subarnapur (Sonepur)",
        "Sundargarh",
    ],
    "Punjab": [
        "Amritsar",
        "Barnala",
        "Bathinda",
        "Faridkot",
        "Fatehgarh Sahib",
        "Fazilka",
        "Ferozepur",
        "Gurdaspur",
        "Hoshiarpur",
        "Jalandhar",
        "Kapurthala",
        "Ludhiana",
        "Malerkotla",
        "Mansa",
        "Moga",
        "Pathankot",
        "Patiala",
        "Rupnagar",
        "Sahibzada Ajit Singh Nagar (Mohali)",
        "Sangrur",
        "Shaheed Bhagat Singh Nagar (Nawanshahr)",
        "Sri Muktsar Sahib",
        "Tarn Taran",
    ],
    "Rajasthan": [
        "Ajmer",
        "Alwar",
        "Anupgarh",
        "Balotra",
        "Banswara",
        "Baran",
        "Barmer",
        "Beawar",
        "Bharatpur",
        "Bhilwara",
        "Bikaner",
        "Bundi",
        "Chittorgarh",
        "Churu",
        "Dausa",
        "Deeg",
        "Dholpur",
        "Didwana–Kuchaman",
        "Dudu",
        "Dungarpur",
        "Gangapur City",
        "Hanumangarh",
        "Jaipur North",
        "Jaipur South",
        "Jaisalmer",
        "Jalore",
        "Jhalawar",
        "Jhunjhunu",
        "Jodhpur East",
        "Jodhpur West",
        "Karauli",
        "Kekri",
        "Khairthal–Tijara",
        "Kota",
        "Kotputli–Behror",
        "Nagaur",
        "Neem Ka Thana",
        "Pali",
        "Phalodi",
        "Pratapgarh",
        "Rajsamand",
        "Salumbar",
        "Sanchore",
        "Sawai Madhopur",
        "Shahpura",
        "Sikar",
        "Sirohi",
        "Sri Ganganagar",
        "Tonk",
        "Udaipur",
    ],
    "Sikkim": [
        "Gangtok",
        "Gyalshing",
        "Mangan",
        "Namchi",
        "Pakyong",
        "Soreng",
    ],
    "Tamil Nadu": [
        "Ariyalur",
        "Chengalpattu",
        "Chennai",
        "Coimbatore",
        "Cuddalore",
        "Dharmapuri",
        "Dindigul",
        "Erode",
        "Kallakurichi",
        "Kancheepuram",
        "Kanniyakumari",
        "Karur",
        "Krishnagiri",
        "Madurai",
        "Mayiladuthurai",
        "Nagapattinam",
        "Namakkal",
        "Nilgiris",
        "Perambalur",
        "Pudukkottai",
        "Ramanathapuram",
        "Ranipet",
        "Salem",
        "Sivaganga",
        "Tenkasi",
        "Thanjavur",
        "Theni",
        "Thoothukudi",
        "Tiruchirappalli",
        "Tirunelveli",
        "Tirupathur",
        "Tiruppur",
        "Tiruvallur",
        "Tiruvannamalai",
        "Tiruvarur",
        "Vellore",
        "Viluppuram",
        "Virudhunagar",
    ],
    "Telangana": [
        "Adilabad",
        "Bhadradri Kothagudem",
        "Hanamkonda",
        "Hyderabad",
        "Jagtial",
        "Jangaon",
        "Jayashankar Bhupalpally",
        "Jogulamba Gadwal",
        "Kamareddy",
        "Karimnagar",
        "Khammam",
        "Komaram Bheem Asifabad",
        "Mahabubabad",
        "Mahabubnagar",
        "Mancherial",
        "Medak",
        "Medchal–Malkajgiri",
        "Mulugu",
        "Nagarkurnool",
        "Nalgonda",
        "Narayanpet",
        "Nirmal",
        "Nizamabad",
        "Peddapalli",
        "Rajanna Sircilla",
        "Ranga Reddy",
        "Sangareddy",
        "Siddipet",
        "Suryapet",
        "Vikarabad",
        "Wanaparthy",
        "Warangal",
        "Yadadri Bhuvanagiri",
    ],
    "Tripura": [
        "Dhalai",
        "Gomati",
        "Khowai",
        "North Tripura",
        "Sepahijala",
        "South Tripura",
        "Unakoti",
        "West Tripura",
    ],
    "Uttar Pradesh": [
        "Agra",
        "Aligarh",
        "Ambedkar Nagar",
        "Amethi",
        "Amroha",
        "Auraiya",
        "Ayodhya",
        "Azamgarh",
        "Baghpat",
        "Bahraich",
        "Ballia",
        "Balrampur",
        "Banda",
        "Barabanki",
        "Bareilly",
        "Basti",
        "Bhadohi (Sant Ravidas Nagar)",
        "Bijnor",
        "Budaun",
        "Bulandshahr",
        "Chandauli",
        "Chitrakoot",
        "Deoria",
        "Etah",
        "Etawah",
        "Farrukhabad",
        "Fatehpur",
        "Firozabad",
        "Gautam Buddha Nagar",
        "Ghaziabad",
        "Ghazipur",
        "Gonda",
        "Gorakhpur",
        "Hamirpur",
        "Hapur",
        "Hardoi",
        "Hathras",
        "Jalaun",
        "Jaunpur",
        "Jhansi",
        "Kannauj",
        "Kanpur Dehat",
        "Kanpur Nagar",
        "Kasganj",
        "Kaushambi",
        "Kushinagar",
        "Lakhimpur Kheri",
        "Lalitpur",
        "Lucknow",
        "Maharajganj",
        "Mahoba",
        "Mainpuri",
        "Mathura",
        "Mau",
        "Meerut",
        "Mirzapur",
        "Moradabad",
        "Muzaffarnagar",
        "Pilibhit",
        "Pratapgarh",
        "Prayagraj",
        "Rae Bareli",
        "Rampur",
        "Saharanpur",
        "Sambhal",
        "Sant Kabir Nagar",
        "Shahjahanpur",
        "Shamli",
        "Shravasti",
        "Siddharthnagar",
        "Sitapur",
        "Sonbhadra",
        "Sultanpur",
        "Unnao",
        "Varanasi",
    ],
    "Uttarakhand": [
        "Almora",
        "Bageshwar",
        "Chamoli",
        "Champawat",
        "Dehradun",
        "Haridwar",
        "Nainital",
        "Pauri Garhwal",
        "Pithoragarh",
        "Rudraprayag",
        "Tehri Garhwal",
        "Udham Singh Nagar",
        "Uttarkashi",
    ],
    "West Bengal": [
        "Alipurduar",
        "Bankura",
        "Birbhum",
        "Cooch Behar",
        "Dakshin Dinajpur",
        "Darjeeling",
        "Hooghly",
        "Howrah",
        "Jalpaiguri",
        "Jhargram",
        "Kalimpong",
        "Kolkata",
        "Malda",
        "Murshidabad",
        "Nadia",
        "North 24 Parganas",
        "Paschim Bardhaman",
        "Paschim Medinipur",
        "Purba Bardhaman",
        "Purba Medinipur",
        "Purulia",
        "South 24 Parganas",
        "Uttar Dinajpur",
    ]
}

def doctorDetails(request):
    dr_id = models.DoctorReg.objects.all().last()
    if dr_id:
        iid = dr_id.id
        dr_id_auto = f"DR_{int(int(iid)+1):03d}"
    else:
        dr_id_auto = "DR_001"

    data = {
        'doctor_ID': dr_id_auto,
        # Serialized JSON passed to template
        'state_district_json': json.dumps(STATE_DISTRICT_DATA)
    }

    if request.method == "POST":
        raw_data = request.POST
        doctor_ID = (raw_data.get('doctor_ID')).strip()

        if doctor_ID is not None:
            try:
                check_dr_id = models.DoctorReg.objects.filter(doctor_ID=doctor_ID)
                if check_dr_id:
                    response_data = {
                        'success': False,
                        'message': "Doctor ID already Exists !"
                    }
                    return http.JsonResponse(response_data, safe=False)
            except Exception as error:
                response_data = {
                    'success': False,
                    'message': str(error)
                }
                return http.JsonResponse(response_data, safe=False)

            name = raw_data.get('name')
            cont_number = raw_data.get('cont_number')
            email = raw_data.get('email')
            gender = raw_data.get('gender')
            specialization = raw_data.get('specialization')
            id_type = raw_data.get('id_type')
            id_number = raw_data.get('id_number')
            photo = request.FILES.get('photo')
            state = raw_data.get('state')
            district = raw_data.get('district')
            pin = raw_data.get('pin')
            address = raw_data.get('address')

            try:
                obj = models.DoctorReg.objects.create(
                    doctor_ID=doctor_ID,
                    name=name,
                    cont_number=cont_number,
                    email=email,
                    gender=gender,
                    specialization=specialization,
                    id_type=id_type,
                    id_number=id_number,
                    photo=photo,
                    state=state,
                    district=district,
                    pin=pin,
                    address=address
                )
                if obj.pk:
                    response_data = {
                        'success': True,
                        'message': "Registration Completed Successfully !"
                    }
                    return http.JsonResponse(response_data, safe=False)
                else:
                    response_data = {
                        'success': False,
                        'message': "Something went Wrong !"
                    }
                    return http.JsonResponse(response_data, safe=False)
            except Exception as error:
                response_data = {
                    'success': False,
                    'message': str(error)
                }
                return http.JsonResponse(response_data, safe=False)

    return render(request, 'doctor/index.html', {'data': data})

def searchDoctorDetails(request):

    data={
        'doctor_Data' : models.DoctorReg.objects.all().values('doctor_ID', 'name', 'specialization')
    }

    if request.method == "POST":
        print(request.POST)
        doctorID=request.POST.get("doctor_ID")
        doctorName=request.POST.get("name")
        specialization=request.POST.get("specialization")

        conditions={}
        if doctorID is not None and doctorID != "":
            conditions['doctor_ID']=doctorID
        if doctorName is not None and doctorName != "":
            conditions['name']=doctorName
        if specialization is not None and specialization != "":
            conditions['specialization']=specialization
        print(conditions)

        if conditions:
            filter_data = models.DoctorReg.objects.filter(**conditions)
            # print(filter_data)

            if filter_data.exists():
                html_data = ''
                sno = 0
                for x in filter_data:
                    sno += 1
                    html_data += '<tr>'
                    html_data += f'<td>{sno}</td>'
                    html_data += f'<td>{x.doctor_ID}</td>'
                    html_data += f'<td>{x.name}</td>'
                    html_data += f'<td>{x.cont_number}</td>'
                    html_data += f'<td>{x.email}</td>'
                    html_data += f'<td>{x.gender}</td>'
                    html_data += f'<td>{x.specialization}</td>'
                    html_data += f'<td>{x.id_type}</td>'
                    html_data += f'<td>{x.id_number}</td>'
                    # html_data += f'<td><img src="{x.photo.url}" height="100" width="100"></td>'
                    if x.photo:
                        html_data += f'<td><img src="{x.photo.url}" height="100" width="100">'
                        html_data += '</td>'
                    else:
                        html_data += '<td>No Photo</td>'
                        
                    html_data += f'<td>{x.address}</td>'
                    html_data += f'<td><div class="d-flex justify-content-center align-items-center"><a href="/Patients/updateDoctorDetails/{x.id}/Update/" class="btn btn-sm btn-primary">Edit</a><button class="btn btn-sm btn-danger" onclick="deleteReg({x.id})">Delete</button></div></td>'
                    html_data += '</tr>'
                    # print(html_data)
                response_data = {
                    'success' : True,
                    'html_data' : html_data
                }
                return http.JsonResponse(response_data, safe=False)
            else:
                response_data ={
                    'success' : False,
                    'message' : 'No records found !'
                }
                return http.JsonResponse(response_data, safe=False)
        else:
            response_data ={
                'success' : False,
                'message' : 'Please select any field!'
            }
            return http.JsonResponse(response_data, safe=False)
    return render(request, 'doctor/service.html', {'data':data})

def deleteDoctorDetails(request, doctor_ID):
    if request.method == "POST":
        try:
            models.DoctorReg.objects.get(id=int(doctor_ID)).delete()
            response_data ={
                'success' : True,
                'message' : 'Doctor details Deleted Successfully !'
            }
            return http.JsonResponse(response_data, safe=False)
        
        except models.DoctorReg.DoesNotExist:
            response_data ={
                'success' : False,
                'message' : 'Doctor details not Exists !'
            }
            return http.JsonResponse(response_data, safe=False)

def updateDoctorDetails(request, doctor_ID):
    state_district_json = json.dumps(STATE_DISTRICT_DATA)

    if doctor_ID is not None:
        if request.method == "GET":
            doctor_data = models.DoctorReg.objects.filter(id=doctor_ID).first()
            context = {
                'doctor_data': doctor_data,
                'state_district_json': state_district_json
            }
            return render(request, 'doctor/update.html', context)
            
        if request.method == "POST":
            raw_data = request.POST
            name=raw_data.get('name')
            cont_number=raw_data.get('cont_number')
            email=raw_data.get('email')
            gender=raw_data.get('gender')
            specialization=raw_data.get('specialization')
            id_type=raw_data.get('id_type')
            id_number=raw_data.get('id_number')
            photo=request.FILES.get('photo')
            state=raw_data.get('state')
            district=raw_data.get('district')
            pin=raw_data.get('pin')
            address=raw_data.get('address')
            try:
                obj = models.DoctorReg.objects.filter(id = doctor_ID).first()
                obj.name=name
                obj.cont_number=cont_number
                obj.email=email
                obj.gender=gender
                obj.specialization=specialization
                obj.id_type=id_type
                obj.id_number=id_number
                obj.photo=photo
                obj.state=state
                obj.district=district
                obj.pin=pin
                obj.address=address
                obj.save()
                if obj.pk:
                    response_data={
                        'success' : True,
                        'message' : "Registration Updated Successfully !"
                    }
                    return http.JsonResponse(response_data, safe=False)
                else:
                    response_data={
                        'success' : False,
                        'message' : "Something went Wrong !"
                    }
                    return http.JsonResponse(response_data, safe=False)
            except Exception as error:
                response_data={
                    'success' : False,
                    'message' : str(error)
                }
                return http.JsonResponse(response_data, safe=False)

def patientDetails(request):

    P_id = models.PatientReg.objects.all().last()
    # print(dr_id)
    if P_id:
       iid = P_id.id
       P_id_auto = f"P_{int(int(iid)+1):03d}"
    else:
        P_id_auto = "P_001"
    # print(P_id)
    data = {
        'patient_ID' : P_id_auto,
        'state_district_json': json.dumps(STATE_DISTRICT_DATA)
    }

    # if request.META.get('HTTP_X_REQUESTED_WITH') == "XMLHttpRequest":
    # print(request)
    # print(request.method)
    if request.method == "POST":
        # print(request.POST)
        raw_data = request.POST
        # print(type(raw_data))
        patient_ID=(raw_data.get('patient_ID')).strip()
        if patient_ID is not None:
            try:
                check_dr_id=models.PatientReg.objects.filter(patient_ID=patient_ID)
                if check_dr_id:
                    response_data={
                        'success' : False,
                        'message' : "Patient ID already Exists !"
                    }
                    return http.JsonResponse(response_data, safe=False)
            except Exception as error:
                response_data={
                    'success' : False,
                    'message' : str(error)
                }
                return http.JsonResponse(response_data, safe=False)

            name=raw_data.get('name')
            cont_number=raw_data.get('cont_number')
            email=raw_data.get('email')
            gender=raw_data.get('gender')
            id_type=raw_data.get('id_type')
            id_number=raw_data.get('id_number')
            photo=request.FILES.get('photo')
            state=raw_data.get('state')
            district=raw_data.get('district')
            pin=raw_data.get('pin')
            address=raw_data.get('address')
            try:
                obj=models.PatientReg.objects.create(
                    patient_ID=patient_ID,
                    name=name,
                    cont_number=cont_number,
                    email=email,
                    gender=gender,
                    id_type=id_type,
                    id_number=id_number,
                    photo=photo,
                    state=state,
                    district=district,
                    pin=pin,
                    address=address
                )
                if obj.pk:
                    response_data={
                        'success' : True,
                        'message' : "Registration Completed Successfully !"
                    }
                    return http.JsonResponse(response_data, safe=False)
                else:
                    response_data={
                        'success' : False,
                        'message' : "Something went Wrong !"
                    }
                    return http.JsonResponse(response_data, safe=False)
            except Exception as error:
                response_data={
                    'success' : False,
                    'message' : str(error)
                }
                return http.JsonResponse(response_data, safe=False)
    return render(request, 'patient/index.html', {'data':data})

def searchPatientsDetails(request):

    data={
        'patient_Data' : models.PatientReg.objects.all().values('patient_ID', 'name', 'cont_number')
    }

    if request.method == "POST":
        # print(request.POST)
        patientID = request.POST.get("patient_ID")
        patientName = request.POST.get("name")
        contNumber = request.POST.get("cont_number")

        conditions={}
        if patientID is not None and patientID != "":
            conditions['patient_ID']=patientID
        if patientName is not None and patientName != "":
            conditions['name']=patientName
        if contNumber is not None and contNumber != "":
            conditions['cont_number']=contNumber
        # print(conditions)

        if conditions:
            filter_data = models.PatientReg.objects.filter(**conditions)     
            # print(filter_data)   

            if filter_data.exists():
                html_data = ''
                sno = 0
                for x in filter_data:
                    sno += 1
                    html_data += '<tr>'
                    html_data += f'<td>{sno}</td>'
                    html_data += f'<td>{x.patient_ID}</td>'
                    html_data += f'<td>{x.name}</td>'
                    html_data += f'<td>{x.cont_number}</td>'
                    html_data += f'<td>{x.email}</td>'
                    html_data += f'<td>{x.gender}</td>'
                    html_data += f'<td>{x.id_type}</td>'
                    html_data += f'<td>{x.id_number}</td>'
                    # html_data += f'<td><img src="{x.photo.url}" height="100" width="100"></td>'
                    if x.photo:
                        html_data += f'<td><img src="{x.photo.url}" height="100" width="100">'
                        html_data += '</td>'
                    else:
                        html_data += '<td>No Photo</td>'
                    html_data += f'<td>{x.address}</td>'
                    html_data += f'<td><div class="d-flex justify-content-center align-items-center"><a href="/Patients/updatePatientDetails/{x.id}/Update/" class="btn btn-sm btn-primary">Edit</a><button class="btn btn-sm btn-danger" onclick="deletePatientData({x.id})">Delete</button></div></td>'
                    html_data += '</tr>'
                    # print(html_data)

                    response_data = {
                        'success' : True,
                        'html_data' : html_data
                    }
                    return http.JsonResponse(response_data, safe=False)
                else:
                    response_data ={
                        'success' : False,
                        'message' : 'No records found !'
                    }
                    return http.JsonResponse(response_data, safe=False)
            else:
                response_data ={
                    'success' : False,
                    'message' : 'Please select any field!'
                }
                return http.JsonResponse(response_data, safe=False)
    return render(request, 'patient/service.html', {'data':data})

def deletePatientDetails(request, patient_ID):
    if request.method == "POST":
        try:
            models.PatientReg.objects.get(id=int(patient_ID)).delete()
            response_data ={
                'success' : True,
                'message' : 'Patient details Deleted Successfully !'
            }
            return http.JsonResponse(response_data, safe=False)
        except models.PatientReg.DoesNotExist:
            response_data ={
                'success' : False,
                'message' : 'Patient details not Exists !'
            }
            return http.JsonResponse(response_data, safe=False)

def updatePatientDetails(request, patient_ID):
    state_district_json = json.dumps(STATE_DISTRICT_DATA)

    if patient_ID is not None:
        if request.method == "GET":
            patient_data = models.PatientReg.objects.filter(id = patient_ID).first()
            context = {
                'patient_data': patient_data,
                'state_district_json': state_district_json
            }
            return render(request, 'patient/update.html', context)
        if request.method == "POST":
            raw_data = request.POST
            name=raw_data.get('name')
            cont_number=raw_data.get('cont_number')
            email=raw_data.get('email')
            gender=raw_data.get('gender')
            id_type=raw_data.get('id_type')
            id_number=raw_data.get('id_number')
            photo=request.FILES.get('photo')
            state=raw_data.get('state')
            district=raw_data.get('district')
            pin=raw_data.get('pin')
            address=raw_data.get('address')
            try:
                obj=models.PatientReg.objects.filter(id = patient_ID).first()
                obj.patient_ID=patient_ID
                obj.name=name
                obj.cont_number=cont_number
                obj.email=email
                obj.gender=gender
                obj.id_type=id_type
                obj.id_number=id_number
                obj.photo=photo
                obj.state=state
                obj.district=district
                obj.pin=pin
                obj.address=address
                obj.save()
                if obj.pk:
                    response_data={
                        'success' : True,
                        'message' : "Registration Updated Successfully !"
                    }
                    return http.JsonResponse(response_data, safe=False)
                else:
                    response_data={
                        'success' : False,
                        'message' : "Something went Wrong !"
                    }
                    return http.JsonResponse(response_data, safe=False)
            except Exception as error:
                response_data={
                    'success' : False,
                    'message' : str(error)
                }
                return http.JsonResponse(response_data, safe=False)
            
def appointmentDetails(request):

    AP_id = models.Appointment.objects.all().last()
    # print(dr_id)
    if AP_id:
       iid = AP_id.id
       AP_id_auto = f"AP_{int(int(iid)+1):03d}"
    else:
        AP_id_auto = "AP_001"
    # print(P_id)
    data = {
        'appointment_ID' : AP_id_auto, 
        'doctor_Data': models.DoctorReg.objects.all(), 
        'patient_Data': models.PatientReg.objects.all()
    }

    # if request.META.get('HTTP_X_REQUESTED_WITH') == "XMLHttpRequest":
        # print(request)
        # print(request.method)
    if request.method == "POST":
        # print(request)
        raw_data = request.POST
        # print(type(raw_data))
        appointment_ID=raw_data.get('appointment_ID').strip()
        if appointment_ID is not None:
            try:
                check_ap_id=models.Appointment.objects.filter(appointment_ID=appointment_ID)
                if check_ap_id:
                    response_data={
                        'success' : False,
                        'message' : "Appointment ID already Exists !"
                    }
                    return http.JsonResponse(response_data, safe=False)
            except Exception as error:
                response_data={
                    'success' : False,
                    'message' : str(error)
                }
                return http.JsonResponse(response_data, safe=False)
            # print(raw_data)

            # -----*-----Condition Start-----*-----
            today_date = datetime.now().date()
            if models.Appointment.objects.filter(appointment_Date=today_date, doctor__doctor_ID=raw_data.get('doctor_ID')).count() == 20:
                response_data={
                    'success' : False,
                    'message' : 'All Slots are full for the selected Doctor'
                }
                return http.JsonResponse(response_data, safe=False)
            if models.Appointment.objects.filter(appointment_Date=today_date, doctor__doctor_ID=raw_data.get('doctor_ID'), patient__patient_ID=raw_data.get('patient_ID') ).exists():
                response_data={
                    'success' : False,
                    'message' : 'You can not book two appointments with same doctor on same date.'
                }
                return http.JsonResponse(response_data, safe=False)
            # -----*-----Conditions End-----*-----
            
            doctor = models.DoctorReg.objects.get(doctor_ID=raw_data.get('doctor_ID'))
            patient = models.PatientReg.objects.get(patient_ID=raw_data.get('patient_ID'))
            appointment_Date = raw_data.get('appointment_Date')
            appointment_Time = raw_data.get('appointment_Time')
            status = raw_data.get('status')
            try:
                obj=models.Appointment.objects.create(
                    appointment_ID=appointment_ID,
                    doctor=doctor,
                    patient=patient,
                    appointment_Date=appointment_Date,
                    appointment_Time=appointment_Time,
                    status=status
                )
                if obj.pk:
                    response_data={
                        'success' : True,
                        'message' : "Registration Completed Successfully !"
                    }
                    return http.JsonResponse(response_data, safe=False)
                else:
                    response_data={
                        'success' : False,
                        'message' : "Something went Wrong !"
                    }
                    return http.JsonResponse(response_data, safe=False)
            except Exception as error:
                response_data={
                    'success' : False,
                    'message' : str(error)
                }
                return http.JsonResponse(response_data, safe=False)
    return render(request, 'appointment/index.html', {'data':data})

def searchAppointmentDetails(request):

    data={
        'appointment_Data' : models.Appointment.objects.all().values('appointment_ID', 'doctor', 'doctor__doctor_ID', 'patient', 'patient__patient_ID', 'appointment_Date')
    }

    if request.method == "POST":
        # print(request.POST)
        appointmentID=request.POST.get("appointment_ID")
        doctorID=request.POST.get("doctor_ID")
        patientID=request.POST.get("patient_ID")
        appointmentDate=request.POST.get("appointment_Date")
        models.Appointment.objects.filter(doctor__doctor_ID=doctorID)
        models.Appointment.objects.filter(patient__patient_ID=patientID)
        # print(doctorID)

        conditions={}
        if appointmentID is not None and appointmentID != "":
            conditions['appointment_ID']=appointmentID
        if doctorID is not None and doctorID != "":
            conditions['doctor__doctor_ID'] = doctorID
        if patientID is not None and patientID != "":
            conditions['patient__patient_ID'] = patientID
        if appointmentDate is not None and appointmentDate != "":
            conditions['appointment_Date']=appointmentDate
        # print(conditions)

        if conditions:
            filter_data = models.Appointment.objects.filter(**conditions)
            print(filter_data)

            if filter_data.exists():
                html_data = ''
                sno = 0
                for x in filter_data:
                    sno += 1
                    html_data += '<tr>'
                    html_data += f'<td>{sno}</td>'
                    html_data += f'<td>{x.appointment_ID}</td>'
                    html_data += f'<td>{x.doctor.doctor_ID}</td>'
                    html_data += f'<td>{x.patient.patient_ID}</td>'
                    html_data += f'<td>{x.appointment_Date}</td>'
                    html_data += '</tr>'
                    # print(html_data)
                    response_data = {
                        'success' : True,
                        'html_data' : html_data
                    }
                    return http.JsonResponse(response_data, safe=False)
                else:
                    response_data ={
                        'success' : False,
                        'message' : 'No records found !'
                    }
                    return http.JsonResponse(response_data, safe=False)
            else:
                response_data ={
                    'success' : False,
                    'message' : 'Please select any field!'
                }
                return http.JsonResponse(response_data, safe=False)        
    return render(request, 'appointment/service.html', {'data':data})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == None or username == "":
            messages.info(request, "Username is required !")
            return redirect('login')
        if password == None or password == "":
            messages.info(request, "Password is required !")
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, "Your account is currently inactive.")
                return redirect('login')
        else:
            messages.info(request, "Either Username or Password is incorrect !")
            return redirect('login')
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'Auth/login.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "Successfully, Logged out !")
    return redirect('login')

def sign_up(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match !")
            return render(request, "Auth/sign_up.html")

        if user_model.objects.filter(username=username).exists():
            messages.error(request, "Username already exists !")
            return render(request, "Auth/sign_up.html")

        if user_model.objects.filter(email=email).exists():
            messages.error(request, "Email already registered !")
            return render(request, "Auth/sign_up.html")

        user_model.objects.create_user(
            username=username,
            first_name=full_name,
            email=email,
            password=password,
        )

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")
    
    return render(request, "Auth/sign_up.html")

def reset_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match !")
            return render(request, "Auth/reset_password.html")

        try:
            user = user_model.objects.get(username=username, email=email)

            user.set_password(new_password)
            user.save()

            messages.success(request, "Password updated successfully. Please login.")
            return redirect("login")

        except user_model.DoesNotExist:
            messages.error(request, "Invalid Username or Email !")

    return render(request, "Auth/reset_password.html")