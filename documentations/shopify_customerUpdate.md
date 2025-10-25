# customerUpdate GraphQL Mutation

## Overview
The `customerUpdate` mutation allows updating a customer's attributes in Shopify's Admin GraphQL API. It requires the `write_customers` access scope and supports various update operations like modifying personal information, addresses, and metafields.

## Mutation Details

### Access Requirements
- Requires `write_customers` access scope
- As of API version 2022-10, apps using protected customer data must meet specific [data protection requirements](https://shopify.dev/apps/store/data-protection/protected-customer-data)

### Input Arguments
- `input` (CustomerInput!, required):
  - `id`: Global ID of the customer to update
  - `firstName`: Customer's first name
  - `lastName`: Customer's last name
  - `metafields`: Array of metafield updates
  - `addresses`: Array of address modifications

### Return Payload
- `customer`: Updated customer object
- `userErrors`: List of errors encountered during mutation

## Key Capabilities
1. Update customer personal information
2. Modify customer addresses
3. Create and update metafields
4. Bulk address operations

## Example Use Cases

### Update Customer Name
```graphql
mutation {
  customerUpdate(input: {
    id: "gid://shopify/Customer/1018520244",
    firstName: "Tobi",
    lastName: "Lutke"
  }) {
    customer {
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

### Add/Update Customer Addresses
```graphql
mutation {
  customerUpdate(input: {
    id: "gid://shopify/Customer/1018520244",
    addresses: [{
      address1: "123 New Street",
      city: "New City"
    }]
  }) {
    customer {
      addressesV2(first: 10) {
        edges {
          node {
            address1
            city
          }
        }
      }
    }
  }
}
```

### Metafield Management
```graphql
mutation {
  customerUpdate(input: {
    id: "gid://shopify/Customer/1018520244",
    metafields: [{
      namespace: "custom",
      key: "preferences",
      value: "value"
    }]
  }) {
    customer {
      metafields(first: 10) {
        edges {
          node {
            namespace
            key
            value
          }
        }
      }
    }
  }
}
```

## Best Practices
- Always handle potential `userErrors`
- Validate customer data before submission
- Use appropriate access scopes
- Respect customer data protection requirements

## API Versions
- Current version: 2025-10
