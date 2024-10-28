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