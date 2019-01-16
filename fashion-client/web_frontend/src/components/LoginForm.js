import 'antd/dist/antd.css';
import axios from 'axios';
import React, {Component} from 'react';
import { Form, Icon, Input, Button, Row, Col,} from 'antd';
import {Redirect} from "react-router-dom";
import './LoginForm.css'

class LoginForm extends Component {
    constructor(props) {
        super(props);
        this.state = {private_key: '', public_key: ''};
    }

    handleSubmit = (e) => {
        e.preventDefault();

        this.props.cookies.set('private_key', e.target[1].value, { path: '/' });
        this.props.cookies.set('public_key', e.target[0].value, { path: '/' });
        window.location.reload();

        // axios.post(`http://127.0.0.1:8888/keys/`, {
        //     private_key: e.target[1].value,
        //     public_key: e.target[0].value
        // }).then(function (response) {
        //     console.log(response);
        // }).catch(function (error) {
        //     console.log(error);
        // });
    };

    generateKeyPair = (e) => {
        e.preventDefault();
        axios.get(`http://127.0.0.1:8888/keys/`)
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
        if (this.props.cookies.get('public_key') && this.props.cookies.get('private_key')){
            return <Redirect to='/' />;

        }else{
            return (
                <div className='homepage'>
                    <Row>
                        <Col span={18} offset={3}>
                            <Form onSubmit={this.handleSubmit} className="login-form">
                                <Form.Item>
                                    <Input
                                        className='public_key'
                                        prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                        placeholder="Public key"
                                        value={this.state.public_key}
                                        onChange={this.updatePublicKey}

                                    />
                                </Form.Item>
                                <Form.Item>
                                    <Input
                                        className='private_key'
                                        prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                        placeholder="Private key"
                                        value={this.state.private_key}
                                        onChange={this.updatePrivateKey}
                                    />
                                </Form.Item>
                                <Form.Item>
                                  <Button type="primary" htmlType="submit" className="login-form-button">
                                    Log in
                                  </Button>
                                    <a> </a>
                                  <Button type="primary"  className="login-form-button" onClick={this.generateKeyPair}>
                                    Generate
                                  </Button>
                                </Form.Item>
                            </Form>
                        </Col>
                    </Row>
                </div>
            );
        }
    };
}

export default LoginForm;