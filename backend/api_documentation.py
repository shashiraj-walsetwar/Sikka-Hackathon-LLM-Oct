from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class APIEndpoint:
    name: str
    method: str
    path: str
    description: str
    params: Dict[str, str]  # parameter name -> description
    required_params: List[str]
    response_fields: List[str]
    sortBy: List[str]

class APIDocumentation:
    def __init__(self):
        self.endpoints = {
            "procedure_codes": APIEndpoint(
                name="Procedure Codes",
                method="GET",
                path="/v4/procedure_codes",
                description="Returns procedure codes data from practice",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "procedure_code": "procedure code from appointments",
                    "practice_id": "practice id of office",
                    "procedure_code_category": "As per the procedure code category in API response"
                },
                required_params=["request_key"],
                response_fields=[
                    "procedure_code",
                    "procedure_code_description",
                    "abbreaviation",
                    "procedure_code_category"
                ],
                sortBy=["procedure_code"]
            ),
            
            "payment_types": APIEndpoint(
                name="Payment Types",
                method="GET",
                path="/v4/payment_types",
                description="Returns payment types from practice",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "practice_id": "practice id of office",
                    "code": "payment type code in practice management system",
                    "customer_id": "customer id of office"
                },
                required_params=["request_key"],
                response_fields=[
                    "code",
                    "description",
                    "is_adjustment_type",
                    "is_insurance_type"
                ],
                sortBy=["code"]
            ),

            "patient_balance": APIEndpoint(
                name="Patient Balance",
                method="GET",
                path="/v4/patient_balance",
                description="Return patient balance from practice management systems",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "practice_id": "Practice ID",
                    "patient_id": "patient id of office",
                    "customer_id": "customer id of office",
                    "current_date": "format: yyyy-mm-dd, current date"
                },
                required_params=["request_key"],
                response_fields=[
                    "patient_id", 
                    "firstname",
                    "lastname",
                    "patient_balance",
                    "insurance_due",
                    "patient_due"
                ],
                sortBy=[
                    "patient_id",
                    "customer_id", 
                    "current_date",
                    "practice_id"
                ]
            ),

            "clinical_conditions": APIEndpoint(
                name="Clinical Conditions",
                method="GET",
                path="/v4/clinical_conditions",
                description="Returns clinical conditions data",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "status": "appointment / treatment plan / clinical_conditions status",
                    "practice_id": "practice id of office"
                },
                required_params=["request_key"],
                response_fields=[
                    "id",
                    "condition_name",
                    "tooth_surface",
                    "description",
                    "status"
                ],
                sortBy=[
                    "status",
                    "id",
                    "description",
                    "condition_name"
                ]
            ),

            "fee_schedules": APIEndpoint(
                name="Fee Schedules",
                method="GET",
                path="/v4/fee_schedules",
                description="Returns fee schedule data from practice",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "practice_id": "practice id of office",
                    "fee_no": "fee number in practice management system",
                    "procedure_code": "procedure code in practice management system"
                },
                required_params=["request_key"],
                response_fields=[
                    "fee_no",
                    "procedure_code",
                    "fee_name",
                    "fee_amount"
                ],
                sortBy=[
                    "fee_amount",
                    "procedure_code"
                ]
            ),

            "practice_location_get": APIEndpoint(
                name="Practice Location",
                method="GET",
                path="/v4/practice_location",
                description="Get all practice details for authorized office id and return with access is on or off",
                params={
                    "office_id": "Office_id received from authorized_practices API"
                },
                required_params=["office_id"],
                response_fields=[
                    "practice_id",
                    "name",
                    "address",
                    "access_status"
                ],
                sortBy=[
                    "practice_id"
                ]
            ),
            "finance_customers": APIEndpoint(
                name="Finance Customers",
                method="GET",
                path="/v4/finance/customers",
                description="Returns customer details data from practice's finance system",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "fullname": "fullname",
                    "customer_id": "customer id from finance system (different from customer_id in other APIs)",
                    "name": "name"
                },
                required_params=["request_key"],
                response_fields=[
                    "customer_id",
                    "name",
                    "fullname",
                    "address",
                    "email",
                    "phone"
                ],
                sortBy=["customer_id"]
            ),

            "appointments": APIEndpoint(
                name="Appointments", 
                method="GET",
                path="/v4/appointments",
                description="Returns appointments data from practice",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "appointment_sr_no": "appointment serial number from appointments",
                    "practice_id": "practice id of office",
                    "patient_id": "Patient ID as per the management system",
                    "guarantor_id": "guarantor id in practice management system",
                    "provider_id": "Provider id as per practice management system",
                    "startdate": "format: yyyy-mm-dd, start date",
                    "enddate": "format: yyyy-mm-dd, end date",
                    "procedure_code": "Procedure code",
                    "status": "Status",
                    "operatory": "Operatory",
                    "type": "Type"
                },
                required_params=["request_key"],
                response_fields=[
                    "appointment_sr_no",
                    "patient_id",
                    "provider_id", 
                    "date",
                    "time",
                    "status",
                    "type",
                    "operatory"
                ],
                sortBy=[
                    "appointment_sr_no",
                    "appointment_date",
                    "appointment_time",
                    "patient_id"
                ]
            ),

            "appointments_available_slots": APIEndpoint(
                name="Available Appointment Slots",
                method="GET",
                path="/v4/appointments_available_slots",
                description="Returns available appointments slots from practice",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "provider_id": "Provider id as per practice management system",
                    "practice_id": "practice id of office",
                    "startdate": "format: yyyy-mm-dd, start date",
                    "enddate": "format: yyyy-mm-dd, end date",
                    "operatory": "Operatory"
                },
                required_params=["request_key"],
                response_fields=[
                    "date",
                    "time",
                    "provider_id",
                    "operatory"
                ],
                sortBy=[
                    "practice_id",
                    "date",
                    "time"
                ]
            ),

            "accounts_receivables": APIEndpoint(
            name="Accounts Receivables",
            method="GET",
            path="/v4/accounts_receivables",
            description="Returns account receivables details from practice",
            params={
                "request_key": "A Valid 32 characters alpha-numeric request key",
                "practice_id": "practice id of office",
                "guarantor_id": "guarantor id in practice management system",
                "current_date": "Value should be true/false. If false returns all data, if true returns current AR"
            },
            required_params=["request_key"],
            response_fields=[
                "guarantor_id",
                "amount_between_0_30",
                "amount_between_31_60",
                "amount_between_61_90",
                "amount_greater_than_90",
                "current_date",
                "entry_id"
            ],
            sortBy=[
                "guarantor_id",
                "current_date",
                "entry_id",
                "practice_id",
                "amount_between_0_30",
                "amount_between_31_60",
                "amount_between_61_90",
                "amount_greater_than_90"
            ]
        ),

            "contact_details": APIEndpoint(
                name="Contact Details",
                method="GET",
                path="/v4/contact_details",
                description="Returns contact details of patients from practice",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "practice_id": "practice id of office",
                    "patient_id": "patient id in practice management system",
                    "uid": "Unique Id",
                    "contact_of": "Contact of patient",
                    "contact_type": "Contact Type of patient",
                    "contact_value": "Contact value"
                },
                required_params=["request_key"],
                response_fields=[
                    "uid",
                    "contact_of",
                    "contact_type",
                    "contact_value",
                    "patient_id"
                ],
                sortBy=[
                    "uid",
                    "contact_of", 
                    "contact_type",
                    "contact_value",
                    "practice_id"
                ]
            ),

            "payment_types": APIEndpoint(
                name="Payment Types",
                method="GET",
                path="/v4/payment_types",
                description="Returns payment types from practice",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "practice_id": "practice id of office",
                    "code": "payment type code in practice management system",
                    "customer_id": "customer id of office",
                    "is_adjustment_type": "value should be true. it will return Credit Adjustment Types only",
                    "is_debit_adjustment_type": "value should be true. it will return Debit Adjustment Types only",
                    "is_insurance_type": "value should be true. it will return Insurance Payment Types only",
                    "are_credit_card_details_required": "value should be true. it will return Payment Types which require credit card details for POST transaction for Planet DDS PMS only",
                    "app_id": "This is the ID assigned to the application when the application is registered on API portal"
                },
                required_params=["request_key"],
                response_fields=[
                    "code",
                    "description",
                    "type"
                ],
                sortBy=["code"]
            ),

            "patient_statuses": APIEndpoint(
                name="Patient Statuses",
                method="GET",
                path="/v4/patient_statuses",
                description="Returns patient status data from practice",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "practice_id": "practice id of office"
                },
                required_params=["request_key"],
                response_fields=[
                    "patient_id",
                    "status",
                    "practice_id"
                ],
                sortBy=["practice_id"]
            ),
            "patients": APIEndpoint(
                name="Patients",
                method="GET",
                path="/v4/patients",
                description="Returns patient information from practice",
                params={
                    "request_key": "A Valid 32 characters alpha-numeric request key",
                    "email": "Email id of patient",
                    "patient_id": "Patient ID as per the management system",
                    "firstname": "First name of patient",
                    "practice_id": "Practice ID of office",
                    "lastname": "Last name of patient",
                    "last_visit": "Last Visit",
                    "cell": "Cell Number",
                    "search": "Search patient by firstname, lastname, email, middlename, city, state, zipcode, homephone, workphone, cell",
                    "fields": "fields parameter allows to return only requested fields with mandatory fields",
                    "status": "Status of patient",
                    "phone": "Phone Number"
                },
                required_params=["request_key"],
                response_fields=[
                    "patient_id",
                    "guarantor_id", 
                    "firstname",
                    "middlename",
                    "lastname",
                    "preferred_name",
                    "salutation",
                    "birthdate",
                    "status",
                    "patient_note",
                    "medical_note",
                    "alert_note",
                    "other_note",
                    "gender",
                    "marital_status",
                    "address_line1",
                    "address_line2", 
                    "city",
                    "state",
                    "zipcode",
                    "homephone",
                    "workphone",
                    "cell",
                    "email",
                    "employer_id",
                    "billing_type",
                    "first_visit",
                    "last_visit",
                    "provider_id",
                    "practice_id",
                    "primary_insurance_company_id",
                    "secondary_insurance_company_id",
                    "primary_relationship",
                    "secondary_relationship"
                ],
                sortBy=[
                    "patient_id",
                    "firstname",
                    "lastname",
                    "zipcode"
                ]
            )
        }

    def get_documentation_prompt(self, selected_endpoints=None):
        """Generate a prompt section for API documentation"""
        docs = ["Available Custom APIs:\n"]
        
        endpoints = self.endpoints
        if selected_endpoints:
            endpoints = {k: v for k, v in self.endpoints.items() if k in selected_endpoints}
        
        for endpoint_name, endpoint in endpoints.items():
            docs.append(f"\n{endpoint.name.upper()}:")
            docs.append(f"Method: {endpoint.method}")
            docs.append(f"Path: {endpoint.path}")
            docs.append(f"Description: {endpoint.description}\n")
            
            docs.append("Required Parameters:")
            for param in endpoint.required_params:
                docs.append(f"  - {param}: {endpoint.params.get(param, '')}")
            
            optional_params = [p for p in endpoint.params if p not in endpoint.required_params]
            if optional_params:
                docs.append("\nOptional Parameters:")
                for param in optional_params:
                    docs.append(f"  - {param}: {endpoint.params[param]}")
            
            docs.append("\nResponse Fields:")
            for field in endpoint.response_fields:
                docs.append(f"  - {field}")
            
            if endpoint.sortBy:
                docs.append("\nSort By:")
                for sort in endpoint.sortBy:
                    docs.append(f"  - {sort}")
            
            docs.append("\n---")
        
        return "\n".join(docs)

# Create the api_docs instance that will be imported by other modules
api_docs = APIDocumentation()
