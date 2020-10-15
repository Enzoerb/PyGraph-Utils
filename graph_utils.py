class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NodeNotInGraphError(Error):

    def __init__(self, message=None, nodes=None, graph=None):

        if not nodes:
            standard_message = "enterred Nodes are not in Graph"
        elif len(nodes) == 1:
            standard_message = f'{nodes[0].node_id} Node is not in Graph'
        else:
            nodes_to_message = [str(node.node_id) for node in self.nodes]
            nodes_in_message = ', '.join(nodes_to_message)
            standard_message = f'{nodes_in_message} Nodes are not in Graph'

        if graph:
            standard_message += f' {graph}'
        self.message = message if message else standard_message
        super().__init__(self.message)


class NodeAlreadyExists(Error):

    def __init__(self, message=None, node=None):

        self.node = node if node else '{node id not informed}'
        standard_message = f'node {self.node} already exists, try another id'
        self.message = message if message else standard_message
        super().__init__(self.message)


class ConnectionAlreadyExists(Error):

    def __init__(self, message=None, connection=None):

        self.connection = connection if connection\
                          else '{connection id not informed}'
        standard_message = f'connection {self.connection} already exists,\
                             try another id'
        self.message = message if message else standard_message
        super().__init__(self.message)


class GraphAlreadyExists(Error):

    def __init__(self, message=None, graph=None):

        self.graph = graph if graph\
                          else '{graph id not informed}'
        standard_message = f'graph {self.graph} already exists, try another id'
        self.message = message if message else standard_message
        super().__init__(self.message)


class GraphAlreadyHasNodes(Error):

    def __init__(self, message=None):

        standard_message = 'Can not execute action in Graph with Nodes'
        self.message = message if message else standard_message
        super().__init__(self.message)


class Node:
    created_nodes = set()

    def __init__(self, node_id=None, state: str = None,
                 connections: '{Connection}' = None, graphs: '{Graph}' = None,
                 weight: int = 1):
        if node_id in Node.created_nodes:
            raise NodeAlreadyExists(node=node_id)
        self.__node_id = node_id if node_id else id(self)
        self.state = state
        self.weight = weight
        self.connections = set(connections) if connections else set()
        self.graphs = set(graphs) if graphs else set()
        Node.created_nodes.add(self.__node_id)

    @property
    def node_id(self):
        return self.__node_id

    @node_id.setter
    def node_id(self, id):
        if id in Node.created_nodes:
            raise NodeAlreadyExists(node=id)
        Node.created_nodes.add(id)
        Node.created_nodes.remove(self.__node_id)
        self.__node_id = id

    @node_id.deleter
    def node_id(self):
        if self.__node_id in Node.created_nodes:
            Node.created_nodes.remove(self.__node_id)
        del self.__node_id

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return False

    def __hash__(self):
        return hash((self.__node_id))

    def __repr__(self):
        connections_ids = [str(connection.connection_id)
                           for connection in self.connections]
        connections = ', '.join(connections_ids)
        graphs_ids = [str(graph.graph_id)
                      for graph in self.graphs]
        graphs = ', '.join(graphs_ids)
        return_text = f'Node(node_id={self.node_id}'
        return_text += f', state={self.state}'
        return_text += f', connections=set([{connections}])'
        return_text += f', graphs=set([{graphs}])'
        return return_text

    def __del__(self):
        for connection in self.connections:
            del connection
        for graph in self.graphs:
            graph.remove_node(self)
        del self.node_id
        del self


class Connection:
    created_connections = set()

    def __init__(self, connection_id=None,
                 node_from: Node = None, node_to: Node = None,
                 weight: int = 1):
        if id in Connection.created_connections:
            raise ConnectionAlreadyExists(connection=id)
        self.__connection_id = connection_id if connection_id else id(self)
        self.node_from = node_from
        self.node_to = node_to
        self.weight = weight
        Connection.created_connections.add(self.__connection_id)

    @property
    def connection_id(self):
        return self.__connection_id

    @connection_id.setter
    def connection_id(self, id):
        if id in Connection.created_connections:
            raise ConnectionAlreadyExists(connection=id)
        Connection.created_connections.add(id)
        Connection.created_connections.remove(self.__connection_id)
        self.__connection_id = id

    @connection_id.deleter
    def connection_id(self):
        if self.__connection_id in Connection.created_connections:
            Connection.created_connections.remove(self.__connection_id)
        del self.__connection_id

    def same(self, other):
        if isinstance(other, Connection):
            weight_condition = self.weight = other.weight
            from_condition = self.node_from == other.node_from
            to_condition = self.node_to == other.node_to
            return weight_condition and from_condition and to_condition
        return False

    def __eq__(self, other):
        if isinstance(other, Connection):
            return self.connection_id == other.connection_id
        return False

    def __hash__(self):
        return hash((self.__connection_id))

    def __repr__(self):
        return_text = f'Connection(connection_id={self.connection_id}'
        return_text += f', node_from={self.node_from.node_id}'
        return_text += f', node_to={self.node_to.node_id}'
        return_text += f', weight={self.weight})'
        return return_text

    def __str__(self):
        return_text = f'{self.node_from.node_id} '
        return_text += f'--{self.weight}-->'
        return_text += f' {self.node_to.node_id}'
        return return_text

    def __del__(self):
        del self.connection_id
        del self


