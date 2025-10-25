# Shopify GraphQL Admin API: customerCreate Mutation

## Overview
The `customerCreate` mutation allows developers to create new customers in a Shopify store. It requires the `write_customers` access scope and supports various customer details and marketing consent options.

## Mutation Details

### Arguments
- `input` (CustomerInput!, required): Specifies customer creation parameters
  - Supports fields like:
    - `email`
    - `phone`
    - `firstName`
    - `lastName`
    - `addresses`
    - `emailMarketingConsent`
    - `smsMarketingConsent`
    - `metafields`

### Payload Returns
- `customer`: The newly created Customer object
- `userErrors`: List of errors encountered during customer creation

## Key Requirements
- Customer must have at least one identifier: name, phone number, or email address
- As of API version 2022-10, apps using protected customer data must meet specific [data protection requirements](https://shopify.dev/apps/store/data-protection/protected-customer-data)

## Marketing Consent Options
- Supports different marketing states:
  - `SUBSCRIBED`
  - `NOT_SUBSCRIBED`
- Marketing opt-in levels:
  - `SINGLE_OPT_IN`
  - `CONFIRMED_OPT_IN`

## Example Use Cases
1. Create a customer with SMS marketing consent
2. Add a customer with a shipping address
3. Create a customer with custom metafields

## Code Example (GraphQL)
```graphql
mutation customerCreate($input: CustomerInput!) {
  customerCreate(input: $input) {
    customer {
      id
      email
      firstName
      lastName
    }
    userErrors {
      field
      message
    }
  }
}
```

## Supported Programming Languages
- JavaScript/Node.js
- Ruby
- React Router
- cURL

## Best Practices
- Always handle potential `userErrors`
- Validate customer data before submission
- Respect customer consent preferences
- Use appropriate marketing consent levels

## API Versions
- Current version: 2025-10
- Requires careful attention to data protection guidelines
