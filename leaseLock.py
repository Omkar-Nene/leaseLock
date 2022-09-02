import requests
import json
import sys

# main API URL
api_url = "https://idy4d4ejzi.execute-api.us-west-2.amazonaws.com/prod/"

# add company info API suffix
company_info_url_suffix = "companies/"

# add certificate info API suffix
cert_info_url_suffix = "/certs"

# add property info API suffix
property_info_url_suffix = "/properties"

# main function
def create_report(id_list):

    # dictionary for the final report with Report & Errors
    final_report = dict()

    # create a list of company ids to call APIs
    final_list = id_list.split(",")

    # 'list to populate report tag in the final output'
    report = []

    no_certificates_present = False
    no_properties_present = False

    # iterate over each company id and call the 3 APIs for each of them
    for company_id in final_list:

        # call company info API and store its response
        company_info_request = api_url + company_info_url_suffix + str(company_id)
        company_info_response = requests.get(company_info_request).json()
        if len(company_info_response['company']) == 0:
            continue

        # call certificate info API for the company and store its response
        cert_info_request = api_url + company_info_url_suffix + str(company_id) + cert_info_url_suffix
        cert_info_response = requests.get(cert_info_request).json()
        if len(cert_info_response['certs']) == 0:
            no_certificates_present = True

        # call the property info API for the company and store its response
        property_info_request = api_url + company_info_url_suffix + str(company_id) + property_info_url_suffix
        property_info_response = requests.get(property_info_request).json()
        if len(property_info_response['properties']) == 0:
            no_properties_present = True

        # create company level object
        company_dic = dict()

        # list to have all company-property pair related errors populated at the end
        errors_list = []

        # to skip a property all together if a product type error occurs
        skip_property_flag = False

        # populate company level data from the company info API response stored
        company_dic['company_name'] = company_info_response['company']['name']
        company_dic['company_id'] = company_info_response['company']['id']

        # variable to populate total monthly revenue across all properties
        total_monthly_rev = 0

        # variable populate total units of the company owns across all properties
        total_units = 0

        properties = []

        # certificate part of report
        certificates = []

        # if there are no properties and no certificates present for a company
        # then we skip calculations at company level as well and just return empty arrays
        if no_properties_present and no_certificates_present:
            continue

        # iterate over properties of a company
        for item in property_info_response['properties']:
            # add all units from each property to find total units
            total_units += int(item['units'])

        # set the value of total units in company level info
        company_dic['total_units'] = total_units

        # populate total certs - nothing but number of certificates
        company_dic['total_certs'] = len(cert_info_response['certs'])

        # populate total coverage - as per formula
        company_dic['total_coverage'] = company_dic['total_certs']/total_units

        # property level details

        # here we loop through properties and the respective certificates
        # for the properties to populate property level data
        for item in property_info_response['properties']:
            certs_per_property = 0
            monthly_rev_per_prop = 0
            prop = dict()
            for cert in cert_info_response['certs']:
                # for every match of id in property info and property id in cert info
                # we process data related to the property
                if cert['property_id'] == item['id']:
                    # add an error entry for invalid product for a property
                    if (item['type'] == 'PAY_IN_FULL' and cert['down_payment'] == 0) or (item['type'] == 'INSTALLMENTS' and cert['installment_payment'] == 0):
                        error_product = dict()
                        error_product['error_code'] = 'INVALID_PRODUCT_FOR_PROPERTY'
                        error_product['company_id'] = company_info_response['company']['id']
                        error_product['property_id'] = item['id']
                        # to exclude the property from the report
                        skip_property_flag = True
                        errors_list.append(error_product)
                        continue

                    certs_per_property += 1
                    # to ensure we always calculate monthly revenue per property as per type of payment
                    if cert['down_payment'] == 0:
                        monthly_rev_per_prop += cert['installment_payment'] + cert['monthly_fee']
                    elif cert['installment_payment'] == 0 or cert['monthly_fee'] == 0:
                        monthly_rev_per_prop += cert['down_payment']/12
                    else:
                        monthly_rev_per_prop += cert['down_payment'] / 12
                else:
                    continue

            # to exclude property calculations
            if skip_property_flag:
                continue

            total_monthly_rev += monthly_rev_per_prop

            # add error to the error list if total certs > total units and skip property calculations
            if certs_per_property > item['units']:
                error_more_certs = dict()
                error_more_certs['error_code'] = 'MORE_CERTS_THAN_UNITS'
                error_more_certs['company_id'] = company_info_response['company']['id']
                error_more_certs['property_id'] = item['id']
                errors_list.append(error_more_certs)
                continue

            prop['property_id'] = item['id']
            prop['certs'] = certs_per_property
            prop['units'] = item['units']

            # populate coverage if cert data is available for the property else the coverage would be 0
            if certs_per_property != 0:
                prop['coverage'] = certs_per_property/item['units']
            else:
                prop['coverage'] = 0
            prop['monthly_revenue'] = monthly_rev_per_prop
            properties.append(prop)


        # to count frequency of each product
        product_counts = dict()
        for item in cert_info_response['certs']:
            if item['product_id'] not in product_counts.keys():
                product_counts[item['product_id']] = 1
            else:
                product_counts[item['product_id']] += 1
        # to set the entire cert data into report per company
        for k, v in product_counts.items():
            certificate = dict()
            certificate['product_id'] = k
            certificate['amount'] = product_counts[k]
            certificate['percent'] = product_counts[k] / len(cert_info_response['certs'])
            certificates.append(certificate)
        # company level data
        company_dic['monthly_revenue'] = total_monthly_rev
        company_dic['annual_revenue'] = total_monthly_rev * 12
        # set property level data
        company_dic['properties'] = properties
        # set cert level data to company
        company_dic['certs'] = certificates
        # add company data to the report
        report.append(company_dic)
    # add report to the final response
    final_report['report'] = report
    # add errors to the final response
    final_report['errors'] = errors_list
    # convert the dictionary to json for the final response structure
    json_string = json.dumps(final_report, indent=4)
    # print the response to std out
    print(json_string)


if __name__ == "__main__":
    # to run code through command line/ terminal
    in_value = sys.argv
    #  to take the user input of company ids
    create_report(in_value[1])


