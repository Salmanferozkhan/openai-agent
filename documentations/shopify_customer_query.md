# Customer GraphQL Query Documentation

## Overview
The `customer` query retrieves a specific `Customer` resource by its unique ID in the Shopify Admin GraphQL API.

## Query Signature
```graphql
query {
  customer(id: ID!): Customer
}
```

## Arguments
- `id` (ID!, Required): The unique global identifier for the customer to retrieve

## Returned Object: Customer
A comprehensive representation of a customer with multiple fields including:

### Personal Information
- `firstName`: Customer's first name
- `lastName`: Customer's last name
- `email`: Customer's email address
- `phone`: Customer's phone number
- `displayName`: Full name representation

### Account Metrics
- `numberOfOrders`: Total number of orders placed
- `amountSpent`: Total monetary value of customer's purchases
- `lifetimeDuration`: Customer's account longevity

### Account Status
- `verifiedEmail`: Email verification status
- `validEmailAddress`: Email address validity
- `state`: Current account state (e.g., "ENABLED")
- `canDelete`: Whether the account can be deleted
- `tags`: Custom tags associated with the customer

### Temporal Information
- `createdAt`: Account creation timestamp
- `updatedAt`: Last account update timestamp

### Address Information
- `defaultAddress`: Primary shipping address
- `addresses`: List of customer's addresses
- `addressesV2`: Enhanced address management

### Additional Features
- `image`: Customer profile image
- `metafields`: Custom metadata
- `orders`: Customer's order history
- `events`: Account-related events

## Access and Permissions
> Only use this data if it's required for your app's functionality.

## Example Query
```graphql
query {
  customer(id: "gid://shopify/Customer/544365967") {
    firstName
    lastName
    email
  }
}
```

## Supported Platforms
- GraphQL Admin API
- Supports multiple programming languages (Ruby, Node.js, React, cURL)

## Potential Use Cases
- Customer profile retrieval
- Order history analysis
- Marketing segmentation
- Customer support tools

## Limitations
- Requires appropriate access scopes
- Limited to retrieving one customer at a time
- Must have valid customer ID
