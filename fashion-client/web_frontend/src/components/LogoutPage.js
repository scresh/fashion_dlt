import { Redirect } from 'react-router-dom'
import React, {Component} from "react";

class LogoutPage extends Component {
    constructor(props){
        super(props);
        if (this.props.cookies.get('public_key') || this.props.cookies.get('private_key')){
            this.props.cookies.remove('public_key');
            this.props.cookies.remove('private_key');
            window.location.reload();
        }

    }
    render() {
        return <Redirect to='/' />;
    }
}

export default LogoutPage;