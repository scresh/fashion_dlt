import axios from 'axios';
import React, {Component} from 'react';
import { Card, Row, Col, Timeline, Table } from 'antd';


const columns = [{
  title: 'Attribute',
  dataIndex: 'key',
}, {
  title: 'Value',
  dataIndex: 'value',
}];


function makeDict(transactions) {
    const dict = {
        attributes: [],
        owners: [],
    };

    for (let i=0; i < transactions.length; i++){
        dict.scantrust_id = transactions[i].scantrust_id;
        dict.item_name = transactions[i].item_name;
        dict.item_info = transactions[i].item_info;
        dict.item_color = transactions[i].item_color;
        dict.item_size = transactions[i].item_size;
        dict.item_img = transactions[i].item_img;
        dict.item_img_md5 = transactions[i].item_img_md5;

        dict.attributes = [{
          key: 'Name',
          value: dict.item_name,
        }, {
          key: 'Info',
          value: dict.item_info,
        }, {
          key: 'Color',
          value: dict.item_color,
        }, {
          key: 'Size',
          value: dict.item_size,
        }, {
          key: 'Owner',
          value: transactions[i].receiver,
        },

        ];

        dict.owners.push(transactions[i].receiver);
    }

    return dict;
}

class ItemDetails extends Component {
    state = {
        itemID: this.props.match.params.itemID,
        attributes: [],
        owners: [],
    };

    componentDidMount() {
    axios.get(`http://127.0.0.1:8888/transactions/?scantrust_id=` + this.state.itemID)
      .then(res => {this.setState(makeDict(res.data.data));
      })
    }

    render() {
        // if (this.state.dict.owners.length > 0){
            return (
                <div className={this.state.scantrust_id}>
                    <Row>
                        <Col span={18} offset={3}>
                            <Card
                                title={'Scantrust ID: ' + this.state.scantrust_id}
                                // style={{ width: 600 }}
                                // cover={<img alt={this.state.item_name} src={this.state.item_img} />}

                            >
                                <Row gutter={12}>
                                    <Col span={6} push={18}>
                                        <Table
                                            pagination={false}
                                            bordered
                                            dataSource = {[1]}
                                            title={() => <img width={'100%'} alt={this.state.item_name} src={this.state.item_img} />}
                                            footer={() => 'MD5: ' + this.state.item_img_md5}
                                          />

                                    </Col>
                                    <Col span={18} pull={6}>
                                        <Table
                                            pagination={false}
                                            columns={columns}
                                            dataSource={this.state.attributes}
                                            bordered
                                            title={() => 'Item Details'}
                                          />
                                    </Col>
                                </Row>
                                <Row gutter={12}>
                                    <Col span={12} offset={6}>
                                         <Card title="Item history" bordered={false} >
                                             <Timeline>
                                                 {this.state.owners.map(el => <Timeline.Item>{el}</Timeline.Item>)}
                                             </Timeline>
                                         </Card>
                                    </Col>
                                </Row>





                            </Card>
                        </Col>
                    </Row>
                </div>
            );
        }
    // }
}

export default ItemDetails;