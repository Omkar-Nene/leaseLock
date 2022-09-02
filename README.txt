Steps to run the program -
1. Install Python on your system
2. Make sure to include python in your path variable in both user variables and system variables
3. Navigate to the folder where the program is present
4. Open cmd(Terminal) in the location
5. Execute the command - python leaseLock.py 1,2
6. You will get response in the terminal

Design of code & assumptions & validations-
1. The program uses sys.argv which takes the file name as 1st element of the list and 2nd element as the comma separated company ids and we send over the 2nd element to the function which does the processing.
2. API end points defined as global variables. So if any additional APIs related to companies are developed they can directly be added as global variables with appropriate suffixes.
3. Create a list of company ids from the input given by the users.
4. Process each company with company info, certificate info, property info.
5. For invalid inputs of company_id we do not process that company as the company information api would not yield any company information.
6. For any company which does not have certificate info as well as property info we will show empty list in the report for that particular company.
7. For a property which does not have certificates associated with it the monthly revenue would be 0 and coverage would be 0.
8. If there are no validation errors as per the validations mentioned in the assignment errors list would be empty.
9. If any of the validations are failed we skip that property's details from the company level data and that property's data gets added to the error's list at the end with its respective company


Sample output for command line input - python leaseLock.py 1,2
{
    "report": [
        {
            "company_name": "Foo PMC",
            "company_id": "1",
            "total_units": 11,
            "total_certs": 4,
            "total_coverage": 0.36363636363636365,
            "monthly_revenue": 91.66666666666666,
            "annual_revenue": 1100.0,
            "properties": [
                {
                    "property_id": "1",
                    "certs": 2,
                    "units": 2,
                    "coverage": 1.0,
                    "monthly_revenue": 30.0
                },
                {
                    "property_id": "2",
                    "certs": 0,
                    "units": 3,
                    "coverage": 0,
                    "monthly_revenue": 0
                },
                {
                    "property_id": "3",
                    "certs": 1,
                    "units": 5,
                    "coverage": 0.2,
                    "monthly_revenue": 41.666666666666664
                },
                {
                    "property_id": "4",
                    "certs": 1,
                    "units": 1,
                    "coverage": 1.0,
                    "monthly_revenue": 20.0
                }
            ],
            "certs": [
                {
                    "product_id": "a",
                    "amount": 1,
                    "percent": 0.25
                },
                {
                    "product_id": "b",
                    "amount": 2,
                    "percent": 0.5
                },
                {
                    "product_id": "c",
                    "amount": 1,
                    "percent": 0.25
                }
            ]
        },
        {
            "company_name": "Bar PMC",
            "company_id": "2",
            "total_units": 93,
            "total_certs": 4,
            "total_coverage": 0.043010752688172046,
            "monthly_revenue": 95.0,
            "annual_revenue": 1140.0,
            "properties": [
                {
                    "property_id": "5",
                    "certs": 3,
                    "units": 56,
                    "coverage": 0.05357142857142857,
                    "monthly_revenue": 60.0
                },
                {
                    "property_id": "6",
                    "certs": 1,
                    "units": 28,
                    "coverage": 0.03571428571428571,
                    "monthly_revenue": 35
                },
                {
                    "property_id": "7",
                    "certs": 0,
                    "units": 9,
                    "coverage": 0,
                    "monthly_revenue": 0
                }
            ],
            "certs": [
                {
                    "product_id": "b",
                    "amount": 3,
                    "percent": 0.75
                },
                {
                    "product_id": "d",
                    "amount": 1,
                    "percent": 0.25
                }
            ]
        }
    ],
    "errors": []
}
