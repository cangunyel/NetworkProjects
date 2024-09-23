import networkx as nx
import random
import heapq
import time
import matplotlib.pyplot as plt

#####################
#Can Günyel 150200049
#####################

#generate inter AS graph
def generate_topology(num_nodes):
    G = nx.random_internet_as_graph(num_nodes,seed=150200049)
    return G
#transform visited nodes to edge pairs
def create_pairs(node_list):
    return [(min(node_list[i], node_list[i + 1]), max(node_list[i], node_list[i + 1])) for i in range(len(node_list) - 1)]

#give random cost values to edges in the topology
def assign_costs(graph):
    cost_list = {}

    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        costs = {}
        
        for neighbor in neighbors:
            # Check if the cost from neighbor to node is already assigned
            if neighbor not in cost_list or node not in cost_list[neighbor]["costs"]:
                # If not assigned, generate a random cost
                cost = random.randint(1, 10)
            else:
                # If already assigned, use the same cost
                cost = cost_list[neighbor]["costs"][node]

            costs[neighbor] = cost

        cost_list[node] = {"neighbors": neighbors, "costs": costs}

    return cost_list

#displays topology and shortest path in a plot
def visualize_graph(graph, visited_nodes, cost_list):
    visited_edges = create_pairs(visited_nodes)
    #mark shortest_path's edges 
    edge_colors = ['red' if edge in visited_edges else 'black' for edge in graph.edges()]

    #give costs as weights to topology
    edge_labels = {(min(edge[0], edge[1]), max(edge[0], edge[1])): cost_list[edge[0]]["costs"][edge[1]] for edge in graph.edges()}

    pos = nx.spring_layout(graph) 

    #draw topology
    nx.draw(graph, pos, with_labels=True, font_weight='bold', edge_color=edge_colors,node_size=100,font_size=7)
    #make shortest_paths edges red
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='blue',font_size=8)

#dijkstra algorithm which will calculate shortest_path and total_cost
def dijkstra(cost_list, source, destination):
    # Initialize distances to all nodes as infinity
    distances = {node: float("inf") for node in cost_list}
    # The distance from the source node to itself is 0
    distances[source] = 0
    # Initialize priority queue with the source node and its distance
    priority_queue = [(0, source)]
    previous_nodes = {node: None for node in cost_list}

    
    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)
        # If the current path is higher, skip to the next iteration
        if current_dist > distances[current_node]:
            continue
        # Explore neighbors of the current node
        for neighbor, cost in cost_list[current_node]["costs"].items():
            # Calculate the new distance from the source to the neighbor
            new_dist = current_dist + cost
            # Update the distance if the new distance is shorter
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                # Update the previous node for the neighbor
                previous_nodes[neighbor] = current_node
                # Add the neighbor to the priority queue with the new distance
                heapq.heappush(priority_queue, (new_dist, neighbor))

    # Reconstruct the path from destination to source
    path = []
    current = destination
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    # Return the total distance and the shortest path for test data
    return distances[destination], path



#perfrom link state routing 
def link_state(graph, cost_list, random_source, random_destination):
    forwarding_table = {}
    result_path = []
    result_cost = 0

    # Construct forwarding table for all nodes
    for source_node in graph.nodes():
        node_table = {}
        for destination_node in graph.nodes():
            if source_node != destination_node:
                total_cost, visited_nodes = dijkstra(cost_list, source_node, destination_node)
                if source_node == random_source and destination_node == random_destination:
                    result_cost = total_cost
                    result_path = visited_nodes
                next_hop = visited_nodes[1] if len(visited_nodes) > 1 else 'inf'
                node_table[destination_node] = next_hop
        forwarding_table[source_node] = node_table

    # Write forwarding tables to a file
    with open("link_state_forwarding_table.txt", 'w') as file:
        for source_node, destinations in forwarding_table.items():
            file.write("-----------------------------------\n")
            file.write(f"Forwarding Table for Node {source_node}:\n")
            file.write("Destination Node      Outgoing Link\n")
            for destination_node, next_hop in destinations.items():
                file.write(f"{destination_node}                       ({source_node},{next_hop})\n")

    # Return test nodes' total_cost and shortest_path
    return result_cost, result_path
 





###########################################################33













# Bellman-Ford algorithm for Distance Vector Routing
def bellman_ford(time_step,cost_list, source, destination):
    distances = {node: float("inf") for node in cost_list}
    distances[source] = 0
    previous_nodes = {node: None for node in cost_list}

    # Relax edges repeatedly
    for _ in range(time_step):#to update wholoe topoplogy we need diameter iterative calls 
        for node in cost_list:
            for neighbor, cost in cost_list[node]["costs"].items():
                if distances[node] + cost < distances[neighbor]:
                    distances[neighbor] = distances[node] + cost
                    previous_nodes[neighbor] = node

    # Reconstruct the path from destination to source
    path = []
    current = destination
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    return distances[destination], path

