import React from 'react';
import { Route } from 'react-router-dom';
import TransactionList from './components/TransactionList';
import ItemDetails from './components/ItemDetails';
import HomePage from './components/HomePage';

class BaseRouter extends React.Component {
  render() {
    return <div>
        <Route exact path='' render={() => (<HomePage cookies={this.props.cookies}/>)} />
        <Route exact path='/transactions' render={() => (<TransactionList cookies={this.props.cookies}/>)} />
        <Route exact path='/items/:itemID' render={() => (<ItemDetails cookies={this.props.cookies}/>)} />
    </div>;
  }
}

export default BaseRouter;