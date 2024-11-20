# Variables
SERVER = uvicorn
APP = main:app
GRAPHQL_URL = http://127.0.0.1:8000/graphql

PRODUCTS_SERVICE_PORT = 8001
ORDERS_SERVICE_PORT = 8002

# Start the Products Service
start_products_service:
	$(SERVER) products:app --reload --host 127.0.0.1 --port $(PRODUCTS_SERVICE_PORT) &

# Start the Orders Service
start_orders_service:
	$(SERVER) orders:app --reload --host 127.0.0.1 --port $(ORDERS_SERVICE_PORT) &

# Start all services
start_all_services: start_products_service start_orders_service
	@echo "All services started!"

# Stop the Products Service
stop_products_service:
	@kill -9 `lsof -t -i:$(PRODUCTS_SERVICE_PORT)` || true

# Stop the Orders Service
stop_orders_service:
	@kill -9 `lsof -t -i:$(ORDERS_SERVICE_PORT)` || true

# Stop all services
stop_all_services: stop_products_service stop_orders_service
	@echo "All services stopped!"

# Run all services (start all services and keep them running)
run: start_all_services
	@echo "All services are running!"

# Stop all services
stop: stop_all_services
	@echo "All services have been stopped."