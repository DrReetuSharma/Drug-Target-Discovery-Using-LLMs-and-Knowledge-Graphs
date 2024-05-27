import networkx as nx
import xml.etree.ElementTree as ET
from py2neo import Graph, Node, Relationship
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_drugbank(xml_file):
    """Parses DrugBank XML file and builds a NetworkX graph."""
    logging.info(f"Parsing XML file: {xml_file}")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    graph = nx.DiGraph()

    for drug in root.findall('drug'):
        drug_id = drug.find('drugbank-id').text
        drug_name = drug.find('name').text
        drug_type = drug.get('type')
        graph.add_node(drug_id, label=drug_name, type='drug', drug_type=drug_type)
        
        for target in drug.findall('.//target'):
            target_id = target.find('id').text
            target_name = target.find('name').text
            graph.add_node(target_id, label=target_name, type='target')
            graph.add_edge(drug_id, target_id, relationship='targets')
        
        for enzyme in drug.findall('.//enzyme'):
            enzyme_id = enzyme.find('id').text
            enzyme_name = enzyme.find('name').text
            graph.add_node(enzyme_id, label=enzyme_name, type='enzyme')
            graph.add_edge(drug_id, enzyme_id, relationship='interacts_with')
        
        for pathway in drug.findall('.//pathway'):
            pathway_id = pathway.find('smpdb-id').text
            pathway_name = pathway.find('name').text
            graph.add_node(pathway_id, label=pathway_name, type='pathway')
            graph.add_edge(drug_id, pathway_id, relationship='participates_in')
        
        for interaction in drug.findall('.//drug-interactions/drug-interaction'):
            interaction_id = interaction.find('drugbank-id').text
            interaction_name = interaction.find('name').text
            graph.add_node(interaction_id, label=interaction_name, type='drug')
            graph.add_edge(drug_id, interaction_id, relationship='interacts_with')

    logging.info("XML parsing completed")
    return graph

def nx_to_neo4j(nx_graph, neo4j_graph):
    """Transfers NetworkX graph to Neo4j database."""
    logging.info("Transferring graph to Neo4j")
    for node, data in nx_graph.nodes(data=True):
        neo_node = Node(data['type'], id=node, label=data['label'], **data)
        neo4j_graph.merge(neo_node, data['type'], 'id')
    
    for source, target, data in nx_graph.edges(data=True):
        source_node = neo4j_graph.nodes.match(id=source).first()
        target_node = neo4j_graph.nodes.match(id=target).first()
        rel = Relationship(source_node, data['relationship'], target_node)
        neo4j_graph.merge(rel)
    
    logging.info("Graph transfer to Neo4j completed")

if __name__ == "__main__":
    xml_file = 'path_to_drugbank.xml'
    neo4j_url = "bolt://localhost:7687"
    neo4j_user = "neo4j"
    neo4j_password = "password"
    
    logging.info("Starting script")
    
    # Parse the XML file to create a NetworkX graph
    drug_graph = parse_drugbank(xml_file)
    
    # Connect to the Neo4j database
    graph_db = Graph(neo4j_url, auth=(neo4j_user, neo4j_password))
    
    # Transfer NetworkX graph to Neo4j
    nx_to_neo4j(drug_graph, graph_db)
    
    logging.info("Script completed successfully")
