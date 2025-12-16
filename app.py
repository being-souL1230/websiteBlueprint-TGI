import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from database import get_database

COMPANIES = [
    {"id": 1, "name": "Tata Motors", "salary": "₹25,000 - ₹45,000/month", "about": "Leading automobile manufacturer in India with global presence.", "services": "Food, Transportation, Accommodation", "requirements": "ITI/Diploma in Mechanical/Electrical", "latest": True},
    {"id": 2, "name": "Reliance Industries", "salary": "₹30,000 - ₹55,000/month", "about": "India's largest private sector company in petrochemicals and retail.", "services": "Food, Medical Insurance, Housing Allowance", "requirements": "Diploma/B.Tech in Chemical/Petroleum", "latest": True},
    {"id": 3, "name": "Infosys", "salary": "₹35,000 - ₹70,000/month", "about": "Global IT services and consulting company.", "services": "Food, Transportation, Health Insurance", "requirements": "B.Tech/MCA in Computer Science", "latest": True},
    {"id": 4, "name": "Wipro", "salary": "₹32,000 - ₹65,000/month", "about": "IT, consulting and business process services.", "services": "Food, Transportation, Insurance", "requirements": "B.Tech/BCA in IT/Computer Science", "latest": False},
    {"id": 5, "name": "Mahindra & Mahindra", "salary": "₹22,000 - ₹40,000/month", "about": "Multinational automobile manufacturing corporation.", "services": "Food, Transportation, Accommodation", "requirements": "ITI/Diploma in Automobile Engineering", "latest": True},
    {"id": 6, "name": "Larsen & Toubro", "salary": "₹28,000 - ₹50,000/month", "about": "Major technology, engineering, and construction company.", "services": "Food, Accommodation, Medical", "requirements": "Diploma/B.Tech in Civil/Mechanical", "latest": True},
    {"id": 7, "name": "Hindustan Unilever", "salary": "₹20,000 - ₹38,000/month", "about": "Consumer goods company with wide product range.", "services": "Food, Transportation", "requirements": "ITI/Diploma in any stream", "latest": False},
    {"id": 8, "name": "Bajaj Auto", "salary": "₹24,000 - ₹42,000/month", "about": "World's third-largest motorcycle manufacturer.", "services": "Food, Transportation, Housing", "requirements": "ITI/Diploma in Mechanical", "latest": True},
    {"id": 9, "name": "Hero MotoCorp", "salary": "₹23,000 - ₹40,000/month", "about": "World's largest manufacturer of two-wheelers.", "services": "Food, Transportation, Accommodation", "requirements": "ITI/Diploma in Mechanical/Electrical", "latest": False},
    {"id": 10, "name": "Asian Paints", "salary": "₹18,000 - ₹35,000/month", "about": "India's largest paint company.", "services": "Food, Transportation", "requirements": "ITI/Diploma in Chemical", "latest": False},
    {"id": 11, "name": "ITC Limited", "salary": "₹20,000 - ₹40,000/month", "about": "Diversified conglomerate in FMCG, hotels, and agri-business.", "services": "Food, Accommodation, Medical", "requirements": "ITI/Diploma in relevant field", "latest": False},
    {"id": 12, "name": "Maruti Suzuki", "salary": "₹26,000 - ₹48,000/month", "about": "India's largest passenger car manufacturer.", "services": "Food, Transportation, Housing Allowance", "requirements": "ITI/Diploma in Automobile/Mechanical", "latest": True},
    {"id": 13, "name": "Adani Group", "salary": "₹25,000 - ₹50,000/month", "about": "Multinational conglomerate in ports, energy, and infrastructure.", "services": "Food, Accommodation, Transport", "requirements": "Diploma/B.Tech in relevant field", "latest": True},
    {"id": 14, "name": "JSW Steel", "salary": "₹28,000 - ₹52,000/month", "about": "Leading integrated steel manufacturer in India.", "services": "Food, Accommodation, Medical", "requirements": "ITI/Diploma in Metallurgy/Mechanical", "latest": True},
    {"id": 15, "name": "Sun Pharma", "salary": "₹22,000 - ₹45,000/month", "about": "World's fourth-largest specialty generic pharmaceutical company.", "services": "Food, Transportation, Insurance", "requirements": "Diploma/B.Pharma in Pharmacy", "latest": False},
    {"id": 16, "name": "HDFC Bank", "salary": "₹20,000 - ₹40,000/month", "about": "India's largest private sector bank.", "services": "Food Allowance, Insurance", "requirements": "Graduate in Commerce/Banking", "latest": False},
    {"id": 17, "name": "ICICI Bank", "salary": "₹18,000 - ₹38,000/month", "about": "Leading private sector bank with extensive network.", "services": "Food Allowance, Medical", "requirements": "Graduate in any stream", "latest": False},
    {"id": 18, "name": "State Bank of India", "salary": "₹25,000 - ₹55,000/month", "about": "India's largest public sector bank.", "services": "All Government Benefits", "requirements": "Graduate with Bank Exam Qualification", "latest": False},
    {"id": 19, "name": "Tata Steel", "salary": "₹30,000 - ₹55,000/month", "about": "One of the world's most geographically diversified steel producers.", "services": "Food, Accommodation, Township Living", "requirements": "ITI/Diploma in Metallurgy/Mechanical", "latest": True},
    {"id": 20, "name": "Bharat Petroleum", "salary": "₹35,000 - ₹60,000/month", "about": "Fortune 500 oil and gas company.", "services": "Food, Housing, Transportation", "requirements": "Diploma/B.Tech in Chemical/Petroleum", "latest": False},
    {"id": 21, "name": "Indian Oil Corporation", "salary": "₹32,000 - ₹58,000/month", "about": "India's largest commercial oil company.", "services": "All Benefits, Housing", "requirements": "Diploma/B.Tech in Chemical/Mechanical", "latest": False},
    {"id": 22, "name": "HCL Technologies", "salary": "₹30,000 - ₹65,000/month", "about": "Global IT services company.", "services": "Food, Transportation, Insurance", "requirements": "B.Tech/MCA in Computer Science", "latest": False},
    {"id": 23, "name": "Tech Mahindra", "salary": "₹28,000 - ₹60,000/month", "about": "IT services and consulting company.", "services": "Food, Transport, Health Insurance", "requirements": "B.Tech/BCA in IT", "latest": False},
    {"id": 24, "name": "Godrej Group", "salary": "₹18,000 - ₹35,000/month", "about": "Diversified conglomerate in consumer products and real estate.", "services": "Food, Transportation", "requirements": "ITI/Diploma in relevant field", "latest": False},
    {"id": 25, "name": "Dabur India", "salary": "₹16,000 - ₹32,000/month", "about": "Leading FMCG company with focus on Ayurveda.", "services": "Food, Medical", "requirements": "ITI/Diploma in any stream", "latest": False},
    {"id": 26, "name": "Nestle India", "salary": "₹20,000 - ₹40,000/month", "about": "Leading food and beverage company.", "services": "Food, Transportation, Insurance", "requirements": "ITI/Diploma in Food Technology", "latest": False},
    {"id": 27, "name": "Britannia Industries", "salary": "₹18,000 - ₹36,000/month", "about": "One of India's leading food companies.", "services": "Food, Transportation", "requirements": "ITI/Diploma in Food Processing", "latest": False},
    {"id": 28, "name": "Amul", "salary": "₹15,000 - ₹30,000/month", "about": "India's largest dairy cooperative.", "services": "Food, Accommodation", "requirements": "ITI/Diploma in Dairy Technology", "latest": False},
    {"id": 29, "name": "Parle Products", "salary": "₹14,000 - ₹28,000/month", "about": "Leading biscuit and confectionery manufacturer.", "services": "Food, Transportation", "requirements": "ITI/Diploma in any stream", "latest": False},
    {"id": 30, "name": "Havells India", "salary": "₹20,000 - ₹42,000/month", "about": "Leading electrical equipment company.", "services": "Food, Transportation", "requirements": "ITI/Diploma in Electrical", "latest": False},
    {"id": 31, "name": "Voltas", "salary": "₹22,000 - ₹44,000/month", "about": "Engineering and air conditioning company.", "services": "Food, Transportation, Medical", "requirements": "ITI/Diploma in AC/Refrigeration", "latest": False},
    {"id": 32, "name": "Blue Star", "salary": "₹20,000 - ₹40,000/month", "about": "Air conditioning and commercial refrigeration company.", "services": "Food, Transportation", "requirements": "ITI/Diploma in AC/Refrigeration", "latest": False},
    {"id": 33, "name": "Crompton Greaves", "salary": "₹18,000 - ₹38,000/month", "about": "Consumer electrical company.", "services": "Food, Transportation", "requirements": "ITI/Diploma in Electrical", "latest": False},
    {"id": 34, "name": "TVS Motor", "salary": "₹22,000 - ₹42,000/month", "about": "Third-largest motorcycle company in India.", "services": "Food, Transportation, Accommodation", "requirements": "ITI/Diploma in Mechanical", "latest": False},
    {"id": 35, "name": "Ashok Leyland", "salary": "₹24,000 - ₹45,000/month", "about": "Second-largest commercial vehicle manufacturer.", "services": "Food, Transportation, Housing", "requirements": "ITI/Diploma in Automobile/Mechanical", "latest": False},
    {"id": 36, "name": "Eicher Motors", "salary": "₹25,000 - ₹48,000/month", "about": "Manufacturer of Royal Enfield motorcycles.", "services": "Food, Transportation, Medical", "requirements": "ITI/Diploma in Mechanical", "latest": False},
    {"id": 37, "name": "MRF Tyres", "salary": "₹20,000 - ₹40,000/month", "about": "Leading tyre manufacturer in India.", "services": "Food, Accommodation, Transport", "requirements": "ITI/Diploma in Rubber Technology", "latest": False},
    {"id": 38, "name": "Apollo Tyres", "salary": "₹18,000 - ₹38,000/month", "about": "Major tyre manufacturer with global presence.", "services": "Food, Transportation", "requirements": "ITI/Diploma in Rubber/Chemical", "latest": False},
    {"id": 39, "name": "CEAT Tyres", "salary": "₹17,000 - ₹35,000/month", "about": "Leading tyre manufacturer in India.", "services": "Food, Transportation", "requirements": "ITI/Diploma in relevant field", "latest": False},
    {"id": 40, "name": "Bosch India", "salary": "₹28,000 - ₹55,000/month", "about": "German multinational engineering company.", "services": "Food, Transportation, Medical", "requirements": "ITI/Diploma in Mechanical/Electronics", "latest": True},
    {"id": 41, "name": "Siemens India", "salary": "₹30,000 - ₹60,000/month", "about": "Global technology powerhouse.", "services": "Food, Transport, Insurance", "requirements": "Diploma/B.Tech in Electrical/Electronics", "latest": False},
    {"id": 42, "name": "ABB India", "salary": "₹28,000 - ₹55,000/month", "about": "Technology leader in electrification.", "services": "Food, Transportation, Medical", "requirements": "Diploma/B.Tech in Electrical", "latest": False},
    {"id": 43, "name": "Schneider Electric", "salary": "₹26,000 - ₹52,000/month", "about": "Global specialist in energy management.", "services": "Food, Transport, Insurance", "requirements": "Diploma/B.Tech in Electrical/Electronics", "latest": False},
    {"id": 44, "name": "Honeywell India", "salary": "₹32,000 - ₹65,000/month", "about": "Technology and manufacturing company.", "services": "Food, Transport, Full Medical", "requirements": "Diploma/B.Tech in relevant field", "latest": False},
    {"id": 45, "name": "Thermax", "salary": "₹24,000 - ₹48,000/month", "about": "Energy and environment solutions company.", "services": "Food, Transportation", "requirements": "Diploma/B.Tech in Mechanical", "latest": False},
    {"id": 46, "name": "Kirloskar Group", "salary": "₹22,000 - ₹45,000/month", "about": "Engineering and manufacturing conglomerate.", "services": "Food, Accommodation, Transport", "requirements": "ITI/Diploma in Mechanical", "latest": False},
    {"id": 47, "name": "Jindal Steel", "salary": "₹26,000 - ₹50,000/month", "about": "Leading steel manufacturer in India.", "services": "Food, Accommodation, Medical", "requirements": "ITI/Diploma in Metallurgy", "latest": False},
    {"id": 48, "name": "Vedanta Limited", "salary": "₹28,000 - ₹55,000/month", "about": "Natural resources conglomerate.", "services": "Food, Accommodation, Township", "requirements": "Diploma/B.Tech in Mining/Metallurgy", "latest": False},
    {"id": 49, "name": "Hindalco Industries", "salary": "₹25,000 - ₹50,000/month", "about": "Aluminium and copper manufacturing company.", "services": "Food, Accommodation, Medical", "requirements": "ITI/Diploma in Metallurgy/Chemical", "latest": False},
    {"id": 50, "name": "Ultratech Cement", "salary": "₹22,000 - ₹45,000/month", "about": "India's largest cement company.", "services": "Food, Accommodation, Transport", "requirements": "ITI/Diploma in Mechanical/Civil", "latest": False},
    {"id": 51, "name": "ACC Cement", "salary": "₹20,000 - ₹42,000/month", "about": "One of India's leading cement manufacturers.", "services": "Food, Accommodation", "requirements": "ITI/Diploma in Mechanical", "latest": False},
    {"id": 52, "name": "Ambuja Cement", "salary": "₹21,000 - ₹43,000/month", "about": "Major cement manufacturer in India.", "services": "Food, Transportation, Housing", "requirements": "ITI/Diploma in relevant field", "latest": False},
]

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "thegoalindia-secret-key")

