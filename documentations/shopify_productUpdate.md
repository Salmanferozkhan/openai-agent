# Shopify GraphQL Product Update Mutation

## Overview
The `productUpdate` mutation allows updating a Shopify product with various attributes such as title, description, vendor, and media.

## Key Features
- Requires `write_products` access scope
- Allows updating multiple product attributes simultaneously
- Cannot update product variants directly

## Mutation Arguments

### `product` (ProductUpdateInput)
- Product details to be updated
- Includes fields like:
  - `id` (required)
  - `title`
  - `handle`
  - `vendor`
  - `productType`
  - `status`
  - `tags`
  - `seo`
  - `metafields`

### `media` ([CreateMediaInput!])
- Optional list of new media to add to the product
- Supports adding images and videos
- Media is uploaded asynchronously

## Limitations
- Throttled when a store has 50,000+ product variants
- Limited to 1,000 new product variant updates per day after threshold

## Complementary Mutations
- `productSet`: Perform multiple product operations
- `publishablePublish`: Publish product to make it available to customers

## Access Requirements
- Requires `write_products` access scope
- User must have product update permissions

## Common Use Cases
- Update product details
- Add new product media
- Modify SEO settings
- Update custom metafields
- Change product status or tags

## Example Scenarios
1. Adding new media to a product
2. Updating comprehensive product details
3. Adding custom metafields
4. Changing product title

## Best Practices
- Use for bulk product updates
- Avoid updating product variants with this mutation
- Use complementary mutations for additional modifications
