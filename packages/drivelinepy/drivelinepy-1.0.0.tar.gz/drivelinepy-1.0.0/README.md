# Drivelinepy

## Installation

```
pip install drivelinepy
```

### .env example for credentials

If interested in using a `.env` file, `pip install python-dotenv` in your root application.

To load your `.env` file in the application code.

```
from dotenv import load_dotenv
load_dotenv()
```

Example contents of `.env`
```
VIRTUAGYM_API_KEY = "redacted"
VIRTUAGYM_CLUB_SECRET = "redacted"
VIRTUAGYM_SCHEDULE_ID = "redacted"
VIRTUAGYM_CLUB_ID = "redacted"

ZOHO_ORGANIZATION_ID = "redacted"
ZOHO_REFRESH_TOKEN = "redacted"
ZOHO_ACCESS_TOKEN = "redacted"
ZOHO_CLIENT_SECRET = "redacted"
ZOHO_CLIENT_ID = "redacted"
ZOHO_BILLINGS_REDIRECT_URI = "www.zohoapis.com/subscriptions"
ZOHO_GRANT_TYPE = "refresh_token"

SLACK_API_TOKEN = "redacted"
SLACK_API_CHANNEL = "redacted"
SLACK_UPLOAD_FILE_API_URL = "https://slack.com/api/files.upload"
```

## VirtuagymAPI

using v1 https://github.com/virtuagym/Virtuagym-Public-API/wiki

`VirtuagymAPI` extends `BaseAPIWrapper` to interact with the Virtuagym API. Initialize it with your API key and club secret:

### Initialization Example

```
import os
from drivelinepy import VirtuagymAPI 

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

#=================================================================
# Function Definition 
#=================================================================

def main():
    
    #-----------------------------------------------------------------
    # Initialize logging and variables
    #-----------------------------------------------------------------
    logging.info("Initializing...")
    vg_api_key = os.getenv("VIRTUAGYM_API_KEY")
    vg_club_secret = os.getenv("VIRTUAGYM_CLUB_SECRET")

    #-----------------------------------------------------------------
    # Initialize Virtuagym Object
    #-----------------------------------------------------------------

    vg_client = VirtuagymAPI(vg_api_key, vg_club_secret)

    logging.info("Initialization complete!")

    #-----------------------------------------------------------------
    # Do Something...
    #-----------------------------------------------------------------
    
#=================================================================
# Main
#=================================================================

if __name__ == "__main__":
    main()

```


### Get Club Events

```
club_id = "your_club_id"  # Replace with the actual club ID
timestamp_start = 1704355200  # Replace with the start timestamp in milliseconds
timestamp_end = 1704441599  # Replace with the end timestamp in milliseconds

club_events = vg_client.get_club_events(club_id, timestamp_start, timestamp_end)
print("Club Events:", club_events)

```


### Get Event Participants

```
club_id = "your_club_id"
event_id = "your_event_id"

event_participants = vg_client.get_event_participants(club_id, event_id=event_id)
print("Event Participants:", event_participants)
```

### Get Club Members
```
club_id = "your_club_id"

# Fetch all members
all_members = vg_client.get_club_members(club_id)
print("All Club Members:", all_members)

# Fetch a specific member by their club member ID
club_member_id = "member_id"  # Replace with the specific club member ID
specific_member = vg_client.get_club_members(club_id, club_member_id=club_member_id)
print("Specific Member Details:", specific_member)

```
## Zoho API

### Developer Console

Before working with Zoho APIs, you will need to obtain access to a Zoho Account to access the Developer Console https://api-console.zoho.com/

A common scope string below
`ZohoCRM.modules.contacts.READ,ZohoSubscriptions.customers.READ,ZohoSubscriptions.subscriptions.READ,ZohoSubscriptions.invoices.READ`

### Zoho Billing API

https://www.zoho.com/billing/api/v1/introduction/#overview

`ZohoBillingAPI` is tailored for the Zoho Billing API. This class extends the `BaseAPIWrapper` to specifically handle the authentication and request patterns for Zoho's Billing services. Key functionalities include refreshing OAuth tokens, fetching subscription data, and handling Zoho-specific API requests.

#### Initialization
To initialize and use `ZohoBillingAPI`, provide your client ID, client secret, refresh token, and organization ID:

```
import os
from drivelinepy import ZohoBillingAPI

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)

#=================================================================
# Function Definition 
#=================================================================

def main():
    #-----------------------------------------------------------------
    # Initialize logging and variables
    #-----------------------------------------------------------------
    client_id = os.getenv("ZOHO_CLIENT_ID")  
    client_secret = os.getenv("ZOHO_CLIENT_SECRET")
    refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")
    organization_id = os.getenv("ZOHO_ORGANIZATION_ID")

    #-----------------------------------------------------------------
    # Initialize Virtuagym Object
    #-----------------------------------------------------------------
    zoho_api = ZohoBillingAPI(client_id, client_secret, refresh_token, organization_id)

#=================================================================
# Main
#=================================================================
if __name__ == "__main__":
    main()
```

#### Get Customers

The `get_customers()` method is an essential feature of the API interface, allowing for the retrieval of customer data from the Zoho Billing API. 

