import axios from 'axios';
import React, {Component} from 'react';
import { List, Avatar, Icon, Tooltip, Tag, Card} from 'antd';

const { Meta } = Card;

const IconText = ({ type, text }) => (
    <span><Icon type={type} style={{ marginRight: 8 }} />{text}</span>
);

class TransactionList extends Component {
    state = {};

    componentDidMount() {
        axios.get('http://127.0.0.1:8000/transaction')
            .then(
                res => {
                    this.setState({
                        transactions: res.data
                    });
                }
            );
        console.log()
    }

    render() {
        return (
            <div className="TransactionList">
                <List
                    grid={{ gutter: 32, column: 4 }}
                    itemLayout="vertical"
                    size="large"
                    pagination={{
                        pageSize: 8,
                    }}
                    dataSource={this.state.films}
                    renderItem={item => (
                        <List.Item>
                            <Card
                              style={{marginTop: 16 }}
                              actions={[
                                <IconText type="clock-circle" text={ item.length + ' min' } />,
                                <IconText type="dollar" text={ "$" + item.price} />,
                                <IconText type="calendar" text={ item.release_year } />,
                              ]}
                              cover={<img alt={item.scantrust_id} src={item.photo_url} />}
                            >
                                <Meta
                                  avatar={
                                    <Tooltip title={ item.language.name }>
                                        <Avatar src={item.language.icon_url} />
                                    </Tooltip>
                                    }
                                  title={<a href={`/films/${item.id}/`}>{item.title}</a>}
                                  description={
                                      item.category.map(
                                          (category) =>
                                              <Tag color="magenta" key={category.toLowerCase()}> { category } </Tag>
                                      )}
                                />
                            </Card>
                        </List.Item>
                    )}

                />
            </div>
        );
    }
}

export default TransactionList;