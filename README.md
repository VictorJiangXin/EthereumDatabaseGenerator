# EthereumDatabaseGenerator
本项目旨在解析本地Geth节点的区块链数据，并将区块链数据存储到SQL Server数据库中。区块链本身是一个高价值的数据库，它将所有链上产生的交易以一定的时间顺序存储在区块链中。我们可以通过分析这些交易信息，去评判区块链的各种参数，比如吞吐量、运行的合约数目等等，从而为以太坊之后的发展做出些许的贡献。当然通过以太坊全节点，可以直接获取到各种需要的信息，但不便于分析，因此我们需要将以太坊全节点上的交易信息转移到数据库中，便于后续工作的使用。

This is a project to parse the Ethereum Blockchain from a local geth node, and store Blockchain data in the SQL Server database. Blockchains are pefect set because they contain every transactions ever made on the network.This is a valueble data if you want to analyze the network. Of course, you can get anything data from a full ethereum node, but it is unconvinent for us to analyze. So we need to store the Blockchian data in the database, to pave the road for the future research.

# Overview（概述）
Geth是Ethereum的Go语言实现版本，也是目前最普及的一个版本。但是Geth将数据进行RLP编码后，再次存入LevelDB中，即使有相关的工具可以使用，也难以直接获取到区块链数据。 因此本项目通过Geth客户端提供的JSON-RPC接口，获取相关的数据。相关的方法可以参照[以太坊JSON-RPC开发文档](https://github.com/ethereum/wiki/wiki/JSON-RPC)

Geth is a official golang implementation of the Ethereum protocol, also the most popular version in the present.But ethereum stores its blockchain in PLP encoded binary blobs within a series of levelDB files and these are surprisingly difficult yto access, even given the avaliable tools. So this project get the blockchain by visiting the JSON-RPC interface which Geth client provided. You can refer to [Ethereum's API](https://github.com/ethereum/wiki/wiki/JSON-RPC)
