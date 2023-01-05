# Happy-Zhitu 

The all-in-one collection of [知兔](https://zhitulist.com/), including algorithm, backend, runner, etc.

# 1 Quick Start

## 1.1 Clone the repository 

Since the repository contains many submodules, you can clone in this way:

```bash
git clone git@github.com:hcmdgh/Happy-Zhitu.git --recurse-submodules
```

## 1.2 Add to PYTHONPATH 

To make full use of JOJO series packages, you can follow these steps:

Firstly, create a directory and some links: 

```bash
#!/bin/bash

set -eux 

mkdir ~/python_package 
ln -s <Repository-Directory>/JOJO-Elasticsearch/jojo_es ~/python_package 
ln -s <Repository-Directory>/JOJO-JanusGraph/jojo_janusgraph ~/python_package 
ln -s <Repository-Directory>/JOJO-MySQL/jojo_mysql ~/python_package 
```

Then, add the following line to "~/.bashrc": 

```bash
export PYTHONPATH=$PYTHONPATH:~/python_package
```

Restart the shell, and you can be happy with Zhitu! 
