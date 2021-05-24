#!/usr/bin/env python3
"""
Created on Mon May 17 13:15:13 2021

@author: erithus
"""

import os
import re

import py010parser
import requests
from bs4 import BeautifulSoup

nodes_in_files = {}
types_used = {}

BT_Repo = "https://www.sweetscape.com/010editor/repository/templates/"


def scrapeSite(sitename: str):
    target = os.path.join(os.getcwd(), "templateRepo")
    if not (os.path.isdir(target)):
        os.mkdir("templateRepo")  # Where the repos get saved

    sitecontents = requests.get(sitename)
    soup = BeautifulSoup(sitecontents.content, "html.parser")
    links = soup.find_all("a", href=re.compile("../files/"))

    for link in links:
        full_link = BT_Repo[:-10] + "files/" + link.text
        link_contents = requests.get(full_link)
        link_soup = BeautifulSoup(link_contents.content, "html.parser")
        write_file = open(os.path.join(target, link.text), "w")
        write_file.write(link_soup.text)
        write_file.close()
        print("Wrote file: " + link.text + ", go and look")


def discover_types_used():
    currentdir = os.getcwd()
    target = os.path.join(os.getcwd(), "templateRepo")
    os.chdir(target)
    for filename in os.listdir(target):
        types_used.clear()
        try:
            ast = py010parser.parse_file(filename)
            node_explorer(ast)
            nodes_in_files[filename] = dict(
                sorted(types_used.items(), key=lambda item: item[1], reverse=True)
            )
        except:
            print("File type sucks, can't do " + filename)
    os.chdir(currentdir)


def node_explorer(node: py010parser.c_ast.Node):
    if type(node) not in types_used:
        types_used[type(node)] = 1
    else:
        types_used[type(node)] += 1
    if hasattr(node, "children") and len(node.children()) > 0:
        for elem_name, elem in node.children():
            if isinstance(elem, list):
                for child in elem:
                    node_explorer(child)
            else:
                node_explorer(elem)
