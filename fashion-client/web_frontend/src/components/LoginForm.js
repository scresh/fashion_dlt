import 'antd/dist/antd.css';
import axios from 'axios';
import React, {Component} from 'react';
import { Form, Icon, Input, Button, Checkbox, Row, Col,} from 'antd';
import {Redirect} from "react-router-dom";
import './LoginForm.css'

class LoginForm extends Component {
    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
            }
        });
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
                                    <Input prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="Public key" />
                                </Form.Item>
                                <Form.Item>
                                    <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="Private key" />
                                </Form.Item>
                                <Form.Item>
                                  <Button type="primary" htmlType="submit" className="login-form-button">
                                    Log in
                                  </Button>
                                    <a> </a>
                                  <Button type="primary"  className="login-form-button">
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