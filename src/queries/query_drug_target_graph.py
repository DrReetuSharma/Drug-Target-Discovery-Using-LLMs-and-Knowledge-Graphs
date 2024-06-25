
#Following the integration of external data into the Neo4j database, the next logical step is to create a script that facilitates querying the database for specific insights or analytics. This can be done through a script that defines custom queries and operations to retrieve, analyze, and visualize data from the Neo4j database.

#src/queries/query_drug_target_graph.py
#This script will include custom queries to extract insights from the drug-target graph and can also include functions to perform analyses like finding shortest paths, subgraph extractions, and other graph-related queries.

#Importing Required Libraries

from py2neo import Graph
import networkx as nx
import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Neo4j connection details
NEO4J_URL = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

# Connect to the Neo4j database
graph_db = Graph(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))
Function to Retrieve Nodes and Relationships
python
Copy code
def get_all_drugs():
    """Retrieve all drug nodes from the Neo4j database."""
    query = "MATCH (d:drug) RETURN d.id as id, d.label as name, d.drug_type as type"
    results = graph_db.run(query).data()
    logging.info(f"Retrieved {len(results)} drugs")
    return results

def get_all_targets():
    """Retrieve all target nodes from the Neo4j database."""
    query = "MATCH (t:target) RETURN t.id as id, t.label as name"
    results = graph_db.run(query).data()
    logging.info(f"Retrieved {len(results)} targets")
    return results

def get_drug_target_relationships():
    """Retrieve all drug-target relationships from the Neo4j database."""
    query = """
    MATCH (d:drug)-[r:targets]->(t:target)
    RETURN d.id as drug_id, t.id as target_id, r
    """
    results = graph_db.run(query).data()
    logging.info(f"Retrieved {len(results)} drug-target relationships")
return results
#Function to Analyze Data
def find_shortest_path_between_drugs(drug_id_1, drug_id_2):
    """Find the shortest path between two drugs in the Neo4j database."""
    query = f"""
    MATCH (d1:drug {{id: '{drug_id_1}'}}), (d2:drug {{id: '{drug_id_2}'}}),
          p = shortestPath((d1)-[*]-(d2))
    RETURN p
    """
    result = graph_db.run(query).evaluate()
    if result:
        logging.info(f"Found shortest path between {drug_id_1} and {drug_id_2}")
    else:
        logging.warning(f"No path found between {drug_id_1} and {drug_id_2}")
    return result

def visualize_graph():
    """Visualize the drug-target graph using NetworkX and Matplotlib."""
    query = """
    MATCH (n)-[r]->(m)
    RETURN n.id as source, m.id as target, type(r) as relationship
    """
    results = graph_db.run(query).data()
    
    G = nx.DiGraph()
    
    for result in results:
        G.add_edge(result['source'], result['target'], relationship=result['relationship'])
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", 
            node_shape="o", alpha=0.75, linewidths=40)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['relationship'] for u, v, d in G.edges(data=True)})
    plt.title("Drug-Target Graph Visualization")
    plt.show()

#Data Retrieval Functions: Define functions to retrieve drugs, targets, and their relationships from Neo4j.
#Shortest Path Function: Implement a function to find the shortest path between two drugs.
#Graph Visualization: Use NetworkX and Matplotlib to visualize the drug-target graph.

if __name__ == "__main__":
    logging.info("Starting query script")
    
    # Retrieve and log all drugs
    drugs = get_all_drugs()
    for drug in drugs:
        logging.info(f"Drug: {drug['id']}, Name: {drug['name']}, Type: {drug['type']}")
    
    # Retrieve and log all targets
    targets = get_all_targets()
    for target in targets:
        logging.info(f"Target: {target['id']}, Name: {target['name']}")
    
    # Retrieve and log all drug-target relationships
    relationships = get_drug_target_relationships()
    for rel in relationships:
        logging.info(f"Drug {rel['drug_id']} targets {rel['target_id']}")
    
    # Example of finding shortest path
    path = find_shortest_path_between_drugs("DB00001", "DB00002")
    if path:
        logging.info(f"Shortest path: {path}")
    
    # Visualize the graph
    visualize_graph()
    
    logging.info("Query script completed successfully")
# Main Execution Block
if __name__ == "__main__":
    logging.info("Starting query script")
    
    # Retrieve and log all drugs
    drugs = get_all_drugs()
    for drug in drugs:
        logging.info(f"Drug: {drug['id']}, Name: {drug['name']}, Type: {drug['type']}")
    
    # Retrieve and log all targets
    targets = get_all_targets()
    for target in targets:
        logging.info(f"Target: {target['id']}, Name: {target['name']}")
    
    # Retrieve and log all drug-target relationships
    relationships = get_drug_target_relationships()
    for rel in relationships:
        logging.info(f"Drug {rel['drug_id']} targets {rel['target_id']}")
    
    # Example of finding shortest path
    path = find_shortest_path_between_drugs("DB00001", "DB00002")
    if path:
        logging.info(f"Shortest path: {path}")
    
    # Visualize the graph
    visualize_graph()
    
    logging.info("Query script completed successfully")

# Retrieve Data: Fetch and log details of drugs, targets, and their relationships.
# Shortest Path Example: Demonstrate finding the shortest path between two example drugs.
# Graph Visualization: Generate and display a visualization of the entire graph.
# Summary
# This script provides a comprehensive approach to querying and analyzing the drug-target graph in the Neo4j database. It includes:

# Data Retrieval: Functions to fetch drugs, targets, and relationships.
# Analysis: A function to find the shortest path between two drugs.
# Visualization: A function to visualize the graph using NetworkX and Matplotlib.
# Execution Block: Demonstrates usage of the retrieval, analysis, and visualization functions.
