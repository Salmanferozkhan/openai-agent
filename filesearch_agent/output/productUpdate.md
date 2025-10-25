# 
mutation {
  productUpdate(product: {
    id: "gid://shopify/Product/1234567890",
    title: "Sample T-Shirt — Updated",
    descriptionHtml: "<strong>Updated description with new details</strong>",
    vendor: "Example Brand",
    productType: "Apparel",
    tags: ["summer","cotton","updated"],
    seo: {title: "Sample T-Shirt - Example Brand", description: "Buy the Sample T-Shirt from Example Brand"},
    metafields: [
      {namespace: "custom", key: "material", value: "100% Cotton", type: "single_line_text_field"}
    ]
  }) {
    product {
      id
      title
      tags
      seo {
        title
        description
      }
      metafields(first: 10) {
        edges {
          node {
            id
            namespace
            key
            value
          }
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}