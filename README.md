```graphql
query MyQuery {
  allProducts {
    description
    id
    name
    price
  }
  getProduct(id: 1) {
    description
    id
  }
}
```

```graphql
mutation MyMutation {
  addProduct(
    name: "Laptop"
    description: "A laptop"
    price: 69420.00
    isAuthorized: true
  ) {
    id
    name
    description
    price
  }
}
```

```graphql
query {
  allProducts {
    id
    name
    price
  }

  allOrders {
    id
    total
    products {
      id
      name
      price
    }
  }
}
```
