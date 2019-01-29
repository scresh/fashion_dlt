import React from 'react';
import { Route } from 'react-router-dom';
import TransactionList from './components/TransactionList';
import ItemDetails from './components/ItemDetails';
import HomePage from './components/HomePage';
import LogoutPage from "./components/LogoutPage";
import LoginForm from "./components/LoginForm";
import UserDetails from "./components/UserDetails";
import TransferForm from "./components/TransferForm";

class BaseRouter extends React.Component {
  render() {
    return <div>
        <Route exact path='' component={HomePage} />
        <Route exact path='/transactions' component={TransactionList} />
        <Route exact path='/items/:itemID' component={ItemDetails} />
        <Route exact path='/users/:userID' render={(props) => <UserDetails {...props} cookies={this.props.cookies} />}/>
        <Route exact path='/account' render={(props) => <UserDetails {...props} cookies={this.props.cookies} />}/>
        <Route exact path='/transfer/:itemID?' render={(props) => <TransferForm {...props} cookies={this.props.cookies} />}/>
        <Route exact path='/login' render={(props) => <LoginForm {...props} cookies={this.props.cookies} />}/>
        <Route exact path='/logout' render={(props) => <LogoutPage {...props} cookies={this.props.cookies} />}/>
    </div>;
  }
}

export default BaseRouter;