# Perform Distance Vector routing
def distance_vector(graph, cost_list, random_source, random_destination):
    forwarding_table = {}
    result_path = []
    result_cost = 0 
    diameter=nx.diameter(graph)#calculate diameter of graph
    start_time=0
    end_time=0
    with open("distance_vector_forwarding_table.txt", 'a') as file:
        for source_node in graph.nodes():
            file.write("-----------------------------------\n")
            file.write(f"Forwarding Table for Node {source_node} at t={0}:\n")
            file.write("Destination Node      Outgoing Link\n")
            for destination_node in graph.nodes():
                if destination_node in cost_list[source_node]["neighbors"]:
                    file.write(f"{destination_node}                       ({source_node},{destination_node})\n")
                else:
                    if destination_node!=source_node:
                        file.write(f"{destination_node}                       ({source_node},inf)\n")




    # Construct forwarding table for all nodes
    for time_step in range(diameter):
        if time_step==diameter-1:
            start_time= time.time()
        for source_node in graph.nodes():
            node_table = {}
            for destination_node in graph.nodes():
                if source_node != destination_node:
                    total_cost, visited_nodes = bellman_ford(time_step+1,cost_list ,source_node, destination_node)
                    if source_node == random_source and destination_node == random_destination:
                        result_cost = total_cost
                        result_path = visited_nodes
                    next_hop = visited_nodes[1] if len(visited_nodes) > 1 else 'inf'
                    node_table[destination_node] = next_hop
            forwarding_table[source_node] = node_table
        if time_step==diameter-1:
            end_time= time.time()
        # Write forwarding tables to a file
        with open("distance_vector_forwarding_table.txt", 'a') as file:
            for source_node, destinations in forwarding_table.items():
                file.write("-----------------------------------\n")
                file.write(f"Forwarding Table for Node {source_node} at t={time_step+1}:\n")
                file.write("Destination Node      Outgoing Link\n")
                for destination_node, next_hop in destinations.items():
                    file.write(f"{destination_node}                       ({source_node},{next_hop})\n")

    # Return test nodes' total_cost and shortest_path
    return result_cost, result_path,end_time-start_time





######################################################
def main():
    #to clear distance_vector_forwarding_table.txt
    with open("distance_vector_forwarding_table.txt", 'w') as file:
        pass
    num_nodes = int(input("Enter the number of nodes: "))
    
    graph = generate_topology(num_nodes)#create topology
    cost_list = assign_costs(graph)#assign cost to edges

    #choosing random source node to test
    source = random.choice(list(graph.nodes()))
    # source=12
    
    #choosing random destination node to test
    destination=random.choice(list(graph.nodes()))
    # destination=13
    while(destination==source):#chose another source until source and destiation are different 
        destination=random.choice(list(graph.nodes()))
    #print test nodes     
    print(f"Source Node: {source}")
    print(f"Destination Node: {destination}")

    # Create forward tables for whole topology using Link State and return test nodes results, calculate runtime
    start_time = time.time()
    LS_cost, LS_path = link_state(graph, cost_list, source, destination)
    end_time = time.time()

    # Visualize shortest path between test nodes for Link State
    # show_shortest_path(graph, LS_path, cost_list)

    # Print results for Link State method
    print(f"Visited Nodes in order: {LS_path}")
    print(f"Total hops: {len(LS_path)-1}")  # -1 for calculating edge number from node number
    print(f"Total cost: {LS_cost}")
    print(f"Packet Transmission Delay: {LS_cost*0.4+len(LS_path)-1*0.7} milliseconds")

    # Print Link State runtime
    print(f"Link State Runtime: {end_time - start_time:.4f} seconds")
##########################################
    # Create forward tables for whole topology using Distance Vector and return test nodes results, calculate runtime
    
    DV_cost, DV_path,runtime = distance_vector(graph, cost_list, source, destination)
    

    # Visualize shortest path between test nodes for Distance Vector
    visualize_graph(graph, DV_path, cost_list)

    # Print results for Distance Vector method
    print(f"Visited Nodes in order: {DV_path}")
    print(f"Total hops: {len(DV_path)-1}")  # -1 for calculating edge number from node number
    print(f"Total cost: {DV_cost}")
    print(f"Packet Transmission Delay: {DV_cost*0.4+len(DV_path)-1*0.7} milliseconds")

    # Print Distance Vector runtime
    print(f"Distance Vector Runtime: {runtime:.4f} seconds")
##########################################
    # Show topology with shortest path between test nodes
    
    plt.show()
    asd=3

if __name__ == "__main__":
    main()