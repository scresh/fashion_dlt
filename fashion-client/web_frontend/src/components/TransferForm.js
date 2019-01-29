import 'antd/dist/antd.css';
import axios from 'axios';
import React, {Component} from 'react';
import { Form, Input, Button, Row, Col} from 'antd';
import {Redirect} from "react-router-dom";
import './Form.css'

class TransferForm extends Component {
    state ={
        sendingForm: false,
    };

    componentDidMount(){
        this.state = {
                public_key: this.props.cookies.get('public_key'),
                private_key: this.props.cookies.get('private_key'),
        };

        if (this.props.match.params.itemID){
            this.setState({sendingForm: true});
            axios.get(`http://127.0.0.1:8888/transactions/?scantrust_id=` + this.props.match.params.itemID)
              .then(res => {
                  this.props.form.setFields({
                      itemID: {
                        value: res.data.data[0].scantrust_id,
                        errors: [],
                      },
                      itemName: {
                        value: res.data.data[0].item_name,
                        errors: [],
                      },
                     itemInfo: {
                        value: res.data.data[0].item_info,
                        errors: [],
                      },
                      itemColor: {
                        value: res.data.data[0].item_color,
                        errors: [],
                      },
                      itemSize: {
                        value: res.data.data[0].item_size,
                        errors: [],
                      },
                      imageURL: {
                        value: res.data.data[0].item_img,
                        errors: [],
                      },
                  });
              })
        }else {
            axios.get(`http://127.0.0.1:8888/transactions/?scantrust_id=` + this.props.match.params.itemID)
              .then(res => {
                  this.props.form.setFields({
                      receiver: {
                          value: this.state.public_key,
                          errors: [],
                      },
                  })})
        }
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                values.public_key = this.props.cookies.get('public_key');
                values.private_key = this.props.cookies.get('private_key');
                axios.post(`http://127.0.0.1:8888/transfer/`, { values })
                      .then(res => {
                      })
            }
        });
    };



    render() {
        const { getFieldDecorator } = this.props.form;
        console.log(this.props.form);
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
                            <p/>
                            <Form onSubmit={this.handleSubmit}>
                                <Form.Item {...formItemLayout} label="Scantrust ID">
                                  {getFieldDecorator('itemID', {
                                    rules: [{
                                      required: true,
                                      message: 'Please input item ScanTrust ID',
                                    }],
                                  })(
                                    <Input
                                        placeholder="Please input item ScanTrust ID"
                                        disabled={this.state.sendingForm}
                                    />
                                  )}
                                </Form.Item>
                                <Form.Item {...formItemLayout} label="Name">
                                  {getFieldDecorator('itemName', {
                                    rules: [{
                                      required: true,
                                      message: 'Please input item name',
                                    }],
                                  })(
                                    <Input
                                        placeholder="Please input item name"
                                        disabled={this.state.sendingForm}
                                    />
                                  )}
                                </Form.Item>
                                <Form.Item {...formItemLayout} label="Color">
                                  {getFieldDecorator('itemColor', {
                                    rules: [{
                                      required: true,
                                      message: 'Please input item color',
                                    }],
                                  })(
                                    <Input
                                        placeholder="Please input item color"
                                        disabled={this.state.sendingForm}
                                    />
                                  )}
                                </Form.Item>
                                <Form.Item {...formItemLayout} label="Info">
                                  {getFieldDecorator('itemInfo', {
                                    rules: [{
                                      required: true,
                                      message: 'Please input item info',
                                    }],
                                  })(
                                    <Input
                                        placeholder="Please input item info"
                                        disabled={this.state.sendingForm}
                                    />
                                  )}
                                </Form.Item>
                                <Form.Item {...formItemLayout} label="Size">
                                  {getFieldDecorator('itemSize', {
                                    rules: [{
                                      required: true,
                                      message: 'Please input item size',
                                    }],
                                  })(
                                    <Input
                                        placeholder="Please input item size"
                                        disabled={this.state.sendingForm}
                                    />
                                  )}
                                </Form.Item>
                                <Form.Item {...formItemLayout} label="Image URL">
                                  {getFieldDecorator('imageURL', {
                                    rules: [{
                                      required: true,
                                      message: 'Please input item image URL',
                                    }],
                                  })(
                                    <Input
                                        placeholder="Please input item image URL"
                                        disabled={this.state.sendingForm}
                                    />
                                  )}
                                </Form.Item>
                                <Form.Item {...formItemLayout} label="Receiver">
                                  {getFieldDecorator('receiver', {
                                    rules: [{
                                      required: true,
                                      message: 'Please input item receiver',
                                    }],
                                  })(
                                    <Input
                                        placeholder="Please input item receiver"
                                        disabled={!this.state.sendingForm}
                                    />
                                  )}
                                </Form.Item>
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

const WrappedApp = Form.create({})(TransferForm);


export default WrappedApp;