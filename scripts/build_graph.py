import networkx as nx
import xml.etree.ElementTree as ET

def parse_drugbank(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    graph = nx.DiGraph()

    for drug in root.findall('drug'):
        drug_id = drug.find('drugbank-id').text
        drug_name = drug.find('name').text
        graph.add_node(drug_id, label=drug_name, type='drug')
        
        for target in drug.find('targets').findall('target'):
            target_id = target.find('id').text
            target_name = target.find('name').text
            graph.add_node(target_id, label=target_name, type='target')
            graph.add_edge(drug_id, target_id, relationship='targets')
    
    return graph

if __name__ == "__main__":
    xml_file = 'path_to_drugbank.xml'
    drug_graph = parse_drugbank(xml_file)
    nx.write_gml(drug_graph, 'drug_target_graph.gml')

