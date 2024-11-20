import strawberry
from fastapi import FastAPI, HTTPException
from strawberry.fastapi import GraphQLRouter
from datetime import datetime
from typing import List


# Define the Product type with Strawberry
@strawberry.type
class Product:
    id: int
    name: str
    description: str
    price: float


# Sample in-memory storage for products
products_db = []


# GraphQL Queries
@strawberry.type
class Query:
    @strawberry.field
    def all_products(self) -> List[Product]:
        return products_db

    @strawberry.field
    def get_product(self, id: int) -> Product:
        for product in products_db:
            if product.id == id:
                return product
        return None


# GraphQL Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    def get_server_time(self) -> str:
        # Get the current server time and return it in ISO 8601 format
        return datetime.now().isoformat()

    @strawberry.mutation
    def add_product(
        self,
        name: str,
        description: str,
        price: float,
        is_authorized: bool,
    ) -> Product:
        if not is_authorized:
            raise HTTPException(status_code=403, detail="Unauthorized")
        new_product = Product(
            id=len(products_db) + 1,  # Simple id generation
            name=name,
            description=description,
            price=price,
        )
        products_db.append(new_product)
        return new_product


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

    uvicorn.run(app, host="127.0.0.1", port=8001)
