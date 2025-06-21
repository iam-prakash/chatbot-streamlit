#!/usr/bin/env python3
"""
Populate the database with sample Sixt rental terms data for testing
"""

import sqlite3
from app.db import get_db_connection

def populate_sample_data():
    """Add sample rental terms data to the database"""
    
    # Sample data based on real Sixt terms
    sample_data = [
        {
            'country': 'USA',
            'vehicle_type': 'Passenger vehicle',
            'rental_information': '''The minimum age to rent a car is 21 years old. Drivers must have a valid driver's license for at least 1 year. International drivers must present a valid passport and international driving permit. All drivers must be present at the time of vehicle pickup with valid identification documents.

Age restrictions:
- 21-24 years: Additional daily fee applies
- 25+ years: Standard rates apply
- Maximum age: 75 years (may require additional documentation)

Required documents:
- Valid driver's license (held for minimum 1 year)
- Credit card in renter's name
- Valid passport (for international renters)
- International driving permit (for non-US licenses)''',
            
            'payment_information': '''Payment Methods:
- Credit cards: Visa, MasterCard, American Express, Discover
- Debit cards: Not accepted for initial payment
- Cash: Not accepted

Security Deposit:
- Standard vehicles: $200-500 hold on credit card
- Luxury vehicles: $500-1000 hold on credit card
- The hold is released 3-5 business days after vehicle return

Prepaid Rates:
- Payment charged at time of booking
- Non-refundable for no-shows
- Changes allowed up to 24 hours before pickup (with fee)

Pay Later Rates:
- Payment charged at time of pickup
- Credit card authorization required at pickup''',
            
            'protection_conditions': '''Basic Coverage (Included):
- Third Party Liability: $1,000,000
- Personal Accident Insurance: $50,000 per person
- Uninsured Motorist Protection

Optional Coverage:
- Collision Damage Waiver (CDW): Reduces deductible to $0-500
- Personal Effects Coverage: $500 maximum
- Roadside Assistance: Included with CDW

Deductibles:
- Without CDW: $2,500-5,000 depending on vehicle
- With CDW: $0-500 depending on plan

Exclusions:
- Off-road driving
- Racing or speed testing
- Transporting hazardous materials
- Driving under the influence''',
            
            'authorized_driving_areas': '''Domestic Travel:
- All 50 US states and Washington DC
- Alaska and Hawaii: Special restrictions apply
- Puerto Rico: Allowed with advance notice

International Travel:
- Canada: Allowed with advance notice
- Mexico: Not allowed
- Other countries: Contact customer service

Restrictions:
- No off-road driving
- No driving on unpaved roads (except for SUVs)
- No driving in areas with travel warnings
- Must return vehicle to original pickup location unless one-way rental is arranged''',
            
            'extras': '''Available Extras:
- GPS Navigation: $15/day
- Child Safety Seat: $15/day
- Additional Driver: $15/day
- Ski Rack: $10/day
- Roof Box: $20/day
- Prepaid Fuel: $50 flat rate
- Early Return Protection: $25

One-Way Rentals:
- Available between most locations
- One-way fee: $50-200 depending on distance
- Must be arranged in advance

Delivery Service:
- Airport delivery: $25
- Hotel delivery: $35
- After-hours pickup: $50''',
            
            'other_charges_and_taxes': '''Additional Charges:
- Airport concession fee: 10-15% of rental cost
- Vehicle license fee: $2-5/day
- Sales tax: Varies by state (5-10%)
- Fuel service fee: $15 if vehicle returned with less than full tank
- Late return fee: $25/hour after grace period
- Cleaning fee: $50-150 for excessive dirt/damage
- Smoking fee: $250
- Pet fee: $50 (if pets allowed)

Traffic Violations:
- Processing fee: $25 per violation
- Customer responsible for all fines and penalties
- Administrative charges may apply

Tolls:
- Electronic toll pass: $5/day
- Customer responsible for all toll charges
- Processing fee: $5 per toll transaction''',
            
            'vat': 'Sales tax rates vary by state and location. Typical rates range from 5% to 10%. Airport locations may have additional concession fees.'
        },
        
        {
            'country': 'Germany',
            'vehicle_type': 'Passenger vehicle',
            'rental_information': '''The minimum age to rent a car is 18 years old. Drivers must have a valid driver's license for at least 1 year. EU driving licenses are accepted. Non-EU licenses require an international driving permit.

Age restrictions:
- 18-21 years: Limited vehicle selection, higher rates
- 21-25 years: Standard rates with young driver fee
- 25+ years: Standard rates apply

Required documents:
- Valid EU driving license or international permit
- Credit card in renter's name
- Valid passport or EU ID card''',
            
            'payment_information': '''Payment Methods:
- Credit cards: Visa, MasterCard, American Express
- Debit cards: Accepted for German residents
- Cash: Not accepted

Security Deposit:
- Standard vehicles: €200-500 hold
- Luxury vehicles: €500-1000 hold

Prepaid Rates:
- Payment charged at time of booking
- Non-refundable for no-shows
- Changes allowed up to 48 hours before pickup''',
            
            'protection_conditions': '''Basic Coverage (Included):
- Third Party Liability: €7,500,000
- Personal Accident Insurance: €50,000 per person

Optional Coverage:
- Collision Damage Waiver (CDW): Reduces deductible to €0-500
- Super CDW: Zero deductible option
- Personal Effects Coverage: €500 maximum

Deductibles:
- Without CDW: €1,000-2,500 depending on vehicle
- With CDW: €0-500 depending on plan''',
            
            'authorized_driving_areas': '''Domestic Travel:
- All of Germany
- Austria and Switzerland: Allowed
- Other EU countries: Allowed with advance notice

Restrictions:
- No driving in Eastern European countries without advance permission
- Must return vehicle to original pickup location unless one-way rental arranged''',
            
            'extras': '''Available Extras:
- GPS Navigation: €15/day
- Child Safety Seat: €15/day
- Additional Driver: €15/day
- Ski Rack: €10/day
- Prepaid Fuel: €50 flat rate

One-Way Rentals:
- Available within Germany and to neighboring countries
- One-way fee: €50-150 depending on distance''',
            
            'other_charges_and_taxes': '''Additional Charges:
- VAT: 19%
- Airport concession fee: 10-15% of rental cost
- Vehicle license fee: €2-5/day
- Fuel service fee: €15 if vehicle returned with less than full tank
- Late return fee: €25/hour after grace period
- Cleaning fee: €50-150 for excessive dirt/damage
- Smoking fee: €250

Traffic Violations:
- Processing fee: €25 per violation
- Customer responsible for all fines and penalties''',
            
            'vat': '19% VAT applies to all rental charges in Germany.'
        }
    ]
    
    # Connect to database
    conn = get_db_connection('sixt_terms.db')
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM rental_terms")
    
    # Insert sample data
    for data in sample_data:
        cursor.execute("""
            INSERT INTO rental_terms (
                country, vehicle_type, rental_information, payment_information,
                protection_conditions, authorized_driving_areas, extras,
                other_charges_and_taxes, vat
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['country'], data['vehicle_type'], data['rental_information'],
            data['payment_information'], data['protection_conditions'],
            data['authorized_driving_areas'], data['extras'],
            data['other_charges_and_taxes'], data['vat']
        ))
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"✅ Successfully added {len(sample_data)} sample records to database")
    print("📊 Sample data includes:")
    for data in sample_data:
        print(f"  - {data['country']} ({data['vehicle_type']})")

if __name__ == "__main__":
    populate_sample_data() 