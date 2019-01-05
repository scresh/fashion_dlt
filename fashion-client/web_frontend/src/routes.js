import React from 'react';
import { Route } from 'react-router-dom';
import TransactionList from './components/TransactionList';
import ItemDetails from './components/ItemDetails';

const BaseRouter = () => (
    <div>
        <Route exact path='/transactions' component={ TransactionList} />
        <Route exact path='/items/:itemID' component={ ItemDetails} />

    </div>
);


export default BaseRouter;