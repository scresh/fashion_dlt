import './App.css';
import { withCookies } from 'react-cookie';
import 'antd/dist/antd.css';
import React, { Component } from 'react';
import { BrowserRouter as Router , Link} from 'react-router-dom';
import { Layout, Menu } from 'antd';
import BaseRouter from './routes';
const { Header, Content, Footer} = Layout;


const AppLayout = (props) => {
    return (
        <Layout className="layout">
            <Header>
                <div className="logo" />
                <Menu
                    theme="dark"
                    mode="horizontal"
                    defaultSelectedKeys={['2']}
                    style={{ lineHeight: '64px' }}
                >
                    <Menu.Item key="home"><Link to="/">Home</Link></Menu.Item>

                </Menu>
            </Header>
            <Content style={{ padding: '0 50px' }}>
                <div style={{ background: '#fff', padding: 24, minHeight: 280 }}>
                    {props.children}
                </div>
            </Content>
            <Footer style={{ textAlign: 'center' }}>
                Ant Design ©2018 Created by Ant UED
            </Footer>
        </Layout>
    );
};

class App extends Component {
  render() {
    return (
      <div className="App">
          <Router>
              <AppLayout>
                <BaseRouter cookies={this.props.cookies}/>
              </AppLayout>
          </Router>
      </div>
    );
  }
}

export default withCookies(App);