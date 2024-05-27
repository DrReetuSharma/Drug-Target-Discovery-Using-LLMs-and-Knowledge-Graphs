from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from py2neo import Graph, NodeMatcher
import logging

# Initialize the FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Neo4j connection details
NEO4J_URL = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

# Connect to the Neo4j database
graph_db = Graph(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))

# NodeMatcher for querying nodes
node_matcher = NodeMatcher(graph_db)

#Defining pydantic models
class Drug(BaseModel):
    id: str
    name: str
    type: str

class Target(BaseModel):
    id: str
    name: str

class RelationshipResponse(BaseModel):
    source: str
    target: str
    relationship: str

# Pydantic Models: Define the data structures for drug and target responses.
# API Endpoints

@app.get("/drugs/{drug_id}", response_model=Drug)
async def get_drug(drug_id: str):
    """Get drug information by drug ID."""
    logging.info(f"Fetching drug with ID: {drug_id}")
    drug = node_matcher.match("drug", id=drug_id).first()
    if not drug:
        logging.error(f"Drug with ID {drug_id} not found")
        raise HTTPException(status_code=404, detail="Drug not found")
    return Drug(id=drug['id'], name=drug['label'], type=drug['drug_type'])

@app.get("/targets/{target_id}", response_model=Target)
async def get_target(target_id: str):
    """Get target information by target ID."""
    logging.info(f"Fetching target with ID: {target_id}")
    target = node_matcher.match("target", id=target_id).first()
    if not target:
        logging.error(f"Target with ID {target_id} not found")
        raise HTTPException(status_code=404, detail="Target not found")
    return Target(id=target['id'], name=target['label'])

@app.get("/relationships/{drug_id}", response_model=list[RelationshipResponse])
async def get_relationships(drug_id: str):
    """Get all relationships for a given drug ID."""
    logging.info(f"Fetching relationships for drug with ID: {drug_id}")
    drug = node_matcher.match("drug", id=drug_id).first()
    if not drug:
        logging.error(f"Drug with ID {drug_id} not found")
        raise HTTPException(status_code=404, detail="Drug not found")

    relationships = []
    for rel in graph_db.match((drug,), r_type=None):
        target_node = rel.end_node
        relationships.append(RelationshipResponse(
            source=rel.start_node['id'],
            target=target_node['id'],
            relationship=rel.__class__.__name__
        ))

    return relationships


Sure, let's create a detailed src/api/endpoints.py script for a web API that interacts with the drug-target graph. This script will use FastAPI to provide endpoints for querying the graph, such as retrieving drug information, target details, and relationships. We will also include detailed explanations and comments to ensure clarity.

src/api/endpoints.py
Importing Required Libraries
python
Copy code
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from py2neo import Graph, NodeMatcher
import logging

# Initialize the FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Neo4j connection details
NEO4J_URL = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

# Connect to the Neo4j database
graph_db = Graph(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))

# NodeMatcher for querying nodes
node_matcher = NodeMatcher(graph_db)
Defining Pydantic Models
python
Copy code
class Drug(BaseModel):
    id: str
    name: str
    type: str

class Target(BaseModel):
    id: str
    name: str

class RelationshipResponse(BaseModel):
    source: str
    target: str
    relationship: str
Pydantic Models: Define the data structures for drug and target responses.
API Endpoints
python
Copy code
@app.get("/drugs/{drug_id}", response_model=Drug)
async def get_drug(drug_id: str):
    """Get drug information by drug ID."""
    logging.info(f"Fetching drug with ID: {drug_id}")
    drug = node_matcher.match("drug", id=drug_id).first()
    if not drug:
        logging.error(f"Drug with ID {drug_id} not found")
        raise HTTPException(status_code=404, detail="Drug not found")
    return Drug(id=drug['id'], name=drug['label'], type=drug['drug_type'])

@app.get("/targets/{target_id}", response_model=Target)
async def get_target(target_id: str):
    """Get target information by target ID."""
    logging.info(f"Fetching target with ID: {target_id}")
    target = node_matcher.match("target", id=target_id).first()
    if not target:
        logging.error(f"Target with ID {target_id} not found")
        raise HTTPException(status_code=404, detail="Target not found")
    return Target(id=target['id'], name=target['label'])

@app.get("/relationships/{drug_id}", response_model=list[RelationshipResponse])
async def get_relationships(drug_id: str):
    """Get all relationships for a given drug ID."""
    logging.info(f"Fetching relationships for drug with ID: {drug_id}")
    drug = node_matcher.match("drug", id=drug_id).first()
    if not drug:
        logging.error(f"Drug with ID {drug_id} not found")
        raise HTTPException(status_code=404, detail="Drug not found")

    relationships = []
    for rel in graph_db.match((drug,), r_type=None):
        target_node = rel.end_node
        relationships.append(RelationshipResponse(
            source=rel.start_node['id'],
            target=target_node['id'],
            relationship=rel.__class__.__name__
        ))

    return relationships
# GET /drugs/{drug_id}: Fetches drug details by ID.
# GET /targets/{target_id}: Fetches target details by ID.
# GET /relationships/{drug_id}: Fetches all relationships for a given drug ID.


#Running API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Runs the FastAPI application using Uvicorn.

# Import Libraries: Import FastAPI, Pydantic, and Py2neo libraries along with logging.
# Initialize FastAPI App: Create the FastAPI app instance.
# Connect to Neo4j: Establish a connection to the Neo4j database and set up a NodeMatcher for querying nodes.
# Define Pydantic Models: Create models to structure the API responses.
# Create API Endpoints:
# Get Drug: Retrieves drug details by ID.
# Get Target: Retrieves target details by ID.
# Get Relationships: Retrieves all relationships for a specified drug ID.
# Run the API: Use Uvicorn to run the FastAPI application.
