import 'antd/dist/antd.css';
import axios from 'axios';
import React, {Component} from 'react';
import { Form, Icon, Input, Button, Row, Col, Alert,} from 'antd';
import {Redirect} from "react-router-dom";
import './LoginForm.css'

class LoginForm extends Component {
    constructor(props) {
        super(props);
        this.state = {private_key: '', public_key: '', alert: ''};
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
        if (this.props.cookies.get('public_key') && this.props.cookies.get('private_key')){
            return <Redirect to='/' />;

        }else{
            return (
                <div className='homepage'>
                    <Row>
                        <Col span={18} offset={3}>
                            {this.state.alert}
                            <p/>
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
                                  <Button type="primary"  className="login-form-button" onClick={this.validateKeyPair}>
                                    Login
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