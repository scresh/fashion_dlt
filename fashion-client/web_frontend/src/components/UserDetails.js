import axios from 'axios';
import React, {Component} from 'react';
import { Card, Row, Col, List, Icon, Button } from 'antd';
import {Link} from "react-router-dom";
const { Meta } = Card;


function makeDict(transactions, user) {
    const dict = {
        transactions: [],
        items: [],
    };

    for (let i=0; i < transactions.length; i++){
        dict.transactions.push(
            {
                sender: transactions[i].sender,
                receiver: transactions[i].receiver,
                scantrust_id: transactions[i].scantrust_id,
            }
        );
        if (transactions[i].receiver === user){
            dict.items.push(
                {
                    scantrust_id: transactions[i].scantrust_id,
                    item_name: transactions[i].item_name,
                    item_size: transactions[i].item_size,
                    item_img: transactions[i].item_img,
                }
            )
        }else {
            for (let j=0; j < dict.items.length; j++) {
                if (transactions[i].scantrust_id === dict.items[j].scantrust_id){
                    dict.items.splice(j, 1);
                    break;
                }
            }
        }
    }

    return dict;
}

class UserDetails extends Component {
    state = {
        userAddress: this.props.match.params.userID,
        transactions: [],
        items: [],
        activeButtons: false,
    };

    componentDidMount() {
        if (this.props.cookies.get('public_key') && this.props.cookies.get('private_key')) {
            if (this.props.cookies.get('public_key')  === this.state.userAddress){
                this.setState({activeButtons: true});
            }
        }
    axios.get(`http://127.0.0.1:8888/transactions/?address=` + this.state.userAddress)
      .then(res => {this.setState(makeDict(res.data.data, this.state.userAddress));
      })
    }

    render() {
            return (
                <div className={this.state.userAddress}>
                    <Row>
                        <Col span={18} offset={3}>
                            <Button
                                type="primary"
                                block
                                disabled={!this.state.activeButtons}
                            >
                                <Link to={'/transfer'}>Create item</Link>
                            </Button>
                            <Card
                                title={'User: ' + this.state.userAddress}
                            >
                                <h3 style={{ margin: '16px 0' }}>Owned items</h3>
                                <List
                                    pagination={{
                                            pageSize: 6,
                                        }}
                                    grid={{ gutter: 16, column: 6 }}
                                    dataSource={this.state.items}
                                    renderItem={item => (
                                      <List.Item>
                                        <Card
                                            actions={[
                                                <Button
                                                    type="primary"
                                                    block
                                                    disabled={!this.state.activeButtons}
                                                >
                                                   <Link to={'/transfer/'  + item.scantrust_id}>Send item</Link>
                                                </Button>,]}
                                            cover={<img
                                                alt={item.scantrust_id.substring(0,16)}
                                                src={item.item_img}
                                                style={{   padding: '10px'}}
                                            />}
                                        >
                                        <Meta
                                          title={<a
                                                  href={'../items/' + item.scantrust_id}
                                              >
                                                  {item.scantrust_id.substring(0,12)}
                                              </a>}
                                          description={
                                              item.item_name + ' [' + item.item_size + ']'
                                          }
                                        />
                                      </Card>
                                    </List.Item>
                                    )
                                }/>
                                <p/>
                                <List
                                    pagination={{
                                        pageSize: 6,
                                    }}
                                  header={<div>Transactions history</div>}
                                  bordered
                                  dataSource={this.state.transactions}
                                  renderItem={item => (
                                      <List.Item>
                                          <a href={'../users/' + item.sender}>{item.sender.substring(0,48)}</a>
                                          <Icon type="caret-right" style={{ fontSize: '20px'}} />
                                          <a href={'../items/' + item.scantrust_id} style={{ fontWeight: 'bold'}}>
                                              {item.scantrust_id.substring(0,48)}
                                          </a>
                                          <Icon type="caret-right" style={{ fontSize: '20px'}} />
                                          <a href={'../users/' + item.receiver}>{item.receiver.substring(0,48)}</a>
                                      </List.Item>
                                  )}
                                />
                            </Card>
                        </Col>
                    </Row>
                </div>
            );
        }
    // }
}

export default UserDetails;