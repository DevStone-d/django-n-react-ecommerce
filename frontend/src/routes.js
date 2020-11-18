import React from "react";
import {Route} from "react-router-dom";

import Hoc from "./hoc/hoc";


import HomepageLayout from "./containers/Home";
import ProductList from "./containers/ProductList";


const BaseRouter = ()=>(
    <Hoc>
        <Route exact path="/" component={HomepageLayout}/>
        {/* <Route path="/login" component={Login}/>
        <Route path="/signup" component={Signup}/> */}
        <Route path="/products" component={ProductList}/>
    </Hoc>
);

export default BaseRouter;