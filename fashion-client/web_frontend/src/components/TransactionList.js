import axios from 'axios';
import React, {Component} from 'react';
import { Table } from 'antd';

const { Column } = Table;

function addShortValues(transaction) {
    transaction['sender_short'] = transaction.sender.substring(0, 16);
    transaction['receiver_short'] = transaction.receiver.substring(0,16);
    transaction['scantrust_id_short'] = transaction.scantrust_id.substring(0,17);
    return transaction;
}


class TransactionList extends Component {
    state = {
        transactions: []
    };

    componentDidMount() {
    axios.get(`http://127.0.0.1:8888/transactions/`)
      .then(res => {
        const transactions = res.data.data.map(
            (transaction) => addShortValues(transaction)
        );
        this.setState({ transactions: transactions });
        console.log(this.state.transactions)
      })
    }

    render() {
        return (
            <div className="TransactionList">
                <Table dataSource={this.state.transactions}>
                    <Column
                      title="Name"
                      dataIndex="item_name"
                      key="item_name"
                    />
                    <Column
                      title="Color"
                      dataIndex="item_color"
                      key="item_color"
                    />
                    <Column
                      title="Size"
                      dataIndex="item_size"
                      key="item_size"
                    />
                    <Column
                      title="Scantrust ID"
                      key="scantrust_id"
                      render={(text, record) => (
                        <span>
                          <a href={'items/' + record.scantrust_id}>{record.scantrust_id_short}</a>
                        </span>
                     )}
                    />
                    <Column
                      title="Sender"
                      key="sender"
                      render={(text, record) => (
                        <span>
                          <a href={'users/' + record.sender}>{record.sender_short}</a>
                        </span>
                     )}
                    />
                    <Column
                      title="Receiver"
                      key="receiver"
                      render={(text, record) => (
                        <span>
                          <a href={'users/' + record.receiver}>{record.receiver_short}</a>
                        </span>
                     )}
                    />
                  </Table>
            </div>
        );
    }
}

export default TransactionList;