# Shopify Admin GraphQL API - productCreate Mutation

## Overview
The `productCreate` mutation creates a new product in a Shopify store with various configurable attributes.

## Access Requirements
- **Required Scope**: `write_products`
- **Permissions**: User must have product creation permissions

## Key Capabilities
- Create products with multiple attributes like title, description, vendor
- Define product options and variations
- Add product metadata and media
- Set SEO settings and tags
- Create combined listing products

## Important Limitations
- Only supports creating a product with its initial product variant
- Has a throttle limit of 1,000 new product variants per day after 50,000 variants

## Main Arguments

### 1. `product` (required)
Product creation details including:
- **Title**: Product name
- **Description**: Product description
- **Product type**: Category/type of product
- **Vendor**: Manufacturer or brand
- **Options**: Product variations (size, color, etc.)
- **Status**: Product visibility status
- **SEO settings**: Meta title, description
- **Tags**: Product tags for organization

### 2. `media` (optional)
Media files to associate with the product

## Typical Use Cases
- Creating multiple products simultaneously
- Launching new product lines
- Adding seasonal products
- Configuring complex product variations

## Post-Creation Actions
- Publish product using `publishablePublish` mutation
- Update product using `productUpdate` mutation
- Modify product options with `productSet` mutation

## Example Mutation

```graphql
mutation {
  productCreate(product: {
    title: "Product Name",
    productOptions: [
      {name: "Color", values: [{name: "Red"}, {name: "Blue"}]},
      {name: "Size", values: [{name: "Small"}, {name: "Large"}]}
    ]
  }) {
    product {
      id
      title
      options {
        name
        values
      }
    }
    userErrors {
      field
      message
    }
  }
}
```

## Response Structure

The mutation returns:
- **product**: The created product object with all requested fields
- **userErrors**: Array of any errors encountered during creation
  - `field`: The field that caused the error
  - `message`: Description of the error

## Best Practices
1. Always check `userErrors` in the response
2. Use meaningful product titles and descriptions
3. Define product options before creating variants
4. Consider SEO settings during product creation
5. Be mindful of the variant creation throttle limits

## Source
Documentation downloaded from: https://shopify.dev/docs/api/admin-graphql/latest/mutations/productCreate