Parameters
- `customer_id`: (Optional) A unique identifier for a specific customer.
- `name`: (Optional) The name of the customer to be fetched.
- `email`: (Optional) The email address of the customer to be fetched.
- `phone`: (Optional) The phone number of the customer to be fetched.
- `filter_by`: (Optional) A string to filter customers by specific criteria, such as 'Status.Active'.
- `page`: (Optional) The page number for pagination, defaulting to the first page.

##### Usage

Get all customers
```
customer_details = zoho_api.get_customers()
```

Get customer by customer id
```
customer_id = "customer-id-here"
customer_details = zoho_api.get_customers(customer_id=customer_id)
```

Get customers by name - note the API is using `display_name_contains` vs using an exact match
```
customer_name = "insert-name-here"
customers = zoho_api.get_customers(name=customer_name)
```

Get customer by email
```
customer_email = "insertemail@gmail.com"
customers = zoho_api.get_customers(email=customer_email)
```

Get customer by phone
```
customer_phone = "4255551234"
customers = zoho_api.get_customers(phone=customer_phone)
```

Get customers with filter

```
customer_filter = "Active"
filtered_customers = zoho_api.get_customers(filter=customer_filter)
```
Available Filters https://www.zoho.com/billing/api/v1/customers/#list-all-customers

##### Get Subscriptions

The `get_subscriptions()` method is designed to fetch subscription data from the Zoho Billing API.

Parameters
- `subscription_id`: (Optional) A unique identifier for a specific subscription.
- `customer_id`: (Optional) A unique identifier for a customer. Used to fetch subscriptions associated with this customer.
- `filter_by`: (Optional) A status value to filter subscriptions. Examples include "Active", "Expired", etc.
- `page`: (Optional) Page number for pagination, defaulting to the first page.

###### Usage

Get all subscriptions
```
subscriptions = zoho_api.get_subscriptions()
```

Get subscriptions by subscription id
```
subscription_id = "insert-sub-id-here"
subscriptions = zoho_api.get_subscriptions(subscription_id=subscription_id)
```

Get subscriptions by customer id
```
customer_id = "insert-customer-id"
subscriptions = zoho_api.get_subscriptions(customer_id=customer_id)
```

Get subscriptions with filter
```
subscription_filter = 'ACTIVE'
subscriptions = zoho_api.get_subscriptions(filter_by=subscription_filter)
```

Available filters https://www.zoho.com/billing/api/v1/subscription/#list-all-subscriptions

##### Get Invoices

The `get_invoices()` method allows for fetching invoices from the Zoho Billing API based on specified criteria.

Parameters:
- `invoice_id` (optional): Fetches a specific invoice.
- `customer_id` (optional): Filters invoices for a specific customer.
- `subscription_id` (optional): Filters invoices for a specific subscription.
- `filter_by` (optional): Filters invoices by their status.
- `page` (optional, default=1): Specifies the page number of results.


###### Usage

Get all invoices
```
invoices = zoho_api.get_invoices()
```

Get invoice by invoice id
```
invoice_id = "insert-invoice-id"
invoices = zoho_api.get_invoices(invoice_id=invoice_id)
```

Get invoice by customer id
```
customer_id = "insert-customer-id"
invoices = zoho_api.get_invoices(customer_id=customer_id)
```

Get invoice by subscription id
```
subscription_id = "insert-subs-id"
invoices = zoho_api.get_invoices(subscription_id=subscription_id)
```

Get invoice with filter
```
invoice_filter = "Paid"
invoices = zoho_api.get_invoices(filter_by=invoice_filter)
```

##### Get Credit Notes

The `get_credit_notes()` method is a part of our API interface to interact with the Zoho Billing API, specifically designed to retrieve credit note data.

Parameters
- `credit_note_id`: (Optional) A unique identifier for a specific credit note.
- `customer_id`: (Optional) A unique identifier for a customer, used to filter credit notes associated with this customer.
- `customer_name`: (Optional) The name of the customer, used to fetch credit notes associated with this customer.
- `filter_by`: (Optional) A string to filter credit notes by specific criteria, such as 'Status.Active'.
- `page`: (Optional) The page number for pagination, defaulting to the first page.

###### Usage

Get all credit notes
```
credit_notes = zoho_api.get_credit_notes()
```

Get credit notes by customer id
```
customer_id = "insert-customer-id"
credit_notes = zoho_api.get_credit_notes(customer_id=customer_id)
```

Get credit notes by customer name
```
customer_name = "John Doe"
credit_notes = zoho_api.get_credit_notes(customer_name=customer_name)
```

Get credit notes with filter
```
credit_note_filter = "Open"
credit_notes = zoho_api.get_credit_notes(filter_by=credit_note_filter)
```

##### Clarifying Filters

If you do not feel like looking through the code to find the filters available you can use the following methods

# Get valid subscription filters
`subscription_filters = zoho_api.get_subscription_filters()`

# Get valid customer status filters
`customer_status_filters = zoho_api.get_customer_status_filters()`

# Get valid invoice filters
`invoice_filters = zoho_api.get_invoice_filters()`

# Get valid credit note status filters
`credit_note_status_filters = zoho_api.get_credit_note_status_filters()`

A check occurs when you call the respective get data method so you do not have to add checks for valid filter in the application code. These are purely nice-to-haves.
