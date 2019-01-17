import 'antd/dist/antd.css';
import axios from 'axios';
import React, {Component} from 'react';
import { Form, Icon, Input, Button, Row, Col, Alert,} from 'antd';
import {Redirect} from "react-router-dom";
import './Form.css'

class TransferForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            item: {
                public_key: this.props.cookies.get('public_key'),
                private_key: this.props.cookies.get('private_key'),
                scantrust_id: '',
                item_name: '',
                item_info: '',
                item_color: '',
                item_size: '',
                item_img: '',
                item_img_md5: '',
            }
        };
        if (this.props.match.params.itemID){
            axios.get(`http://127.0.0.1:8888/transactions/?scantrust_id=` + this.props.match.params.itemID)
              .then(res => {this.setState(res.data.data[0]);})
        }
    }

    validateKeyPair = (e) => {
        e.preventDefault();

        axios.get(
            `http://127.0.0.1:8888/validator/?private_key=${this.state.private_key}&public_key=${this.state.public_key}`
        ).then(res => {
            const result = res.data.result;
            if (result === 'OK'){
                this.props.cookies.set('private_key', this.state.private_key, { path: '/' });
                this.props.cookies.set('public_key', this.state.public_key, { path: '/' });
                window.location.reload();
            } else {
                this.setState(
                    {alert: <Alert message="Error"
                                   description={result}
                                   type="error"
                                   showIcon
                            />});
            }

          });
    };

    generateKeyPair = (e) => {
        e.preventDefault();
        axios.get(`http://127.0.0.1:8888/generator/`)
          .then(res => {
            const key_pair = res.data;
            this.setState({ private_key: key_pair.private_key,  public_key: key_pair.public_key });
          });
    };

    updatePrivateKey = (e) => {
        e.preventDefault();
        this.setState({private_key: e.target.value});
    };

    updatePublicKey = (e) => {
        e.preventDefault();
        this.setState({public_key: e.target.value});
    };


    render() {
        const formItemLayout = {
            labelCol: {
            xs: { span: 24 },
            sm: { span: 8 },
          },
          wrapperCol: {
            xs: { span: 24 },
            sm: { span: 16 },
          },
        };
        if (this.props.cookies.get('public_key') && this.props.cookies.get('private_key')){
            return (
                <div className='homepage'>
                    <Row>
                        <Col span={18} offset={3}>
                            {this.state.alert}
                            <p/>
                            <Form onSubmit={this.handleSubmit}>
                                <Form.Item {...formItemLayout} label="Scantrust ID"><Input /></Form.Item>
                                <Form.Item {...formItemLayout} label="Name"><Input /></Form.Item>
                                <Form.Item {...formItemLayout} label="Info"><Input /></Form.Item>
                                <Form.Item {...formItemLayout} label="Color"><Input /></Form.Item>
                                <Form.Item {...formItemLayout} label="Size"><Input /></Form.Item>
                                <Form.Item {...formItemLayout} label="Image URL"><Input /></Form.Item>
                                <Form.Item {...formItemLayout} label="Receiver"><Input /></Form.Item>
                                <Form.Item {...formItemLayout}>
                                    <Button type="primary" htmlType="submit">Create</Button>
                                </Form.Item>
                            </Form>
                        </Col>
                    </Row>
                </div>
            );
        }else{
            return <Redirect to='/' />;
        }
    };
}

export default TransferForm;