import sys
import uuid
import argparse
import networkx as nx

from bs4 import BeautifulSoup


def parse_args():
    parser = argparse.ArgumentParser(usage="Visualize DOM tree")
    parser.add_argument("file", help="HTML input file to visualize.")
    return parser.parse_args()


def process_dom(dom):
    def process_node(g: nx.DiGraph, node):
        if not node:
            return
        for child in node.findChildren(recursive=False):
            child.__nodeid__ = uuid.uuid4()
            g.add_node(child.__nodeid__, label=child.name, style="filled")
            g.add_edge(node.__nodeid__, child.__nodeid__)
            colors = {
                "h3": "#e8db4a",
                "a": "#92f268",
                "dt": "#f2acaa",
                "dl": "#aae2f2",
                "p": "#f2aaeb",
            }
            g.nodes[child.__nodeid__]["fillcolor"] = colors.get(child.name, "gray")
            process_node(g, child)
    g = nx.DiGraph()
    dom.__nodeid__ = uuid.uuid4()
    g.add_node(dom.__nodeid__, label=dom.name)
    process_node(g, dom)
    return g


def main():
    args = parse_args()
    with open(args.file) as f:
        dom = BeautifulSoup(f.read(), "html5lib")

    g = process_dom(dom)
    nx.nx_agraph.to_agraph(g).draw("dom.svg", format="svg", prog="dot")


if __name__ == "__main__":
    sys.exit(main())