def get_sorted_companies():
    latest = sorted([c for c in COMPANIES if c.get('latest')], key=lambda x: x['name'])
    others = sorted([c for c in COMPANIES if not c.get('latest')], key=lambda x: x['name'])
    return latest + others

@app.route('/')
def home():
    sorted_companies = get_sorted_companies()
    latest_companies = [c for c in sorted_companies if c.get('latest')]
    other_companies = [c for c in sorted_companies if not c.get('latest')]
    return render_template('index.html', latest_companies=latest_companies, other_companies=other_companies)

@app.route('/api/companies')
def get_companies():
    return jsonify(get_sorted_companies())

@app.route('/api/company/<int:company_id>')
def get_company(company_id):
    company = next((c for c in COMPANIES if c['id'] == company_id), None)
    if company:
        return jsonify(company)
    return jsonify({"error": "Company not found"}), 404

@app.route('/api/apply', methods=['POST'])
def apply():
    data = request.json
    required_fields = ['name', 'age', 'email', 'phone', 'qualification', 'company_applied']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
    try:
        db = get_database()
        candidates_collection = db.candidates
        
        candidate_data = {
            'name': data['name'],
            'age': int(data['age']),
            'email': data['email'],
            'phone': data['phone'],
            'qualification': data['qualification'],
            'experience': data.get('experience', ''),
            'company_applied': data['company_applied'],
            'created_at': datetime.now()
        }
        
        result = candidates_collection.insert_one(candidate_data)
        
        return jsonify({"success": True, "message": "Application submitted successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
