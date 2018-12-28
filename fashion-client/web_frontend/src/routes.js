import React from 'react';
import { Route } from 'react-router-dom';
import TransactionList from './components/TransactionList';

const BaseRouter = () => (
    <div>
        <Route exact path='/transactions' component={ TransactionList} />
    </div>
);


export default BaseRouter;