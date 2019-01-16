import 'antd/dist/antd.css';
import axios from 'axios';
import React, {Component} from 'react';
import { Card, Row, Col, Timeline, Table } from 'antd';


class HomePage extends Component {
    componentDidMount() {
        console.log(this.props.cookies)
    // axios.get(`http://127.0.0.1:8888/transactions/`)
    //   .then(res => {
    //     const transactions = res.data.data.map(
    //         (transaction) => addShortValues(transaction)
    //     );
    //     this.setState({ transactions: transactions });
    //     console.log(this.state.transactions)
    //   })
    }

    render() {
        return (
            <div className='homepage'>
                    <Row>
                        <Col span={18} offset={3}>
                            <Card
                                title={'Home page'}
                                cover={<img alt='dlt' src='http://scet.berkeley.edu/wp-content/uploads/BCgraphicelement-3.png' />}

                            >
                            </Card>
                        </Col>
                    </Row>
                </div>
        );
    }
}

export default HomePage;