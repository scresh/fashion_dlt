import './HomePage.css';
import 'antd/dist/antd.css';
import axios from 'axios';
import React, {Component} from 'react';
import { Carousel } from 'antd';


class HomePage extends Component {
    state = {
        transactions: []
    };

    componentDidMount() {
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
            <Carousel effect="fade">
                <div><h3>1</h3></div>
                <div><h3>2</h3></div>
                <div><h3>3</h3></div>
                <div><h3>4</h3></div>
          </Carousel>
        );
    }
}

export default HomePage;