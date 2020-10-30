import React from 'react';

import axios from 'axios';

export default class productList extends React.Component {
  state = {
    products: []
  }

  componentDidMount() {
    axios.get(`http://127.0.0.1:8000/api/products`)
      .then(res => {
        const products = res.data;
        this.setState({ products });
      })
  }

  render() {
    return (
      <ul>
        {this.state.products.map(product => <li>{product.name}</li>)}
      </ul>
    )
  }
}