class Graph:
    created_graphs = set()

    def __init__(self, graph_id=None, nodes: '{Node}' = None,
                 connections: '{Connection}' = None,
                 is_directional: 'bool' = False, is_weighted: 'bool' = False):
        if id in Graph.created_graphs:
            raise GraphAlreadyExists(graph=id)
        self.__graph_id = graph_id if graph_id else id(self)
        self.nodes = set(nodes) if nodes else set()
        self.connections = set(connections) if connections else set()
        self.is_directional = is_directional
        self.is_weighted = is_weighted
        Graph.created_graphs.add(self.__graph_id)

    @property
    def graph_id(self):
        return self.__graph_id

    @graph_id.setter
    def graph_id(self, id):
        if id in Graph.created_graphs:
            raise GraphAlreadyExists(graph=id)
        Graph.created_graphs.add(id)
        Graph.created_graphs.remove(self.__graph_id)
        self.__graph_id = id

    @graph_id.deleter
    def graph_id(self):
        if self.__graph_id in Graph.created_graphs:
            Graph.created_graphs.remove(self.__graph_id)
        del self.__graph_id

    def remove_node(self, node):
        self.nodes.remove(node)

    def include_node(self, node):
        self.nodes.add(node)

    def remove_connection(self, connection):
        self.connections.remove(connection)

    def add_connection(self, node_1, node_2, weight=1, is_directional=None):
        is_directional = is_directional if is_directional is not None\
                         else self.is_directional

        connection_1 = Connection(node_from=node_1, node_to=node_2,
                                  weight=weight)
        connection_2 = Connection(node_from=node_2, node_to=node_1,
                                  weight=weight)

        nodes_not_in_graph = {node_1, node_2}.difference(self.nodes)
        if len(nodes_not_in_graph) > 0:
            raise NodeNotInGraphError(nodes=list(nodes_not_in_graph),
                                      graph=self.graph_id)

        node_1.connections.add(connection_1)
        self.connections.add(connection_1)
        if not is_directional:
            node_2.connections.add(connection_2)
            self.connections.add(connection_2)

        return True

    @staticmethod
    def csv_to_matrix(csv_file, separator=','):
        return [[True, True]]

    def matrix_to_graph(self, matrix):
        if len(self.nodes) > 0:
            message = 'The Graph you are trying to create already has nodes'
            raise GraphAlreadyHasNodes(message)
        return True

    def csv_to_graph(self, csv_file, separator=','):
        matrix = self.csv_to_graph()
        self.matrix_to_graph(matrix)

    def copy_connections(self, other):
        if not isinstance(other, Graph):
            message = f'{other} is a {str(type(other))[7:-1]}, not a Graph'
            raise TypeError(message)

        old_new_nodes = [(node, Node()) for node in self.nodes]
        for _, new in old_new_nodes:
            other.include_node(new)
        checks = list()
        for old_from, new_from in old_new_nodes:
            new_from.weight = old_from.weight
            new_from.state = old_from.state
            new_from.graphs.add(other)
            for connection in old_from.connections:
                to_connect = connection.node_to
                for old_to, new_to in old_new_nodes:
                    if to_connect == old_to:
                        other.add_connection(new_from, new_to,
                                             connection.weight,
                                             is_directional=True)
                        print(checks)
                        break

        return other

    def __eq__(self, other):
        if isinstance(other, Graph):
            return self.graph_id == other.graph_id
        return False

    def __hash__(self):
        return hash((self.__graph_id))

    def __add__(self, other):
        if not isinstance(self, Graph):
            message = f'{self} is a {str(type(self))[7:-1]}, not a Graph'
            raise TypeError(message)
        if not isinstance(other, Graph):
            message = f'{other} is a {str(type(other))[7:-1]}, not a Graph'
            raise TypeError(message)

        new_graph = Graph()
        is_directional = self.is_directional or other.is_directional
        is_weighted = self.is_weighted or other.is_weighted

        self.copy_connections(new_graph)
        other.copy_connections(new_graph)
        new_graph.is_directional = is_directional
        new_graph.is_weighted = is_weighted

        return new_graph

    def __repr__(self):
        nodes = ', '.join([str(node.node_id) for node in self.nodes])
        connections_ids = [str(connection.connection_id)
                           for connection in self.connections]
        connections = ', '.join(connections_ids)
        return_text = f'Graph(graph_id={self.graph_id}, nodes=set([{nodes}])'
        return_text += f', is_directional={self.is_directional}'
        return_text += f', is_weighted={self.is_weighted})'
        return_text += f', connections=set([{connections}])'
        return return_text

    def __del__(self):
        del self.graph_id
        del self


if __name__ == '__main__':
    node = [Node(i) for i in range(7)]
    graph_1 = Graph(nodes={node[1], node[2], node[3]},
                    is_directional=False,
                    is_weighted=True)
    graph_2 = Graph(nodes={node[4], node[5], node[6]},
                    is_directional=False,
                    is_weighted=False)

    graph_1.add_connection(node[1], node[2])
    graph_1.add_connection(node[1], node[3])
    graph_2.add_connection(node[5], node[6])
    new_graph = graph_1 + graph_2

    for connection in new_graph.connections:
        print(connection)
