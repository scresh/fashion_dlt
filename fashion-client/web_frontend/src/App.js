import './App.css';
import { withCookies } from 'react-cookie';
import 'antd/dist/antd.css';
import React, { Component } from 'react';
import { BrowserRouter as Router , Link} from 'react-router-dom';
import { Layout, Menu, Breadcrumb } from 'antd';
import BaseRouter from './routes';

const { Header, Content, Footer} = Layout;

class AppLayout extends Component {
    constructor(props) {
      super(props);
      // Don't call this.setState() here!
      this.menuItems = [
          {name: 'Home', key: 'home', href: '/'},
          {name: 'Transactions', key: 'transactions', href: '/transactions'},
      ];

      console.log(props.cookies.get('public_key'));

      if (props.cookies.get('public_key')){
          this.menuItems.push({name: 'Account', key: 'account', href: '/account'});
          this.menuItems.push({name: 'Logout', key: 'logout', href: '/logout'});
      }else {
          this.menuItems.push({name: 'Login', key: 'login', href: '/login'});

      }
    }

    render() {
        return (
            <Layout className="layout" >
                <Header>
                    <div className="logo"/>
                    <Menu
                        theme="dark"
                        mode="horizontal"
                        defaultSelectedKeys={['2']}
                        style={{lineHeight: '64px'}}
                    >
                        {
                            this.menuItems.map((item) =>
                                <Menu.Item key={item.key}><Link to={item.href}>{item.name}</Link></Menu.Item>
                            )
                        }
                    </Menu>
                </Header>
                <Layout>
                    <Breadcrumb style={{margin: '16px 0'}} >
                        <Breadcrumb.Item/>
                    </Breadcrumb>
                    <Content style={{padding: '0 50px'}}>
                        <div style={{background: '#fff', padding: 24, minHeight: "calc(100vh - 186px)"}}>
                            {this.props.children}
                        </div>
                    </Content>
                    <Footer style={{textAlign: 'center'}}>
                        &bull; Fashion DLT &bull;    2019 &bull;    <br/> &bull; Created by <a
                        href={'https://github.com/scresh'}><b>scresh</b></a>  &bull;
                    </Footer>
                </Layout>
            </Layout>
        );
    }
}

class App extends Component {
  render() {
    return (
      <div className="App">
          <Router>
              <AppLayout {...this.props}>
                <BaseRouter {...this.props}/>
              </AppLayout>
          </Router>
      </div>
    );
  }
}

export default withCookies(App);