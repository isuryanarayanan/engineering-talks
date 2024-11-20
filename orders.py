import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
import httpx


# Define the Product and Order types with Federation
@strawberry.federation.type(keys=["id"])
class Order:
    id: int
    product: "Product"
    total: float


@strawberry.type
class Product:
    id: int
    name: str
    description: str
    price: float


# Sample in-memory storage for orders
orders_db = []


# GraphQL Queries
@strawberry.type
class Query:
    @strawberry.field
    async def all_orders(self) -> List[Order]:
        return orders_db

    @strawberry.field
    async def get_order(self, id: int) -> Optional[Order]:
        for order in orders_db:
            if order.id == id:
                return order
        return None


# GraphQL Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_order(self, product_id: int) -> Order:
        async with httpx.AsyncClient() as client:
            # Fetch product details from the Products Service
            products_response = await client.post(
                "http://127.0.0.1:8001/graphql",
                json={
                    "query": """
                    query getProduct($id: Int!) {
                        getProduct(id: $id) {
                            id
                            name
                            price
                            description
                        }
                    }
                    """,
                    "variables": {"id": product_id},
                },
            )
            product = products_response.json()

            if not product.get("data"):
                raise ValueError("Product not found")

            product = product.get("data", {}).get("getProduct", [])

            # Calculate the total price
            total_price = product["price"]
            product = Product(**product)

            # Create the order
            new_order = Order(
                id=len(orders_db) + 1,
                product=product,
                total=total_price,
            )
            orders_db.append(new_order)
            return new_order


# Create the schema
schema = strawberry.federation.Schema(query=Query, mutation=Mutation)

# FastAPI app
app = FastAPI()

# GraphQL router
graphql_app = GraphQLRouter(schema)

# Add the GraphQL router to the FastAPI app
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8002)
