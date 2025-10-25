# orderUpdate GraphQL Mutation

## Overview
The `orderUpdate` mutation allows updating specific attributes of an existing order in Shopify's Admin GraphQL API.

## Access Requirements
- Requires `write_orders` or `write_marketplace_orders` access scope
- Optional: `write_pos_staff_member_event_attribution_overrides` to assign events to another staff member

## Supported Updates
Allows modification of:
- Customer email
- Shipping address
- Order tags
- Order notes
- Metafields

## Limitations
- Cannot modify line items, quantities, or discounts (use `orderEditBegin` instead)
- Cannot remove a customer (use `orderCustomerRemove` instead)

## Mutation Arguments
- `input` (required): [OrderInput!]
  - `id`: Global order identifier
  - `email`: Customer email address
  - `shippingAddress`: Updated shipping details
  - `tags`: Order tags
  - `note`: Order-level notes

## Return Payload
- `order`: Updated [Order] object
- `userErrors`: List of potential errors during mutation

## Example Use Cases
1. Update shipping address
2. Change customer email
3. Add order tags
4. Modify order notes

## Code Examples Provided
- GraphQL
- cURL
- React Router
- Node.js
- Ruby

## Best Practices
- Use appropriate access scopes
- Validate input before mutation
- Handle potential user errors
- Consider using specialized mutations for complex order modifications

## Supported API Versions
- Current version: 2025-10
